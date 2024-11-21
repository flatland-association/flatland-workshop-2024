from __future__ import annotations

import json
from abc import ABC
from collections.abc import Iterable
from dataclasses import asdict, dataclass, is_dataclass
from types import UnionType
from typing import (Any, Generic, Iterator, Literal, NewType, Type, TypeVar,
                    Union, get_args, get_origin, get_type_hints)

import igraph

from next_flatland.network.abc import LinkABC, NodeABC
from next_flatland.network.abc.debug import debug_plot
from next_flatland.network.abc.link import BaseLinkType, EndNodeIdPair
from next_flatland.network.abc.node import BaseNodeType, NodeId, NodeIndex

NodeT = TypeVar("NodeT", bound=NodeABC)
LinkT = TypeVar("LinkT", bound=LinkABC)
NodeTypeT = TypeVar("NodeTypeT", bound=BaseNodeType)
LinkTypeT = TypeVar("LinkTypeT", bound=BaseLinkType)
Self = TypeVar("Self", bound="ImmutableNetworkABC")
LinkIndex = NewType("LinkIndex", int)

VERTEX_NAME_IN_GRAPH: Literal["name"] = "name"  # is given by igraph library
assert (
    VERTEX_NAME_IN_GRAPH == "name"
)  # is given by igraph library and cannot be changed


