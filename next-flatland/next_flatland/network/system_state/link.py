from enum import unique

from network.abc import LinkABC
from network.abc.link import BaseLinkType


@unique
class SSLinkType(BaseLinkType):
    OCCUPATION = 0
    RESERVATION = 1
    ALLOCATION = 2


class SSLink(LinkABC):
    link_type: SSLinkType
