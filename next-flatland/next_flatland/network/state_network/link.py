from enum import unique

from next_flatland.network.abc import LinkABC
from next_flatland.network.abc.link import BaseLinkType


@unique
class StateLinkType(BaseLinkType):
    OCCUPATION = 0
    RESERVATION = 1
    ALLOCATION = 2
    TRANSITION = 3


class StateLink(LinkABC):
    link_type: StateLinkType
