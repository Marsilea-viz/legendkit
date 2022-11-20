from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import _api
from matplotlib.axes import Axes
from matplotlib.collections import Collection
from matplotlib.colors import is_color_like
from matplotlib.font_manager import FontProperties
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.markers import MarkerStyle
from matplotlib.offsetbox import VPacker, HPacker
from matplotlib.patches import Patch

from ._handlers import CircleHandler, RectHandler, BoxplotHanlder
from ._locs import Locs
from .handles import RectItem, CircleItem, LineItem, BoxplotItem

_handlers = {
    # 'square': SquareItem,
    'rect': RectItem,
    'circle': CircleItem,
    'line': LineItem,
    'boxplot': BoxplotItem,
}

_handle_marker = {
    "rect": "s",
    "square": "s",
    "circle": "o",
    "triangle": "^",
    "triangle-up": "^",
    "triangle-down": "v",
    "triangle-left": "<",
    "triangle-right": ">",
    "diamond": "d",
    "octagon": "8",
    "pentagon": "p",
    "star": "*",
    "hexagon": "h",
    "plus": "P",
    "cross": "X",
    "asterisk": (6, 2, 0)
}


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


_default_alignment = {
    "top": "left",
    "bottom": "left",
    "left": "center",
    "right": "center"
}


class ListLegend(Legend):
    """This is a modified legend based the original matplotlib class

    List of sementic legend handle to be used:
        - rect
        - circle
        - square
        - line
        - boxplot
        - triangle (triangle-up, triangle-down, triangle-left, triangle-right)
        - diamond
        - octagon
        - pentagon
        - hexagon
        - star
        - plus
        - cross
        - asterisk
        - The markers in :mod:`matplotlib.markers`

    Parameters
    ----------
    ax : Axes
        The axes to draw on
    legend_items : array-like of (handle, label, styles)
        See examples
    handles : array-like
        A list of legend handler
    labels : array-like
        A list of legend labels
    title_loc : {'top', 'bottom', 'left', 'right'}
        The location of title
    alignment : {'top', 'bottom', 'left', 'right', 'center'}
        How to align the whole legendbox,
        if title is placed on top or bottom, default is 'left';
        if title is placed on left and right, default is 'center';
    titlepad : float
        The space between title and legend entries
    draw : bool
        Whether to draw the legend
    handler_map : dict
    loc : str
        Apart from the default location code, you can add 'out' as prefix
        to place the legend ouside the axes.
    deviation : float
        The space between legend and axes if legend is placed ouside axes.
    kwargs :
        For other paramters, please see :class:`matplotlib.legend.Legend`


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
                 alignment=None,
                 titlepad=0.5,
                 draw=True,
                 handler_map=None,
                 loc=None,
                 deviation=0.05,
                 bbox_to_anchor=None,
                 bbox_transform=None,
                 fontsize=None,
                 prop=None,
                 handleheight=None,
                 handlelength=None,
                 **kwargs,
                 ):

        _api.check_in_list(["top", "bottom", "left", "right"],
                           title_loc=title_loc)
        self._has_axes = ax is not None
        if ax is None:
            ax = plt.gca()
        self._title_loc = title_loc
        self.titlepad = titlepad
        self._is_patch = False

        if prop is None:
            if fontsize is not None:
                self.prop = FontProperties(size=fontsize)
            else:
                self.prop = FontProperties(
                    size=mpl.rcParams["legend.fontsize"])
        else:
            self.prop = FontProperties._from_any(prop)
            if isinstance(prop, dict) and "size" not in prop:
                self.prop.set_size(mpl.rcParams["legend.fontsize"])

        self._fontsize = self.prop.get_size_in_points()

        def val_or_rc(val, rc_name):
            return val if val is not None else mpl.rcParams[rc_name]
        self.handlelength = val_or_rc(handlelength, 'legend.handlelength')
        self.handleheight = val_or_rc(handleheight, 'legend.handleheight')
        handle_size = min(self.handleheight, self.handlelength)

        legend_handles = []
        legend_labels = []

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
                legend_handles.append(self._parse_handler(
                    handle, handle_size, config=handle_config))
                legend_labels.append(label)
        elif (handles is not None) & (labels is None):
            legend_handles = handles
            legend_labels = [h.get_label() for h in handles]
        elif (handles is None) & (labels is not None):
            legend_labels = labels
            legend_handles = [Patch() for _ in range(len(labels))]
        else:
            # make matplotlib handles this
            legend_handles, legend_labels = handles, labels

        loc, bbox_to_anchor, bbox_transform = \
            Locs().transform(ax, loc, bbox_to_anchor=bbox_to_anchor,
                             bbox_transform=bbox_transform,
                             deviation=deviation)
        if handler_map is None:
            handler_map = {}
        handler_map.update({RectItem: RectHandler(),
                            CircleItem: CircleHandler(),
                            BoxplotItem: BoxplotHanlder(),
                            })
        default_kwargs = dict(
            loc=loc,
            bbox_to_anchor=bbox_to_anchor,
            bbox_transform=bbox_transform,
            # Make the title bold if user supply no style
            title_fontproperties={'weight': 600},
            handler_map=handler_map,
            fontsize=self._fontsize,
            handleheight=self.handleheight,
            handlelength=self.handlelength,
        )

        final_options = {**default_kwargs, **kwargs}
        super().__init__(ax,
                         handles=legend_handles,
                         labels=legend_labels,
                         **final_options)
        if alignment is None:
            alignment = _default_alignment[self._title_loc]
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

    def _parse_handler(self, handle, handle_size, config=None):
        if not isinstance(handle, str):
            return handle
        if config is None:
            config = {}
        handler = _handlers.get(handle)
        # Use predefined legend handler
        if handler is not None:
            return _handlers[handle].__call__(**config)

        marker = _handle_marker.get(handle)
        if marker is None:
            # If it's not a marker
            try:
                MarkerStyle(handle)
            except Exception:
                return handle
            marker = handle
        config.setdefault("markersize", self._fontsize * handle_size)
        config.setdefault("color", "C0")
        config.update({"ls": ""})
        # handle parameters
        fc = config.pop("fc", config.pop("facecolor", None))
        ec = config.pop("ec", config.pop("edgecolor", None))
        lw = config.pop("lw", config.pop("linewidth", None))
        config.setdefault("mfc", fc)
        config.setdefault("mec", ec)
        config.setdefault("mew", lw)
        return Line2D([0], [0], marker=marker, **config)

    def set_title_loc(self, loc):
        self._title_loc = loc

    def get_title_loc(self):
        return self._title_loc

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

        if title_loc in ["bottom", "right"]:
            # if title_loc in ["bottom", "right"]:
            children = children[::-1]
        self._legend_box = packer(pad=pad, sep=sep,
                                  align=alignment, children=children)

        self._legend_box.set_figure(self.figure)
        self._legend_box.axes = self.axes

        # call this to maintain consistent behavior as legend
        self._legend_box.set_offset(self._findoffset)


_sizer = {
    "small": 0.4,
    "medium": 0.7,
    "large": 1.1,
}


class CatLegend(ListLegend):
    """Categorical legend with same handles

    This is useful to create legend that share
    the same handle but with different colors

    Parameters
    ----------
    colors : array-like
        The color for each legend item
    labels : array-like
        The text for each legend item
    handle : str or handle object, default: 'rect'
        The handle to be used for every entry
    handler_kw : mapping
        Use this to control the style of handler
    fill : bool, default: True
        If not filled, the color will draw on the edge.
    size : str or number, {"small", "medium", "large"}
        The size of legend handle
    kwargs :
        Pass to :func:`legendkit.legend`

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

    def __init__(self,
                 ax=None,
                 colors=None,
                 labels=None,
                 size="medium",
                 handle=None,
                 handler_kw=None,
                 fill=True,
                 **kwargs
                 ):
        if handle is None:
            handle = 'square'
        if handler_kw is None:
            handler_kw = {}

        legend_items = []
        for c, name in zip(colors, labels):
            if fill:
                options = {'color': c, **handler_kw}
            else:
                options = {'ec': c, 'fc': 'none', **handler_kw}
            legend_items.append((handle, name, options))
        if isinstance(size, str):
            size = _sizer[size]
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
    sizes : array-like
        The sizes array of all circles on the plot,
        the unit is point**2, same as :meth:`matplotlib.axes.Axes.scatter`
    ax : Axes
        The axes to draw the legend
    labels : array-like
        The labels of the legend
    array : array-like
        The actual data used in plotting, will be used to
        display labels if labels are not specific
    colors : array-like
        The color of the entry
    show_at : array-like, default: [.25, .5, .75, 1.]
        The percentile to show the sizes
    dtype : data type
        This can be used to enforce the data type to display
        the label
    handle : str or sizable handle
        You can use any markers in :module:matplotlib.markers
    handler_kw : mapping
        Use this to control the style of handler
    fill : bool, default: True
        If not filled, the color will draw on the edge.
    kwargs : mapping
        Pass to :func:`legendkit.legend`


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
                 handle="circle",
                 handler_kw=None,
                 fill=True,
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

        marker = _handle_marker.get(handle)
        if marker is None:
            marker = handle

        # handler_kw
        fc = handler_kw.pop("fc", handler_kw.pop("facecolor", None))
        ec = handler_kw.pop("ec", handler_kw.pop("edgecolor", None))
        lw = handler_kw.pop("lw", handler_kw.pop("linewidth", None))
        if fc is not None:
            handler_kw.setdefault("mfc", fc)
        if ec is not None:
            handler_kw.setdefault("mec", ec)
        if lw is not None:
            handler_kw.setdefault("mew", lw)

        for s, label, color in zip(handle_sizes,
                                   self._size_labels,
                                   self._size_colors):
            if fill:
                options = {'color': color, 'mew': .75, **handler_kw}
            else:
                options = {'mec': color, 'mfc': 'none',
                           'mew': .75, **handler_kw}
            ms = MarkerStyle(marker=marker)
            size_handles.append(Line2D([0], [0], ls="", marker=ms,
                                       markersize=np.sqrt(s), **options))
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
