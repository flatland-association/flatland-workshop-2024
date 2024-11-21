from next_flatland.network.abc import MutableNetworkABC
from next_flatland.network.state_network.link import StateLink, StateLinkType
from next_flatland.network.state_network.node import StateNode, StateNodeType


class StateNetwork(
    MutableNetworkABC[StateNode, StateLink, StateNodeType, StateLinkType]
):

    def reduce_to_agent_network(self) -> "StateNetwork":
        copied = self.shallow_copy
        copied.delete_nodes_without_type(frozenset((StateNodeType.AGENT,)))
        return copied

    def reduce_to_resource_network(self) -> "StateNetwork":
        copied = self.shallow_copy
        copied.delete_nodes_without_type(frozenset((StateNodeType.RESOURCE,)))
        return copied

    def reduce_to_infrastructure_network(self) -> "StateNetwork":
        copied = self.shallow_copy
        copied.delete_nodes_without_type(frozenset((StateNodeType.INFRASTRUCTURE,)))
        return copied

    def reduce_to_resource_and_infrastructure_network(self) -> "StateNetwork":
        copied = self.shallow_copy
        copied.delete_nodes_without_type(
            frozenset((StateNodeType.RESOURCE, StateNodeType.INFRASTRUCTURE))
        )
        return copied

    def reduce_to_infrastructure_and_agent_network(self) -> "StateNetwork":
        copied = self.shallow_copy
        copied.delete_nodes_without_type(
            frozenset((StateNodeType.INFRASTRUCTURE, StateNodeType.AGENT))
        )
        return copied
