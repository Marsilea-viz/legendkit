import numpy as np
from matplotlib.collections import CircleCollection
from matplotlib.colors import is_color_like

from legendkit import ListLegend


class CatLegend(ListLegend):
    _sizer = {
        "small": 0.4,
        "medium": 0.7,
        "large": 1.1,
    }

    def __init__(self, colors, labels, size="medium", handle=None, **kwargs):
        if handle is None:
            handle = 'square'

        legend_items = [(handle, name, {'color': c}) for c, name in zip(colors, labels)]

        side = self._sizer[size]

        options = dict(
            frameon=False,
            handleheight=side,
            handlelength=side,
            handletextpad=0.5,
            labelspacing=0.3,
            borderpad=0,
        )
        options = {**options, **kwargs}

        super().__init__(legend_items=legend_items,
                         **options)


class SizeLegend(ListLegend):
    """A special class use to create legend that represent size"""

    def __init__(self, sizes, array=None, colors=None, labels=None,
                 num=5, trim_min=True, dtype=None, ascending=True,
                 **kwargs):

        self._trim_min = trim_min
        self.num = num

        if not isinstance(sizes, np.ndarray):
            sizes = np.array(sizes)
        # smin, smax = np.nanmin(sizes), np.nanmax(sizes)
        # if dtype is None:
        #     dtype = sizes.dtype
        # handles_sizes = np.linspace(smin, smax, num=num, dtype=dtype)
        # if trim_min:
        #     handles_sizes = handles_sizes[1::]
        handles_sizes = self._get_linspace(sizes)
        if colors is None:
            self.colors = ['black' for _ in range(num)]
        elif is_color_like(colors):
            self.colors = [colors for _ in range(num)]
        else:
            self.colors = colors
        if (array is None) & (labels is None):
            labels = handles_sizes
        elif array is not None:
            labels = self._get_linspace(array, dtype=dtype)

        size_handles = []
        size_labels = []

        for s, label, color in zip(handles_sizes, labels, self.colors):
            size_handles.append(
                CircleCollection([s], facecolors=color)
            )
            if label is None:
                label = s
            size_labels.append(label)

        if not ascending:
            size_handles = size_handles[::-1]
            size_labels = size_labels[::-1]

        options = dict(
            frameon=False,
            handleheight=1.0,
            handlelength=1.0,
            handletextpad=0.7,
            labelspacing=1,
            borderpad=0,
        )

        options = {**options, **kwargs}

        super().__init__(
            handles=size_handles,
            labels=size_labels,
            **options)

    def _get_linspace(self, sizes, dtype=None):
        if dtype is None:
            dtype = sizes.dtype
        smin, smax = np.nanmin(sizes), np.nanmax(sizes)
        handles_sizes = np.linspace(smin, smax, num=self.num, dtype=dtype)
        if self._trim_min:
            handles_sizes = handles_sizes[1::]
        return handles_sizes