@dataclass(init=False, frozen=True)
class ImmutableNetworkABC(Generic[NodeT, LinkT, NodeTypeT, LinkTypeT], ABC):
    _underlying_digraph: igraph.Graph
    node_attribute_name: str = "node"
    link_attribute_name: str = "link"
    _vertex_name_in_graph: str = VERTEX_NAME_IN_GRAPH

    def __init__(self, _underlying_digraph: igraph.Graph) -> None:
        if not _underlying_digraph.is_directed():
            raise TypeError("Only directed graphs allowed")
        object.__setattr__(self, "_underlying_digraph", _underlying_digraph)

    @property
    def n_count(self) -> int:
        return self._underlying_digraph.vcount()

    @property
    def l_count(self) -> int:
        return self._underlying_digraph.ecount()

    @property
    def node_ids(self) -> list[NodeId]:
        if self._underlying_digraph.vcount() == 0:
            return []
        return self._underlying_digraph.vs[self._vertex_name_in_graph]

    @property
    def all_edges(self) -> igraph.EdgeSeq:
        return self._underlying_digraph.es

    @property
    def end_node_id_pair_iterator(self) -> Iterator[EndNodeIdPair]:
        return (
            EndNodeIdPair(
                (
                    es.source_vertex[self._vertex_name_in_graph],
                    es.target_vertex[self._vertex_name_in_graph],
                )
            )
            for es in self._underlying_digraph.es
        )  # noqa

    @property
    def edge_tuple_iterator(self) -> Iterator[tuple[NodeIndex, NodeIndex]]:
        return (es.tuple for es in self._underlying_digraph.es)

    @property
    def all_links(self) -> list[LinkT]:
        if self._underlying_digraph.vcount() == 0:
            return []
        return self._underlying_digraph.es[self.link_attribute_name]

    @property
    def all_nodes(self) -> list[NodeT]:
        if self._underlying_digraph.vcount() == 0:
            return []
        return self._underlying_digraph.vs[self.node_attribute_name]

    def node_index_by_name(self, node_name: NodeId) -> NodeIndex:
        return self._underlying_digraph.vs.find(node_name).index

    def node_name_by_index(self, node_index: NodeIndex) -> NodeId:
        return self._underlying_digraph.vs[self._vertex_name_in_graph][node_index]

    def node_by_index(self, node_index: NodeIndex) -> NodeT:
        return self._underlying_digraph.vs[self.node_attribute_name][node_index]

    def node_by_id(self, n_id: NodeId) -> NodeT:
        return self.node_by_index(self.node_index_by_name(n_id))

    def link_index_by_source_target(
        self, source: NodeId | NodeIndex, target: NodeId | NodeIndex
    ) -> LinkIndex:
        return self._underlying_digraph.get_eid(source, target)

    def link_source_target_by_index(
        self, idx: LinkIndex
    ) -> tuple[NodeIndex, NodeIndex]:
        return self._underlying_digraph.es[idx].tuple

    def link_index_by_end_node_id_pair(self, end_nodes: EndNodeIdPair) -> LinkIndex:
        return self._underlying_digraph.get_eid(end_nodes[0], end_nodes[1])

    def edge_by_index(self, idx: LinkIndex) -> igraph.Edge:
        return self._underlying_digraph.es.find(idx)

    def edge_by_source_target(
        self, source: NodeId | NodeIndex, target: NodeId | NodeIndex
    ) -> igraph.Edge:
        return self._underlying_digraph.es.find(_from=source, _to=target)

    def link_by_index(self, idx: LinkIndex) -> LinkT:
        return self._underlying_digraph.es[self.link_attribute_name][idx]

    def link_by_source_target(
        self, source_id: NodeId | NodeIndex, target_id: NodeId | NodeIndex
    ) -> LinkT:
        return self.link_by_index(
            self.link_index_by_source_target(source_id, target_id)
        )

    def link_by_end_node_id_pair(self, end_nodes: EndNodeIdPair) -> LinkT:
        return self.link_by_index(
            self.link_index_by_source_target(end_nodes[0], end_nodes[1])
        )

    def link_end_node_id_pair_by_index(self, index: LinkIndex) -> EndNodeIdPair:
        edge = self.edge_by_index(index)
        return EndNodeIdPair(
            (
                edge.source_vertex[self._vertex_name_in_graph],
                edge.target_vertex[self._vertex_name_in_graph],
            )
        )

    def link_by_end_node_iterator(self) -> Iterator[tuple[EndNodeIdPair, LinkT]]:
        return zip(self.end_node_id_pair_iterator, self.all_links)

    def link_by_tuple_iterator(
        self,
    ) -> Iterator[tuple[tuple[NodeIndex, NodeIndex], LinkT]]:
        return zip((es.tuple for es in self._underlying_digraph.es), self.all_links)

    def in_degrees(self) -> list[int]:
        return self._underlying_digraph.indegree()

    def out_degrees(self) -> list[int]:
        return self._underlying_digraph.outdegree()

    def degrees(self) -> list[int]:
        return self._underlying_digraph.degree()

    def incident_links_per_node(
        self, idx: NodeId | NodeIndex, mode: Literal["in", "out", "all"] = "all"
    ) -> list[LinkT]:
        return [
            self._underlying_digraph.es[i][self.link_attribute_name]
            for i in self._underlying_digraph.incident(idx, mode)
        ]

    def incident_link_idx_per_node(
        self, idx: NodeId | NodeIndex, mode: Literal["in", "out", "all"] = "all"
    ) -> list[LinkIndex]:
        return self._underlying_digraph.incident(vertex=idx, mode=mode)

    def neighbors(
        self, idx: NodeId | NodeIndex, mode: Literal["in", "out", "all"] = "all"
    ) -> list[NodeT]:
        return self._underlying_digraph.vs[
            self._underlying_digraph.neighbors(vertex=idx, mode=mode)
        ][self.node_attribute_name]

    @classmethod
    def create_empty(cls: Type[Self]) -> Self:
        return cls(igraph.Graph(directed=True))

    @property
    def shallow_copy(self: Self) -> Self:
        return self.__class__(self._underlying_digraph.copy(), self.time_context)

    def nodes_by_indexes(self, indexes: Iterable[NodeIndex]) -> list[NodeT]:
        return self._underlying_digraph.vs.select(indexes)[self.node_attribute_name]

    def nodes_by_names(self, names: Iterable[NodeId]) -> list[NodeT]:
        return self._underlying_digraph.vs.select(name_in=names)[
            self.node_attribute_name
        ]

    def links_by_indexes(self, indexes: Iterable[LinkIndex]) -> list[LinkT]:
        return self._underlying_digraph.es.select(indexes)[self.link_attribute_name]

    def weak_components(self: Self) -> tuple[Self, ...]:
        return tuple(
            self.__class__(graph, self.time_context)
            for graph in self._underlying_digraph.components(mode="weak").subgraphs()
        )

    def debug_plot(
        self, file_name: str | None = None, with_labels: bool = True
    ) -> None:
        debug_plot(self._underlying_digraph, with_labels, file_name)


