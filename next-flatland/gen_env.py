from abc import abstractmethod, ABCMeta
from collections import defaultdict
from typing import Set, Generic, TypeVar, Any, List, Dict

import numpy as np
from examples.custom_observation_example_02_SingleAgentNavigationObs import SingleAgentNavigationObs
from flatland.core.grid.grid4_utils import get_new_position
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_env_action import RailEnvActions
from flatland.envs.rail_generators import sparse_rail_generator
from flatland.utils.rendertools import RenderTool


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


class Relation(Generic[EntityType, StateType]):
    """
    A Relation defines the connection between entities. This implies the possible action can be proposed, and the involved entities.
    A Relation also attaches to a set of rule s that need to be considered while proposing an effect involving the relation.
    """

    def __init__(self, fromEntity: EntityType, toEntity: EntityType, ):
        self._fromEntity = fromEntity
        self._toEntity = toEntity

    @property
    def fromEntity(self) -> EntityType:
        return self._fromEntity

    @property
    def toEntity(self) -> EntityType:
        return self._toEntity


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


class Effect():
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


class Arbiter():
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


class Propagator():
    """
    Given the valid effects , a propagator updates the system state (entities and relations). Note that if
multiple effects are propagated at the same time, the propagator needs to handle potential conflicts
between the effects.
    """

    @abstractmethod
    def propagate(self, effects: List[Effect]):
        raise NotImplementedError()


class SystemState:

    @abstractmethod
    def actionsToEffects(self, action_dict):
        raise NotImplementedError()

    @abstractmethod
    def pullActions(self):
        raise NotImplementedError()


class GenEnvSimulation():

    def __init__(self,
                 propagator: Propagator,
                 state: SystemState,
                 arbiter: Arbiter
                 ):
        self.propagator = propagator
        self.state = state
        self.arbiter = arbiter
        self.queue = list()

    def addEffects(self, effects: List[Effect]):
        self.queue.extend(effects)

    def run(self):
        dones = self.step()

        while (not (all(dones.values()))):
            self.queue.clear()
            dones = self.step()

    def step(self):
        self.addEffects(self.state.actionsToEffects(self.state.pullActions()))
        # TODO malfuntion/env
        self.queue = self.arbiter.check_rules(self.queue)
        dones = self.propagator.propagate(self.queue)
        return dones


class RailEnvSystemStateWrapper(SystemState):
    def __init__(self, env: RailEnv):
        self.env = env

    def pullActions(self):
        action_dict: Dict[int, RailEnvActions] = {}
        for a in range(self.env.get_num_agents()):
            action = np.random.randint(0, 5)
            action_dict[a] = action
        return action_dict

    def actionsToEffects(self, action_dict):
        return [action_dict]


class RailEnvPropagatorWrapper(Propagator):
    def __init__(self, env: RailEnv, render_mode="rgb_array"):
        self.env = env
        self.render_mode = render_mode
        self.env_renderer = RenderTool(env)

    def propagate(self, action_dict):
        obs, rews, dones, infos = self.env.step(action_dict[0])
        if self.render_mode is not None:
            # We render the initial step and show the obsered cells as colored boxes
            self.env_renderer.render_env(show=True, frames=True, show_observations=True, show_predictions=False)
        print(dones)
        return dones


class RailEnvArbiterWrapper(Arbiter):
    def __init__(self, env: RailEnv):
        self.env = env

    def check_rules(self, effects):
        return effects


class RailPropagator(Propagator):
    pass


# TODO malfunctions
# TODO agent speeds, timetables etc.
# TODO stations?
# TODO lines?
class RailState(SystemState):

    # TODO super call -> generalise resources, objects, relations....
    def __init__(self, cells, transitions, num_agents, agent_minimum_running_time):
        # vertices
        self.cells = cells

        # resource-resource relations
        self.transitions = transitions

        # agent-resource relations
        self.agent_cell_relations = {}  # agent -> cell

        # agent internal states
        self.num_agents = num_agents
        self.agent_cell_ticks = {}  # agent -> Optional[int]
        self.agent_minimum_running_time = agent_minimum_running_time  # agent -> int

    @staticmethod
    def fromRailEnv(env: RailEnv) -> "RailState":
        trans = defaultdict(lambda: [])
        cells = set()
        for row in range(env.height):
            for col in range(env.width):
                cell_connected = False
                for direction in range(4):
                    transitions = env.rail.get_transitions(row, col, direction)
                    for neigh_direction, is_valid in enumerate(transitions):
                        if is_valid:
                            neighbor = get_new_position((row, col), neigh_direction)
                            cell_connected = True
                            trans[(row, col, direction)].append((*neighbor, neigh_direction))
                    if cell_connected:
                        cells.add((row, col, direction))
        return RailState(cells, trans, env.get_num_agents(), {i: env.agents[i].speed_counter.max_count for i in range(env.get_num_agents())})

    def actionsToEffects(self, action_dict):
        # TODO update positions and ticks, reset ticks to 0 when moving to next cell, no ticks = not entered, ticks but no position = exited, ticks + position = in grid/active
        raise NotImplementedError()

    def pullActions(self):
        # TODO random policy for all active agents
        # TODO generalize agent policy
        raise NotImplementedError()


class RailArbiter(Arbiter):
    pass


class RailEnvSimulationVerifier(GenEnvSimulation):
    def __init__(self,
                 propagator: RailPropagator,
                 state: RailState,
                 arbiter: RailArbiter,
                 env: RailEnv
                 ):
        super().__init__(propagator, state, arbiter)
        self.env = env

    def checkSameState(self, env: RailEnv, state: RailState):
        raise NotImplementedError()

    def step(self):
        dones = super().step()
        self.env.step(self.queue[0])
        self.checkSameState(self.env, self.state)
        return dones


if __name__ == '__main__':
    nAgents = 2
    n_cities = 2
    max_rails_between_cities = 2
    max_rails_in_city = 4
    seed = 0
    env = RailEnv(
        width=30,
        height=40,
        rail_generator=sparse_rail_generator(
            max_num_cities=n_cities,
            seed=seed,
            grid_mode=True,
            max_rails_between_cities=max_rails_between_cities,
            max_rail_pairs_in_city=max_rails_in_city
        ),
        line_generator=sparse_line_generator(),
        number_of_agents=nAgents,
        obs_builder_object=SingleAgentNavigationObs()
    )

    if True:
        simulation = GenEnvSimulation(
            propagator=RailEnvPropagatorWrapper(env),
            state=RailEnvSystemStateWrapper(env),
            arbiter=RailEnvArbiterWrapper(env),
        )
        env.reset()
        simulation.run()

    if True:
        env.reset()
        simulation = RailEnvSimulationVerifier(
            propagator=RailPropagator(),
            state=RailState.fromRailEnv(env),
            arbiter=RailArbiter(),
            env=env
        )
        simulation.run()
