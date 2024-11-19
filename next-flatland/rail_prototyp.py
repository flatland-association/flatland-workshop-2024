from dataclasses import dataclass
from gen_env import Agent, Arbiter, Effect, Agent, Relation, Resource, SystemState


@dataclass()
class RailResource(Resource):
    id: int
    valid_routes: dict[Resource, list[Resource]]


@dataclass()
class TrainAgent(Agent):
    id: int
    previous_position: Resource

    def act(self):
        return AddAndRemoveRelation(
            remove_relation=Relation(
                self, self.previous_position, self.current_position
            ),
            add_relation=Relation(self, self.current_position, self.next_position),
        )


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


class RailState(SystemState):
    def __init__(
        self,
        agents: list[Agent],
        relations: list[Relation],
        resources: list[RailResource],
    ):
        self.entities = agents
        self.relations = relations
        self.resources = resources

    def pull_actions(self):
        for agent in self.entities:
            if isinstance(agent, TrainAgent):
                yield agent.act()

    def add_entity(self, entity: Agent):
        self.entities.append(entity)

    def add_relation(self, from_entity: Agent, to_entity: Agent):
        self.relations.append(Relation(from_entity, to_entity))

    def remove_relation(self, from_entity: Agent, to_entity: Agent):
        self.relations.remove(Relation(from_entity, to_entity))

    def add_resource(self, resource: RailResource):
        self.resources.append(resource)


class RailArbiter(Arbiter):
    def check_rules(self, effects: list[Effect]) -> list[Effect]:
        valid_effects: list[Effect] = []
        for effect in effects:
            if isinstance(effect, AddAndRemoveRelation):
                agent = effect.add_relation.from_entity
                resource_to_add = effect.add_relation.to_entity
                resource_to_remove = effect.remove_relation.to_entity

                # occupation check
                resource_to_add.relations

                # transition check
                valid_transition = (
                    resource_to_add.id
                    in resource_to_remove.valid_routes[agent.previous_position]
                )
                if valid_transition:
                    valid_effects.extend(
                        [
                            AddRelation(effect.add_relation),
                            RemoveRelation(effect.remove_relation),
                        ]
                    )
                print("agent {} stopped at invalid transition".format(agent.id))

        return valid_effects
