from enum import unique

from network.abc import NodeABC
from network.abc.node import BaseNodeType, NodeId, ThreeDCoordinates


@unique
class SSNodeType(BaseNodeType):
    RESOURCE = 0
    INFRASTRUCTURE = 1
    AGENT = 2


class SSNode(NodeABC):
    node_type: SSNodeType
    coordinates: ThreeDCoordinates
    id: NodeId
