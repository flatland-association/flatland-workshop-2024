from enum import unique

from next_flatland.network.abc import NodeABC
from next_flatland.network.abc.node import (BaseNodeType, NodeId,
                                            ThreeDCoordinates)


@unique
class StateNodeType(BaseNodeType):
    RESOURCE = 0
    INFRASTRUCTURE = 1
    AGENT = 2


class StateNode(NodeABC):
    node_type: StateNodeType
    coordinates: ThreeDCoordinates
    id: NodeId
