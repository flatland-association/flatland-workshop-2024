from next_flatland.network.abc import MutableNetworkABC
from next_flatland.network.state_network.link import StateLink, StateLinkType
from next_flatland.network.state_network.node import StateNode, StateNodeType


class StateNetwork(
    MutableNetworkABC[StateNode, StateLink, StateNodeType, StateLinkType]
):
    pass
