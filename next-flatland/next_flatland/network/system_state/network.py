from network.abc import MutableNetworkABC
from network.system_state.link import SSLink, SSLinkType
from network.system_state.node import SSNode, SSNodeType


class SSNetwork(MutableNetworkABC[SSNode, SSLink, SSNodeType, SSLinkType]):
    pass
