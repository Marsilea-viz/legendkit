from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import _api
from matplotlib.axes import Axes
from matplotlib.collections import Collection, CircleCollection
from matplotlib.colors import is_color_like
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.offsetbox import VPacker, HPacker
from matplotlib.patches import Patch

from ._locs import Locs
from .handles import SquareItem, RectItem, CircleItem, LineItem, BoxplotItem

_handlers = {
    'square': SquareItem,
    'rect': RectItem,
    'circle': CircleItem,
    'line': LineItem,
    'boxplot': BoxplotItem,
}


def _parse_handler(handle, config=None):
    if config is None:
        config = {}
    if isinstance(handle, str):
        return _handlers[handle].__call__(**config)
    else:
        return handle


def _get_legend_handles(axs, legend_handler_map=None):
    """
    Return a generator of artists that can be used as handles in
    a legend.
    """
    handles_original = []
    for ax in axs:
        handles_original += [
            *(a for a in ax._children
              if isinstance(a, (Line2D, Patch, Collection))),
            *ax.containers]
        # support parasite axes:
        if hasattr(ax, 'parasites'):
            for axx in ax.parasites:
                handles_original += [
                    *(a for a in axx._children
                      if isinstance(a, (Line2D, Patch, Collection))),
                    *axx.containers]

    handler_map = Legend.get_default_handler_map()

    if legend_handler_map is not None:
        handler_map = handler_map.copy()
        handler_map.update(legend_handler_map)

    has_handler = Legend.get_legend_handler

    for handle in handles_original:
        label = handle.get_label()
        if label != '_nolegend_' and has_handler(handler_map, handle):
            yield handle


class ListLegend(Legend):
    """This is a modified legend based the original matplotlib class

    Parameters
    ----------
    ax : Axes
        The axes to draw on
    legend_items : list of (handle, label, styles)
    handles : list
        A list of legend handler
    labels : list
        A list of legend labels
    title_loc : {'top', 'bottom', 'left', 'right'}
        The location of title
    alignment : {'left', 'center', 'right'}
        How to align the whole legendbox
    titlepad : float
        The space between title and legend entries
    draw : bool
        Whether to draw the legend
    handler_map
    kwargs :
        Pass to `matplotlib.legend.Legend`


    Examples
    --------

    Create legend from existing axes

    .. plot::
        :context: close-figs

        >>> from legendkit import legend
        >>> x = np.arange(0, 10, 0.1)
        >>> _, ax = plt.subplots()
        >>> ax.plot(x, 2*x + 1, label="Line1")
        >>> ax.plot(x, 5*x + 1, label="Line2")
        >>> legend(ax, title="Title", alignment="left")


    Create legend semantically

    .. plot::
        :context: close-figs

        >>> _, ax = plt.subplots(figsize=(1, 1.5))
        >>> ax.set_axis_off()
        >>> legend(ax, legend_items=[
        ...     # (handle, label, styles)
        ...     ('square', 'Item 1', {'color': '#01949A'}),
        ...     ('circle', 'Item 2', {'facecolor': '#004369',
        ...                           'edgecolor': '#DB1F48'}),
        ...     ('rect', 'Item 3', {'color': '#E5DDC8'}),
        ...     # Or you can have no config at all
        ...     ('line', 'Item 4'),
        ...     ('boxplot', 'Item 5'),
        ... ])

    """

    def __repr__(self):
        return "<ListLegend>"

    def __init__(self,
                 ax=None,
                 legend_items=None,
                 handles=None,
                 labels=None,
                 title_loc="top",  # "top" or "left",
                 alignment="left",
                 titlepad=0.5,
                 draw=True,
                 handler_map=None,
                 loc=None,
                 deviation=0.05,
                 bbox_to_anchor=None,
                 bbox_transform=None,
                 **kwargs,
                 ):
        self._title_loc = title_loc
        self.titlepad = titlepad
        self._is_patch = False

        _api.check_in_list(["top", "bottom", "left", "right"],
                           title_loc=title_loc)

        legend_handles = []
        legend_labels = []

        self._has_axes = ax is not None
        if ax is None:
            ax = plt.gca()

        if (legend_items is None) & (handles is None) & (labels is None):
            # If only axes is provided, we will try to get
            legend_handles, legend_labels = \
                ax.get_legend_handles_labels(handler_map)
        elif legend_items is not None:
            for item in legend_items:
                if len(item) == 2:
                    handle, label = item
                    handle_config = None
                else:
                    item = item[:3]
                    handle, label, handle_config = item
                legend_handles.append(
                    _parse_handler(handle, config=handle_config))
                legend_labels.append(label)
        else:
            # make matplotlib handles this
            legend_handles, legend_labels = handles, labels

        loc, bbox_to_anchor, bbox_transform = \
            Locs().transform(ax, loc, bbox_to_anchor=bbox_to_anchor,
                             bbox_transform=bbox_transform,
                             deviation=deviation)

        default_kwargs = dict(
            loc=loc,
            bbox_to_anchor=bbox_to_anchor,
            bbox_transform=bbox_transform,
            # Make the title bold if user supply no style
            title_fontproperties={'weight': 600},
            handler_map=handler_map,
        )

        final_options = {**default_kwargs, **kwargs}
        super().__init__(ax,
                         handles=legend_handles,
                         labels=legend_labels,
                         **final_options)
        self._alignment = alignment
        self._title_layout()

        if draw:
            # Attach as legend element
            # 1. ax.get_legend() will work
            # 2. legend won't be clipped
            if ax.legend_ is None:
                ax.legend_ = self
            else:
                ax.add_artist(self)

    def _title_layout(self):
        fontsize = self._fontsize
        alignment = self._alignment
        title_loc = self._title_loc
        pad = self.borderpad * fontsize
        sep = self.titlepad * fontsize
        # Positioning of legend title
        # by override the default legend box layout
        packer = HPacker
        children = [self._legend_title_box, self._legend_handle_box]
        if title_loc in ["top", "bottom"]:
            packer = VPacker
        else:
            # if title_loc in ["bottom", "right"]:
            children = children[::-1]
        self._legend_box = packer(pad=pad, sep=sep,
                                  align=alignment, children=children)

        self._legend_box.set_figure(self.figure)
        self._legend_box.axes = self.axes

        # call this to maintain consistent behavior as legend
        self._legend_box.set_offset(self._findoffset)


