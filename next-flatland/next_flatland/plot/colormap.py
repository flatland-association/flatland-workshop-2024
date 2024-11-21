from collections import defaultdict
from typing import Collection, Hashable, NewType

from _plotly_utils.colors import sample_colorscale
from plotly import express as px

ColorMap = NewType("ColorMap", dict[Hashable, str])


def create_colormap(elements: Collection[Hashable], default_color: str | None = None) -> ColorMap:
    count = len(elements)
    colors = sample_colorscale(px.colors.cyclical.Phase, samplepoints=[i / count for i in range(0, count)])
    if default_color is None:
        return ColorMap({key: color for key, color in zip(elements, colors)})
    cmap = defaultdict(lambda: default_color)
    cmap.update(zip(elements, colors))
    return ColorMap(cmap)
