from abc import abstractmethod, ABCMeta
from collections import defaultdict
from dataclasses import dataclass
from typing import Set, Generic, TypeVar, Any, List, Dict


# TODO type hints and generics domain-agnostic
class Entity(metaclass=ABCMeta):
    @property
    @abstractmethod
    def state(self):
        """
        The internal state representing the entity's own dynamics/attributes.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def rules(self) -> Set[Any]:
        """
                A set of internal rules to determine if a proposed effect with the current entity is allowed
        or not.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def objectives(self):
        """
        Objective influences the action posed on the entity.
        """
        raise NotImplementedError()


class Resource(Entity):
    """
    Resource to be allocated. Agents occupy or "use" the resources to achieve certain
    action. e.g. track of train system, bandwidth of internet, storage space of warehouse systems.
    Except the 3 basic attributes, a resource can also have other attributes like capacity ,
    location , etc.
    """

    pass


class Agent(Entity):
    """
        Agents drive the internal dynamics of the system. An agent has a policy , which is a
    mapping from current state (including agent, object, and resource's objectives) to an action.
    Agent is the only entity that can propose an action to modify the system.
    """

    @property
    @abstractmethod
    def policy(self):
        """
        Objective influences the action posed on the entity.
        """
        raise NotImplementedError()

    @abstractmethod
    def act(self):
        """
                An agent takes its current observable environment into account and proposes an action that tries
        to trigger an effect based on its policy .
        Agents' actions are the internal driver of state evolution. Or in plain words, agents act to change the
        system in order to achieve its goal.
        """
        raise NotImplementedError()


EntityType = TypeVar("EntityType", bound=Entity)
StateType = TypeVar("StateType")
AgentType = TypeVar("AgentType", bound=Agent)
ResourceType = TypeVar("ResourceType", bound=Resource)


class Relation(Generic[EntityType, StateType]):
    """
    A Relation defines the connection between entities. This implies the possible action can be proposed, and the involved entities.
    A Relation also attaches to a set of rule s that need to be considered while proposing an effect involving the relation.
    """

    def __init__(
        self,
        from_entity: EntityType,
        to_entity: EntityType,
    ):
        self._from_entity = from_entity
        self._to_entity = to_entity

    @property
    def from_entity(self) -> EntityType:
        return self._from_entity

    @property
    def to_entity(self) -> EntityType:
        return self._to_entity


RelationType = TypeVar("RelationType", bound=Relation)


# TODO
class SystemSnapshot(Generic[EntityType, RelationType]):
    def __init__(self, vertices: Set[EntityType], relations: Set[RelationType]):
        self.vertices = vertices
        self.relations = relations

    @property
    @abstractmethod
    def vertices(self) -> Set[EntityType]:
        return self.vertices

    @property
    @abstractmethod
    def relations(self) -> Set[RelationType]:
        return self.relations


class Effect:
    """
        An effect is a proposed modification of the current state. It can only do the following:
    Change internal state of entities
    Add/remove relations
    Add/remove entities
    For example, a movement of a train is an effect that proposes the following changes
    Remove the relation between the current track and the train
    Add a new relation to the new track it wants to travel to
    A breakdown of a train or an agent is equivalent to Change internal state from operating to
    malfunction
    """

    pass


EffectsType = TypeVar("EffectsType", bound=Effect)


class Arbiter:
    """
        Arbiter takes a proposed effect and the set of rules involved for the proposal, decide whether
    to accept or reject the effect .
    An arbiter works in 2 levels
    Local : checks the rules regarding the change of an entity's internal state without considering
    the outside world
    Global : checks the rules regarding the relation between entities.
    Arbiter can also add new effect to the proposed effects to complete the state change. For
    example, a train proposes to move from one track to another. If these two tracks involves a turn, the
    arbiter adds another effect to change the train's internal state "direction" to the direction of the
    new track.
    """

    @abstractmethod
    def check_rules(self, effects: List[Effect]) -> List[Effect]:
        raise NotImplementedError()


class Propagator:
    """
        Given the valid effects , a propagator updates the system state (entities and relations). Note that if
    multiple effects are propagated at the same time, the propagator needs to handle potential conflicts
    between the effects.
    """

    @abstractmethod
    def propagate(self, effects: List[Effect]):
        raise NotImplementedError()


@dataclass()
class SystemState(Generic[AgentType, RelationType, ResourceType]):
    agents: list[AgentType]
    relations: list[RelationType]
    resources: list[ResourceType]

    @abstractmethod
    def actions_to_effects(self, actions):
        raise NotImplementedError()

    @abstractmethod
    def pull_actions(self):
        raise NotImplementedError()

    def relations_by_entity(self):
        relations_by_entity = defaultdict(list)
        for relation in self.relations:
            relations_by_entity[relation.from_entity].append(relation)
        return relations_by_entity


class GenEnvSimulation:

    def __init__(self, propagator: Propagator, state: SystemState, arbiter: Arbiter):
        self.propagator = propagator
        self.state = state
        self.arbiter = arbiter
        self.queue = list()

    def addEffects(self, effects: List[Effect]):
        self.queue.extend(effects)

    def run(self):
        dones = self.step()

        while not (all(dones.values())):
            self.queue.clear()
            dones = self.step()

    def step(self):
        self.addEffects(self.state.actions_to_effects(self.state.pull_actions()))
        # TODO malfuntion/env
        self.queue = self.arbiter.check_rules(self.queue)
        dones = self.propagator.propagate(self.queue)
        return dones
