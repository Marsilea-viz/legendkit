from functools import partial
from typing import List, Union, Dict, Tuple, Optional

import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.collections import Collection
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.offsetbox import VPacker, HPacker
from matplotlib.patches import Patch

from .handles import SquareItem, RectItem, CircleItem, LineItem

_handlers = {
    'square': SquareItem,
    'rect': RectItem,
    'circle': CircleItem,
    'line': LineItem
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

    def __repr__(self):
        return "<ListLegend>"

    def __init__(self,
                 ax: Union[Axes, None] = None,
                 legend_items: Union[List[Tuple], None] = None,
                 handles: Union[str, Artist, List[str], List[Artist], None] = None,
                 labels: Union[List[str], None] = None,
                 style: str = 'none',  # 'none', 'frameless'
                 title_pos: str = "top",  # "top" or "left",
                 title_align: str = "center",
                 titlepad: float = 0.5,
                 draw: bool = True,
                 handler_map: Optional[Dict] = None,
                 **kwargs,
                 ):
        """This is a modified class of the original matplotlib class

        Parameters
        ----------
        ax
        legend_items
        handles
        labels
        style
        title_pos
        title_align
        titlepad
        draw
        handler_map
        kwargs

        """

        self._title_pos = title_pos
        self._title_align = title_align
        self.titlepad = titlepad
        self._is_patch = False

        legend_handles = []
        legend_labels = []

        self._has_axes = ax is not None

        # If only axes is provided, we will try to get
        if (ax is not None) & (legend_items is None) & (handles is None) & (labels is None):
            legend_handles, legend_labels = ax.get_legend_handles_labels(handler_map)
        # If nothing is provided, we will get current axes and get the handles
        elif (ax is None) & (legend_items is None) & (handles is None) & (labels is None):
            ax = plt.gca()
            legend_handles, legend_labels = ax.get_legend_handles_labels(handler_map)
        else:
            ax = plt.gca()

        if legend_items is not None:
            for item in legend_items:
                if len(item) == 2:
                    handle, label = item
                    handle_config = None
                else:
                    item = item[:3]
                    handle, label, handle_config = item
                legend_handles.append(_parse_handler(handle, config=handle_config))
                legend_labels.append(label)

        if legend_items is None:
            # make matplotlib handles this
            legend_handles, legend_labels = handles, labels

        # handle location parameters
        # we provide extra loc parameters
        # ['out left center', 'out ]

        frameless_options = dict(
            # Dimensions as fraction of font size:
            frameon=False,
            borderpad=0,  # 0.4,  # border whitespace
            labelspacing=0.5,  # the vertical space between the legend entries
            handlelength=1.5,  # 2.0,  # the length of the legend lines
            handleheight=1.,  # 0.7,  # the height of the legend handle
            handletextpad=0.4,  # 0.8,  # the space between the legend line and legend text
            borderaxespad=0.,  # 0.5,  # the border between the axes and legend edge
            columnspacing=1.0,  # 2.0,  # column separation
        )

        default_kwargs = dict(
            title_fontproperties={'weight': 600},  # Make the title bold if user supply no style
            handler_map=handler_map,
        )

        if style == 'frameless':
            default_kwargs = {**default_kwargs, **frameless_options}

        final_options = {**default_kwargs, **kwargs}
        super().__init__(ax, handles=legend_handles, labels=legend_labels, **final_options)
        self._title_layout()

        if draw:
            ax.add_artist(self)

    def _title_layout(self):
        fontsize = self._fontsize
        title_align = self._title_align
        title_pos = self._title_pos

        pad = self.borderpad * fontsize
        sep = self.titlepad * fontsize
        # To make positioning of legend title possible by override the default legend box layout
        hpacker = partial(HPacker, pad=pad, sep=sep, align=title_align)
        vpacker = partial(VPacker, pad=pad, sep=sep, align=title_align)
        children = [self._legend_title_box, self._legend_handle_box]

        if title_pos == "top":
            self._legend_box = vpacker(children=children)
        elif title_pos == "bottom":
            self._legend_box = vpacker(children=children[::-1])
        elif title_pos == "left":
            self._legend_box = hpacker(children=children)
        elif title_pos == "right":
            self._legend_box = hpacker(children=children[::-1])
        else:
            raise NotImplementedError("Available options are: (top, bottom, right, left)")
        self._legend_box.set_figure(self.figure)
        self._legend_box.axes = self.axes

        # call this to maintain consistent behavior as legend
        self._legend_box.set_offset(self._findoffset)

    def set_title(self, title, align=None, prop=None):
        """
        Set the legend title. Fontproperties can be optionally set
        with *prop* parameter.
        """
        self._legend_title_box._text.set_text(title)
        if title:
            self._legend_title_box._text.set_visible(True)
            self._legend_title_box.set_visible(True)
        else:
            self._legend_title_box._text.set_visible(False)
            self._legend_title_box.set_visible(False)

        if align is not None:
            self._legend_box.align = align

        if prop is not None:
            self._legend_title_box._text.set_fontproperties(prop)

        self.stale = True
