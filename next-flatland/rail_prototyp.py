from __future__ import annotations

from dataclasses import dataclass
from gen_env import Agent, Arbiter, Effect, Agent, Relation, Resource, SystemState


@dataclass()
class RailResource(Resource):
    id: int
    valid_routes: dict[RailResource, list[RailResource]]


@dataclass()
class MoveAction:
    agent: Agent
    destination: RailResource


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
            self.resources[i + 1].valid_routes[self.resources[i + 1]] = [
                self.resources[i]
            ]

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
                    relation = Relation(
                        from_entity=from_resource, to_entity=to_resource
                    )
                    self.relations.append(relation)

    def get_resources(self):
        return self.resources

    def get_relations(self):
        return self.relations


@dataclass()
class TrainAgent(Agent):
    id: int
    previous_position: RailResource

    def act(self):
        next_position = self.previous_position.valid_routes[self.previous_position][0]
        return MoveAction(self, next_position)


@dataclass()
class AddAndRemoveRelation(Effect):
    add_relation: Relation
    remove_relation: Relation


@dataclass()
class AddRelation(Effect):
    relation: Relation


@dataclass()
class RemoveRelation(Effect):
    relation: Relation


class RailState(SystemState[Agent, Relation, RailResource]):
    def __init__(
        self,
        agents_starting_resources: list[Resource],
    ):
        rail_network = RailNetwork()
        self.agents = [TrainAgent(id=i) for i in range(len(agents_starting_resources))]
        self.relations = rail_network.get_relations()
        self.resources = rail_network.get_resources()
        self.relations.extend(
            [
                Relation(agent, resource)
                for agent, resource in zip(self.agents, agents_starting_resources)
            ]
        )

    def pull_actions(self):
        actions = []
        for agent in self.agents:
            actions.append(agent.act())
        return actions

    def actions_to_effects(self, actions: list[MoveAction]) -> list[Effect]:
        effects = []
        for action in actions:
            effects.append(
                AddAndRemoveRelation(
                    remove_relation=Relation(
                        action.agent, action.agent.previous_position
                    ),
                    add_relation=Relation(action.agent, action.destination),
                )
            )
        return effects

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
        for effect in effects:
            if isinstance(effect, AddAndRemoveRelation):
                agent = effect.add_relation.from_entity
                resource_to_add = effect.add_relation.to_entity
                resource_to_remove = effect.remove_relation.to_entity

                # occupation check
                valid_occupation = (
                    self.rail_state.relations_by_entity()[resource_to_add] == 0
                )
                if not valid_occupation:
                    print("agent {} stopped at occupied resource".format(agent.id))
                    continue

                # transition check
                valid_transition = (
                    resource_to_add.id
                    in resource_to_remove.valid_routes[agent.previous_position]
                )
                if not valid_transition:
                    print("agent {} stopped at invalid transition".format(agent.id))

                valid_effects.extend(
                    [
                        AddRelation(effect.add_relation),
                        RemoveRelation(effect.remove_relation),
                    ]
                )

        return valid_effects
