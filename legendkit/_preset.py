import numpy as np
from matplotlib.collections import CircleCollection

from legendkit import ListLegend


class CatLegend(ListLegend):
    _sizer = {
        "small": 0.4,
        "medium": 0.7,
        "large": 1.0,
    }

    def __init__(self, colors, labels, size="small", handle=None, **kwargs):
        if handle is None:
            handle = 'square'

        legend_items = [(handle, name, {'color': c}) for c, name in zip(colors, labels)]

        side = self._sizer[size]

        super().__init__(legend_items=legend_items,
                         handleheight=side,
                         handlelength=side,
                         handletextpad=0.5,
                         labelspacing=0.2,
                         **kwargs)


class SizeLegend(ListLegend):
    """A special class use to create legend that represent size"""

    def __init__(self, sizes, colors=None, labels=None, num=5, forceint=True, ascending=True, **kwargs):

        smin, smax = np.nanmin(sizes), np.nanmax(sizes)
        dtype = int if forceint else float
        handles_sizes = np.linspace(smin, smax, num=num, dtype=dtype)
        if colors is None:
            colors = ['black' for _ in range(num)]
        if labels is None:
            labels = [None for _ in range(num)]

        size_handles = []
        size_labels = []

        for s, label, color in zip(handles_sizes, labels, colors):
            size_handles.append(
                CircleCollection([s], facecolors=color)
            )
            if label is None:
                label = s
            size_labels.append(label)

        if not ascending:
            size_handles = size_handles[::-1]
            size_labels = size_labels[::-1]

        super().__init__(handles=size_handles, labels=size_labels, **kwargs)
