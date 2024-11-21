from __future__ import annotations

from abc import ABC
from collections.abc import Collection
from dataclasses import dataclass
from enum import IntEnum, unique
from statistics import mean
from typing import NewType, Type, TypeVar

NodeId = NewType("NodeId", str)
ClusterId = NodeId
EndNodeIds = NewType("EndNodeIds", tuple[NodeId, ...])
NodeIndex = NewType("NodeIndex", int)

T = TypeVar("T", bound="ThreeDCoordinates")


@dataclass(frozen=True, slots=True)
class ThreeDCoordinates:
    x: float
    y: float
    z: float

    def __add__(self, other: ThreeDCoordinates) -> ThreeDCoordinates:
        return ThreeDCoordinates(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: ThreeDCoordinates) -> ThreeDCoordinates:
        return ThreeDCoordinates(self.x - other.x, self.y - other.y, self.z - other.z)

    @classmethod
    def create_mean_location_coordinates(
        cls: Type[T], coordinates: Collection[ThreeDCoordinates]
    ) -> T:
        return cls(
            mean(c.x for c in coordinates),
            mean(c.y for c in coordinates),
            mean(c.z for c in coordinates),
        )


@unique
class BaseNodeType(IntEnum):
    pass


@dataclass(frozen=True, slots=True)
class NodeABC(ABC):
    id: NodeId
    coordinates: ThreeDCoordinates
    node_type: BaseNodeType


def node_distance(n_1: NodeABC, n_2: NodeABC) -> float:
    a, b = n_1.coordinates, n_2.coordinates
    if a.z == 0 == b.z:
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2) ** 0.5
