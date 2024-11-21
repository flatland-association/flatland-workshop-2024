from __future__ import annotations

from dataclasses import dataclass, field
from collections import defaultdict
import random
from typing import Dict, List, Set, Any, TypeVar
from example.rail_network import AGENT_Z, create_example_rail_network
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

from next_flatland.network.abc.immutablenetwork_abc import LinkIndex
from next_flatland.network.abc.link import EndNodeIdPair
from next_flatland.network.abc.node import NodeId, ThreeDCoordinates
from next_flatland.network.state_network.link import StateLink, StateLinkType
from next_flatland.network.state_network.network import StateNetwork
from next_flatland.network.state_network.node import StateNode, StateNodeType
from next_flatland.network.state_network.plot_3d import (
    add_state_network_in_3d_to_figure,
)


@dataclass()
class Action:
    pass


@dataclass()
class MoveAction(Action):
    agent: StateNode
    destination: StateNode

    def __post_init__(self):
        assert self.agent.node_type == StateNodeType.AGENT
        assert self.destination.node_type == StateNodeType.INFRASTRUCTURE


@dataclass()
class NoAction(Action):
    pass


@dataclass()
class MoveEffect(Effect):
    edge_to_add: EndNodeIdPair
    edge_to_remove: EndNodeIdPair


@dataclass()
class AddEdge(Effect):
    edge: EndNodeIdPair


@dataclass()
class RemoveEdge(Effect):
    edge: EndNodeIdPair


@dataclass
class RandomPolicy:
    def propose_next_position(
        self, agent_id: NodeId, state: StateNetwork
    ) -> StateNode | None:
        # this only works if the agent doesn't have any reservations (a single occupation)
        current_position = state.neighbors(agent_id, "out")[0]
        possible_next_positions = state.neighbors(current_position.id, "out")
        possible_next_positions = list(
            filter(
                lambda x: x.node_type == StateNodeType.INFRASTRUCTURE,
                possible_next_positions,
            )
        )
        if not possible_next_positions:
            return None

        return random.choice(list(possible_next_positions))


@dataclass
class TrainAgent(Agent):
    id: int
    policy: RandomPolicy = RandomPolicy()

    def __init__(self, id: int):
        self.id = id

    def act(self, state: StateNetwork) -> Action:
        agent = state.node_by_id(NodeId(f"agent_{self.id}"))
        next_position = self.policy.propose_next_position(agent.id, state)
        if next_position is None:
            return NoAction()

        return MoveAction(agent, next_position)


@dataclass()
class RailArbiter(Arbiter):
    def check_rules(self, state: StateNetwork, effects: list[Effect]) -> list[Effect]:
        valid_effects: list[Effect] = []

        for effect in effects:
            if isinstance(effect, MoveEffect):
                agent_id, curr_infra_id = effect.edge_to_remove
                agent_id, next_infra_id = effect.edge_to_add

                # is transition valid
                valid_transition = next_infra_id in [
                    node.id for node in state.neighbors(curr_infra_id, "out")
                ]
                if not valid_transition:
                    print(f"Invalid transition from {curr_infra_id} to {next_infra_id}")
                    continue

                valid_effects.extend(
                    [
                        AddEdge(edge=effect.edge_to_add),
                        RemoveEdge(edge=effect.edge_to_remove),
                    ]
                )

        return valid_effects


@dataclass
class RailPropagator(Propagator):
    def propagate(
        self, state: StateNetwork, effects: List[Effect]
    ) -> Dict[Agent, bool]:
        """
        Propagates effects by:
        - Validating effect types
        - Updating agent positions
        - Updating rail state relations
        - Tracking completion status
        """
        dones = {"agent": True}
        links_to_add: list[tuple[EndNodeIdPair, StateLink]] = []
        links_to_remove: list[LinkIndex] = []

        for effect in effects:
            if isinstance(effect, AddEdge):
                links_to_add.append(
                    (effect.edge, StateLink(link_type=StateLinkType.OCCUPATION))
                )
            if isinstance(effect, RemoveEdge):
                links_to_remove.append(
                    state.link_index_by_end_node_id_pair(effect.edge)
                )
            dones["agent"] = False

        state.delete_links(links_to_remove)
        state.add_links(links_to_add)

        return dones


@dataclass(slots=True)
class RailState(SystemState):
    state: StateNetwork
    agents: list[TrainAgent]

    def __init__(self, state: StateNetwork):
        self.state = state
        self.agents = []

    def actions_to_effects(self, actions: list[Action]) -> list[Effect]:
        effects = []
        for action in actions:
            if isinstance(action, MoveAction):
                agent_id = action.agent.id
                curr_infra_id = self.state.neighbors(action.agent.id, "out")[0].id
                next_infra_id = action.destination.id
                effects.append(
                    MoveEffect(
                        edge_to_add=EndNodeIdPair((agent_id, next_infra_id)),
                        edge_to_remove=EndNodeIdPair((agent_id, curr_infra_id)),
                    )
                )

        return effects

    def pull_actions(self):
        actions = []
        for agent in self.agents:
            actions.append(agent.act(self.state))
        return actions

    def add_agent_to_network(self, agent: TrainAgent, infrastructure_id: NodeId):
        self.agents.append(agent)
        agent_node_id = NodeId(f"agent_{agent.id}")
        self.state.add_nodes(
            [
                StateNode(
                    id=agent_node_id,
                    node_type=StateNodeType.AGENT,
                    coordinates=ThreeDCoordinates(x=agent.id * 10, y=20, z=AGENT_Z),
                )
            ]
        )
        self.state.add_links(
            [
                (
                    EndNodeIdPair((agent_node_id, infrastructure_id)),
                    StateLink(link_type=StateLinkType.OCCUPATION),
                )
            ]
        )


# Example usage
if __name__ == "__main__":
    rail_network = create_example_rail_network()
    agents = [TrainAgent(id=i) for i in range(2)]
    rail_state = RailState(state=rail_network)
    rail_state.add_agent_to_network(agents[0], NodeId("0_forward"))
    rail_state.add_agent_to_network(agents[1], NodeId("5_backward"))
    add_state_network_in_3d_to_figure(rail_state.state).show()

    rail_arbiter = RailArbiter()
    rail_propagator = RailPropagator()

    # Create and run simulation
    simulation = GenEnvSimulation(
        propagator=rail_propagator, state=rail_state, arbiter=rail_arbiter
    )

    simulation.run()
