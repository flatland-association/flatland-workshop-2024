from example.rail_network import RESOURCE_Z, create_example_rail_network
from next_flatland.network.abc.node import ThreeDCoordinates
from next_flatland.network.state_network.network import StateNetwork
from next_flatland.network.state_network.node import StateNode, StateNodeType
from next_flatland.network.state_network import StateLink, StateLinkType
from next_flatland.network.abc.link import EndNodeIdPair
from next_flatland.network.abc.node import NodeId


AGENT_ID_1 = NodeId("a1")
AGENT_ID_2 = NodeId("a2")


FORWARD_0 = NodeId("0_forward")
FORWARD_1 = NodeId("1_forward")
FORWARD_2 = NodeId("2_forward")
FORWARD_3 = NodeId("3_forward")
FORWARD_4 = NodeId("4_forward")
FORWARD_5 = NodeId("5_forward")
FORWARD_6 = NodeId("6_forward")
FORWARD_7 = NodeId("7_forward")

BACKWARD_0 = NodeId("0_backward")
BACKWARD_1 = NodeId("1_backward")
BACKWARD_2 = NodeId("2_backward")
BACKWARD_3 = NodeId("3_backward")
BACKWARD_4 = NodeId("4_backward")
BACKWARD_5 = NodeId("5_backward")
BACKWARD_6 = NodeId("6_backward")
BACKWARD_7 = NodeId("7_backward")


def mock_state(
    occupations: dict[NodeId, NodeId], reservations: dict[NodeId, NodeId]
) -> StateNetwork:

    agent_1 = StateNode(
        id=AGENT_ID_1,
        coordinates=ThreeDCoordinates(x=0, y=10, z=2 * RESOURCE_Z),
        node_type=StateNodeType.AGENT,
    )
    agent_2 = StateNode(
        id=AGENT_ID_2,
        coordinates=ThreeDCoordinates(x=0, y=10, z=2 * RESOURCE_Z),
        node_type=StateNodeType.AGENT,
    )

    links_to_add = []

    for agent, ressource in occupations.items():
        links_to_add.append(
            (
                EndNodeIdPair((agent, ressource)),
                StateLink(link_type=StateLinkType.OCCUPATION),
            )
        )

    for agent, ressource in reservations.items():
        links_to_add.append(
            (
                EndNodeIdPair((agent, ressource)),
                StateLink(link_type=StateLinkType.RESERVATION),
            )
        )

    state = create_example_rail_network()
    state.add_nodes([agent_1, agent_2])
    state.add_links(links_to_add)

    return state


states = []


states.append(
    mock_state(
        occupations={AGENT_ID_1: FORWARD_0, AGENT_ID_2: BACKWARD_5},
        reservations={AGENT_ID_1: FORWARD_1, AGENT_ID_2: BACKWARD_4},
    )
)

states.append(
    mock_state(
        occupations={AGENT_ID_1: FORWARD_1, AGENT_ID_2: BACKWARD_4},
        reservations={AGENT_ID_1: FORWARD_2, AGENT_ID_2: BACKWARD_3},
    )
)

states.append(
    mock_state(
        occupations={AGENT_ID_1: FORWARD_2, AGENT_ID_2: BACKWARD_7},
        reservations={AGENT_ID_1: FORWARD_3, AGENT_ID_2: BACKWARD_6},
    )
)
