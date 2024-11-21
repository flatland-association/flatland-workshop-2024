from next_flatland.network.abc.link import EndNodeIdPair
from next_flatland.network.abc.node import NodeId, ThreeDCoordinates
from next_flatland.network.state_network.link import StateLink, StateLinkType
from next_flatland.network.state_network.network import StateNetwork
from next_flatland.network.state_network.node import StateNode, StateNodeType

RESOURCE_Z = -100
NODE_DISTANCE = 100
TRACK_LOW_Y = 0
TRACK_HIGH_Y = 50


def create_example_rail_network() -> StateNetwork:
    """
         6 7
         - - 
       /     \ 
    - -  - -  - -
    0 1  2 3  4 5
    """

    nodes_to_add: list[StateNode] = []
    links_to_add: list[tuple[EndNodeIdPair, StateLink]] = []

    resources = [(str(i), (i * NODE_DISTANCE, TRACK_LOW_Y)) for i in range(5)]
    resources.extend(
        [(str(i), ((i - 4) * NODE_DISTANCE, TRACK_HIGH_Y)) for i in range(6, 8)]
    )

    for resource_index, (x, y) in resources:

        forward_node_id = NodeId(resource_index + "_forward")
        backward_node_id = NodeId(resource_index + "_backward")
        resource_node_id = NodeId(resource_index)
        nodes_to_add.append(
            StateNode(
                id=forward_node_id,
                coordinates=ThreeDCoordinates(x=x, y=y, z=0),
                node_type=StateNodeType.INFRASTRUCTURE,
            )
        )
        nodes_to_add.append(
            StateNode(
                id=backward_node_id,
                coordinates=ThreeDCoordinates(x=x, y=y, z=0),
                node_type=StateNodeType.INFRASTRUCTURE,
            )
        )
        nodes_to_add.append(
            StateNode(
                id=NodeId(resource_index),
                coordinates=ThreeDCoordinates(x=x, y=y, z=RESOURCE_Z),
                node_type=StateNodeType.RESOURCE,
            )
        )
        links_to_add.extend(
            [
                (
                    EndNodeIdPair((forward_node_id, resource_node_id)),
                    StateLink(
                        link_type=StateLinkType.ALLOCATION,
                    ),
                ),
                (
                    EndNodeIdPair((resource_node_id, backward_node_id)),
                    StateLink(
                        link_type=StateLinkType.ALLOCATION,
                    ),
                ),
            ]
        )

    # Add forward and backward links between infrastructure nodes
    # Bottom track (0 -> 1 -> 2 -> 3 -> 4 -> 5)
    for i in range(5):
        current_forward = NodeId(f"{i}_forward")
        next_forward = NodeId(f"{i + 1}_forward")
        current_backward = NodeId(f"{i + 1}_backward")
        previous_backward = NodeId(f"{i}_backward")

        # Link consecutive forward nodes
        links_to_add.append(
            (
                EndNodeIdPair((current_forward, next_forward)),
                StateLink(link_type=StateLinkType.TRANSITION),
            )
        )

        # Link consecutive backward nodes
        links_to_add.append(
            (
                EndNodeIdPair((current_backward, previous_backward)),
                StateLink(link_type=StateLinkType.TRANSITION),
            )
        )

    # Top track (6 -> 7)
    links_to_add.append(
        (
            EndNodeIdPair((NodeId("6_forward"), NodeId("7_forward"))),
            StateLink(link_type=StateLinkType.TRANSITION),
        )
    )
    links_to_add.append(
        (
            EndNodeIdPair((NodeId("7_backward"), NodeId("6_backward"))),
            StateLink(link_type=StateLinkType.TRANSITION),
        )
    )

    # Diagonal connections (1 <-> 6, 4 <-> 7)
    links_to_add.append(
        (
            EndNodeIdPair((NodeId("1_forward"), NodeId("6_forward"))),
            StateLink(link_type=StateLinkType.TRANSITION),
        )
    )
    links_to_add.append(
        (
            EndNodeIdPair((NodeId("6_backward"), NodeId("1_backward"))),
            StateLink(link_type=StateLinkType.TRANSITION),
        )
    )
    links_to_add.append(
        (
            EndNodeIdPair((NodeId("4_forward"), NodeId("7_forward"))),
            StateLink(link_type=StateLinkType.TRANSITION),
        )
    )
    links_to_add.append(
        (
            EndNodeIdPair((NodeId("7_backward"), NodeId("4_backward"))),
            StateLink(link_type=StateLinkType.TRANSITION),
        )
    )

    # Add the nodes and links to the system state network
    system_state_network = StateNetwork.create_new(nodes_to_add, links_to_add)
    return system_state_network


if __name__ == "__main__":
    network = create_example_rail_network()
    network.debug_plot()