class ImmutableNetworkEncoder(json.JSONEncoder):
    def default(self, o) -> Any:
        if isinstance(o, igraph.Graph):
            igraph_dict = serialize_igraph(o)
            igraph_dict["edge_attrs"] = {
                str(k): v for k, v in igraph_dict["edge_attrs"].items()
            }
            igraph_dict["__class__"] = "igraph.Graph"
            return igraph_dict
        if isinstance(o, NodeABC | LinkABC):
            data = asdict(o)
            data["__class__"] = f"{o.__class__.__module__}.{o.__class__.__name__}"
            return data
        if isinstance(o, ImmutableNetworkABC):
            data = asdict(o)
            del data["node_attribute_name"]
            del data["link_attribute_name"]
            del data["_vertex_name_in_graph"]
            data["__class__"] = f"{o.__class__.__module__}.{o.__class__.__name__}"
            return data
        if isinstance(o, set | frozenset):
            return list(o)
        return super().default(o)


class ImmutableNetworkDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(dct: dict[str, Any]) -> Any:
        if "__class__" in dct:
            class_name: str = dct["__class__"]
            del dct["__class__"]

            if class_name == "igraph.Graph":
                return deserialize_igraph(dct)

            module_name, class_name = class_name.rsplit(".", 1)
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            return dataclass_from_dict(cls, dct)

        return dct


def dataclass_from_dict(cls: type, data: dict[str, Any] | Any) -> Any:
    # handle type unions
    if get_origin(cls) is Union or get_origin(cls) is UnionType:
        for arg in get_args(cls):
            try:
                return dataclass_from_dict(arg, data)
            except Exception as e:
                print(f"Failed to convert {data} to {arg}: {e}", flush=True)
        raise ValueError(f"Could not convert {data} to any of {get_args(cls)}")

    # handle types defined with NewType
    if hasattr(cls, "__supertype__"):
        supertype = cls.__supertype__
        return cls(dataclass_from_dict(supertype, data))

    # handle non dataclass types
    if not is_dataclass(cls):
        if isinstance(data, igraph.Graph) or data is None:
            return data
        else:
            return cls(data)

    field_types = get_type_hints(cls)
    result = {}
    for f in field_types:
        if f not in data:
            continue
        # catch ellipsis type hints
        args = get_args(field_types[f])
        if len(args) > 0 and args[-1] is Ellipsis:
            # This is a variadic tuple, convert each list item into the appropriate type
            elem_type = args[0]  # The type of the tuple's elements
            result[f] = tuple(dataclass_from_dict(elem_type, item) for item in data[f])
        else:
            # Handle non-ellipsis types normally
            result[f] = (
                dataclass_from_dict(field_types[f], data[f]) if f in data else None
            )
    return cls(**result)


def serialize_igraph(graph: igraph.Graph) -> dict[str, Any]:
    return {
        "node_count": graph.vcount(),
        "edges": graph.get_edgelist(),
        "attributes": {key: graph[key] for key in graph.attributes()},
        "vertex_attrs": {v.index: v.attributes() for v in graph.vs},
        "edge_attrs": {e.tuple: e.attributes() for e in graph.es},
        "is_directed": graph.is_directed(),
    }


def deserialize_igraph(data: dict[str, Any]) -> igraph.Graph:
    edge_attr_keys = (
        next(iter(data["edge_attrs"].values())).keys() if data["edge_attrs"] else []
    )
    edge_attrs = {
        k: [d[k] for d in data["edge_attrs"].values()] for k in edge_attr_keys
    }

    vertex_attr_keys = (
        next(iter(data["vertex_attrs"].values())).keys() if data["vertex_attrs"] else []
    )
    vertex_attrs = {
        k: [d[k] for d in data["vertex_attrs"].values()] for k in vertex_attr_keys
    }

    return igraph.Graph(
        n=data["node_count"],
        edges=data["edges"],
        directed=data["is_directed"],
        graph_attrs=data["attributes"],
        edge_attrs=edge_attrs,
        vertex_attrs=vertex_attrs,
    )
