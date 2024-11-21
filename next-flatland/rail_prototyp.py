from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
import random
from typing import Dict, List, Set, Any, TypeVar
from gen_env import (
    Agent,
    Arbiter,
    Effect,
    Agent,
    Entity,
    GenEnvSimulation,
    Relation,
    Resource,
    SystemState,
    Propagator,
)
import networkx as nx
import matplotlib.pyplot as plt


@dataclass()
class RailResource(Resource):
    id: int
    valid_routes: dict[Resource, list[Resource]]
    x: int
    y: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, RailResource):
            return self.id == other.id
        return False


@dataclass()
class MoveAction:
    agent: TrainAgent
    destination: RailResource


class RailNetwork:
    def __init__(self):
        self.coordinates = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (2, 1),
            (3, 1),
        ]
        self.resources = [
            RailResource(id=i, valid_routes={}, x=coord[0], y=coord[1])
            for i, coord in enumerate(self.coordinates)
        ]
        self.relations = []
        self._initialize_routes()
        self._initialize_relations()

    def _initialize_routes(self):
        """
             6 7
             - - 
           /     \ 
        - -  - -  - -
        0 1  2 3  4 5
        """
        # Define valid routes for straight line 0->1->2->3->4->5
        for i in range(1, 4):
            self.resources[i].valid_routes[self.resources[i - 1]] = [self.resources[i]]
            self.resources[i + 1].valid_routes[self.resources[i + 1]] = [
                self.resources[i]
            ]

        self.resources[0].valid_routes[self.resources[1]] = [self.resources[1]]
        self.resources[0].valid_routes[self.resources[0]] = [self.resources[1]]
        self.resources[5].valid_routes[self.resources[4]] = [self.resources[4]]
        self.resources[5].valid_routes[self.resources[5]] = [self.resources[4]]

        # Define valid routes for straight line 6->7
        self.resources[6].valid_routes[self.resources[1]] = [self.resources[7]]
        self.resources[7].valid_routes[self.resources[4]] = [self.resources[6]]
        self.resources[6].valid_routes[self.resources[7]] = [self.resources[1]]
        self.resources[7].valid_routes[self.resources[6]] = [self.resources[4]]

        # Add switch connections
        # At resource 1 (connecting to 6)
        self.resources[1].valid_routes[self.resources[0]] = [
            self.resources[2],
            self.resources[6],
        ]
        self.resources[1].valid_routes[self.resources[2]] = [self.resources[0]]
        self.resources[1].valid_routes[self.resources[6]] = [self.resources[0]]

        # At resource 4 (connecting to 7)
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
                    relation = Relation(
                        from_entity=from_resource, to_entity=to_resource
                    )
                    self.relations.append(relation)

    def get_resources(self):
        return self.resources

    def get_relations(self):
        return self.relations

    def plot_network(self):
        G = nx.DiGraph()
        for resource in self.resources:
            G.add_node(resource.id, pos=(resource.x, resource.y))
            for dest in resource.valid_routes.get(resource, []):
                G.add_edge(resource.id, dest.id)

        pos = nx.get_node_attributes(G, "pos")
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=700,
            node_color="skyblue",
            font_size=10,
            font_weight="bold",
        )
        plt.show()


@dataclass
class RandomPolicy:
    def propose_next_position(
        self, current_position: RailResource, previous_position: RailResource
    ) -> RailResource:
        possible_resources = list(current_position.valid_routes[current_position])
        if previous_position in possible_resources:
            possible_resources.remove(previous_position)
        if not possible_resources:
            return None
        return random.choice(possible_resources)


@dataclass
class TrainAgent(Agent):
    id: int
    current_position: RailResource
    previous_position: RailResource = None
    policy: RandomPolicy = None
    _state: Dict = None
    _rules: Set = None
    _objectives: Dict = None

    def __post_init__(self):
        self._state = {
            "current_position": self.current_position,
            "previous_position": self.previous_position,
        }
        self._rules = {
            "valid_move": lambda next_pos: next_pos
            in self.current_position.valid_routes.get(self.current_position, [])
        }
        self._objectives = {"reach_end": False}

    @property
    def state(self):
        return self._state

    @property
    def rules(self) -> Set[Any]:
        return self._rules

    @property
    def objectives(self):
        return self._objectives

    def act(self) -> Effect:
        next_position = self.policy.propose_next_position(
            self.current_position, self.previous_position
        )
        print(next_position.id)
        if next_position is None:
            return None

        return AddAndRemoveRelation(
            add_relation=Relation(from_entity=self, to_entity=next_position),
            remove_relation=Relation(from_entity=self, to_entity=self.current_position),
        )