class CatLegend(ListLegend):
    """Categorical legend with same handles

    This is useful to create legend that share
    the same handle but with different colors

    Parameters
    ----------
    colors : list
        The color for each legend item
    labels : list of str
        The text for each legend item
    handle : optional, str or handle object
    size : str or number, {"small", "medium", "large"}
        The size of legend handle
    kwargs :
        pass to `ListLegend`

    Examples
    --------
    Create a legend easily

    .. plot::
        :context: close-figs

        >>> from legendkit import cat_legend
        >>> _, ax = plt.subplots(figsize=(1, 1))
        >>> ax.set_axis_off()
        >>> cat_legend(ax,
        ...            colors=["red", "blue", "green"],
        ...            labels=["Item 1", "Item 2", "Item 3"],
        ...            )


    """
    _sizer = {
        "small": 0.4,
        "medium": 0.7,
        "large": 1.1,
    }

    def __init__(self,
                 ax=None,
                 colors=None,
                 labels=None,
                 size="medium",
                 handle=None,
                 **kwargs
                 ):
        if handle is None:
            handle = 'square'

        legend_items = [(handle, name, {'color': c}) for c, name in
                        zip(colors, labels)]
        if isinstance(size, str):
            size = self._sizer[size]
        else:
            size = size

        options = dict(
            ax=ax,
            frameon=False,
            handleheight=size,
            handlelength=size,
            handletextpad=0.5,
            labelspacing=0.3,
            borderpad=0,
        )
        options = {**options, **kwargs}

        super().__init__(legend_items=legend_items,
                         **options)


class SizeLegend(ListLegend):
    """Create legend that represent the size of circle

    Parameters
    ----------
    sizes : list
        The sizes array of all circles on the plot
    ax : Axes
        The axes to draw the legend
    labels : list of str
        The labels of the legend
    array : list of number
        The actual data used in plotting, will be used to
        display labels if labels is not specific
    colors : list of color
        The color of the entry
    show_at : list of float, default: [.25, .5, .75, 1.]
        The percentile to show the sizes
    dtype
    handler_kw : mapping
        Use this to control the style of handler
    kwargs : mapping
        Pass to `legendkit.ListLegend`


    Examples
    --------

    .. plot::
        :context: close-figs

        >>> from legendkit import size_legend
        >>> sizes = np.arange(0, 101, 10)
        >>> _, ax = plt.subplots(figsize=(1, 1.5)); ax.set_axis_off()
        >>> size_legend(sizes)

    Change the looking of legends

    .. plot::
        :context: close-figs

        >>> from legendkit import size_legend
        >>> sizes = np.arange(0, 101, 10)
        >>> array = np.arange(0, 201, 10)
        >>> _, ax = plt.subplots(figsize=(1, 1.5)); ax.set_axis_off()
        >>> size_legend(sizes, array=array, 
        ...             show_at=[.2, .4, .6, .8, 1.],
        ...             colors=['r', 'r', '.5', '.5', 'g'],
        ...             handler_kw=dict(ec='orange'))


    """

    def __init__(self,
                 sizes,
                 *,
                 ax=None,
                 labels=None,
                 array=None,
                 colors=None,
                 show_at=None,
                 dtype=None,
                 handler_kw=None,
                 **kwargs
                 ):
        if show_at is None:
            show_at = [.25, .5, .75, 1.]
        if handler_kw is None:
            handler_kw = {}
        num = len(show_at)

        sizes = np.asarray(sizes)
        if dtype is None:
            if array is not None:
                dtype = array.dtype
            else:
                dtype = sizes.dtype

        handle_sizes = np.array(
            [np.percentile(sizes, q * 100) for q in show_at],
            dtype=dtype)

        if colors is None:
            self._size_colors = ['black' for _ in range(num)]
        elif is_color_like(colors):
            self._size_colors = [colors for _ in range(num)]
        else:
            self._size_colors = colors

        if (array is None) & (labels is None):
            self._size_labels = handle_sizes
        elif labels is not None:
            self._size_labels = labels
        else:
            self._size_labels = np.array([
                np.percentile(array, q * 100) for q in show_at],
                dtype=dtype)

        size_handles = []
        size_labels = []

        for s, label, color in zip(handle_sizes,
                                   self._size_labels,
                                   self._size_colors):
            size_handles.append(CircleCollection([s],
                                                 facecolors=color,
                                                 **handler_kw,
                                                 ))
            size_labels.append(label)

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
            ax=ax,
            handles=size_handles,
            labels=size_labels,
            **options)
