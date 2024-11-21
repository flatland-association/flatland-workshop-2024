from dataclasses import dataclass
from typing import Dict, List, TypeVar

from gen_env import Relation

EntityType = TypeVar("EntityType")
StateType = TypeVar("StateType")


@dataclass
class Resource:
    id: int


@dataclass
class RailResource(Resource):
    id: int
    valid_routes: Dict[Resource, List[Resource]]


class RailNetwork:
    def __init__(self):
        self.resources = [RailResource(id=i, valid_routes={}) for i in range(8)]
        self.relations = []
        self._initialize_routes()
        self._initialize_relations()

    def _initialize_routes(self):
        # Define valid routes for straight line 0->1->2->3->4->5
        for i in range(5):
            self.resources[i].valid_routes[self.resources[i]] = [self.resources[i + 1]]
            self.resources[i + 1].valid_routes[self.resources[i + 1]] = [self.resources[i]]

        # Define valid routes for straight line 6->7
        self.resources[6].valid_routes[self.resources[6]] = [self.resources[7]]
        self.resources[7].valid_routes[self.resources[7]] = [self.resources[6]]

        # Add switch connections
        # At resource 1 (connecting to 6)
        self.resources[1].valid_routes[self.resources[0]] = [
            self.resources[2],
            self.resources[6],
        ]
        self.resources[1].valid_routes[self.resources[2]] = [self.resources[0]]
        self.resources[1].valid_routes[self.resources[6]] = [self.resources[0]]

        # Move switch from resource 5 to resource 4
        self.resources[4].valid_routes[self.resources[5]] = [
            self.resources[3],
            self.resources[7],
        ]
        self.resources[4].valid_routes[self.resources[3]] = [self.resources[5]]
        self.resources[4].valid_routes[self.resources[7]] = [self.resources[5]]

    def _initialize_relations(self):
        for resource in self.resources:
            for from_resource, to_resources in resource.valid_routes.items():
                for to_resource in to_resources:
                    relation = Relation(from_entity=from_resource, to_entity=to_resource)
                    self.relations.append(relation)

    def get_resources(self):
        return self.resources

    def get_relations(self):
        return self.relations


# Example usage
if __name__ == "__main__":
    rail_network = RailNetwork()
    resources = rail_network.get_resources()
    relations = rail_network.get_relations()