@dataclass()
class MoveEffect(Effect):
    entity: Entity
    from_position: Resource
    to_position: Resource


@dataclass()
class AddRelation(Effect):
    relation: Relation


@dataclass()
class RemoveRelation(Effect):
    relation: Relation


class RailState(SystemState[Agent, Relation, RailResource]):
    def __init__(
        self,
        agents: list[Agent],
        relations: list[Relation],
        resources: list[RailResource],
    ):
        self.agents = agents
        self.relations = relations
        self.resources = resources

    def pull_actions(self):
        """Pull actions from all agents"""
        for agent in self.agents:
            if isinstance(agent, TrainAgent):
                yield agent.act()

    def actions_to_effects(self, actions) -> list[Effect]:
        effects = []
        for action in actions:
            effects.append(
                MoveEffect(
                    entity=action.agent,
                    from_position=action.agent.previous_position,
                    to_position=action.destination,
                )
            )
        return effects

    def relations_by_entity(self):
        relations_by_entity = defaultdict(int)
        for relation in self.relations:
            relations_by_entity[relation.to_entity] += 0
        return relations_by_entity

    def add_entity(self, entity: Agent):
        self.agents.append(entity)

    def add_relation(self, from_entity: Agent, to_entity: Agent):
        self.relations.append(Relation(from_entity, to_entity))

    def remove_relation(self, from_entity: Agent, to_entity: Agent):
        self.relations.remove(Relation(from_entity, to_entity))

    def add_resource(self, resource: RailResource):
        self.resources.append(resource)


@dataclass()
class RailArbiter(Arbiter):
    rail_state: RailState

    def check_rules(self, effects: list[Effect]) -> list[Effect]:
        valid_effects: list[Effect] = []
        relations_by_entity = self.rail_state.relations_by_entity()

        for effect in effects:
            if isinstance(effect, MoveEffect):
                agent = effect.entity
                from_position = effect.from_position
                to_position = effect.to_position

                for entity in (
                    self.rail_state.resource_occupancy[to_position] is not None
                ):
                    if isinstance(entity, TrainAgent):
                        print(
                            "conflict with between agents {} and {}".format(
                                agent.id, entity.id
                            )
                        )
                        continue

                # Check if transition is valid
                if resource_to_add.id in resource_to_remove.valid_routes.get(
                    agent.previous_position, []
                ):
                    valid_effects.append(effect)
                else:
                    print(
                        f"Invalid transition from {resource_to_remove.id} to {resource_to_add.id}"
                    )

        return valid_effects


@dataclass
class RailPropagator(Propagator):
    rail_state: RailState

    def propagate(self, effects: List[Effect]) -> Dict[Agent, bool]:
        """
        Propagates effects by:
        - Validating effect types
        - Updating agent positions
        - Updating rail state relations
        - Tracking completion status
        """
        dones = {}

        for effect in effects:
            if isinstance(effect, MoveEffect):
                agent = effect.add_relation.from_entity
                next_position = effect.add_relation.to_entity
                current_position = effect.remove_relation.to_entity

                # Update agent's position
                agent.previous_position = current_position
                agent.current_position = next_position

                # Update relations in rail state
                self.rail_state.remove_relation(agent, current_position)
                self.rail_state.add_relation(agent, next_position)

                # Track if agent has completed its objective
                dones[agent] = False  # Could be updated based on objectives

        return dones


# Example usage
if __name__ == "__main__":
    rail_network = RailNetwork()
    initial_position = [rail_network.resources[0], rail_network.resources[5]]

    # Create agents with random policy
    agents = [
        TrainAgent(
            id=i,
            current_position=initial_position[i],
            previous_position=initial_position[i],
            policy=RandomPolicy(),
        )
        for i in range(2)
    ]

    # Setup simulation components
    rail_state = RailState(
        agents=agents,
        relations=rail_network.relations,
        resources=rail_network.resources,
    )
    rail_arbiter = RailArbiter(rail_state=rail_state)
    rail_propagator = RailPropagator(rail_state=rail_state)

    # Create and run simulation
    simulation = GenEnvSimulation(
        propagator=rail_propagator, state=rail_state, arbiter=rail_arbiter
    )

    simulation.run()
