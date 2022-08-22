from __future__ import annotations

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable, get_cmap
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.colors import Colormap, Normalize
from matplotlib.font_manager import FontProperties
from matplotlib.image import BboxImage
from matplotlib.offsetbox import DrawingArea, VPacker, HPacker, TextArea, AnchoredOffsetbox
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.ticker import FixedLocator


class ColorArt(Artist):

    def __init__(self,
                 mappable: ScalarMappable = None,
                 cmap: str | Colormap = None,
                 norm: Normalize = None,
                 vmin: float = None,
                 vmax: float = None,
                 clip: bool = False,

                 ticks=None,
                 format=None,
                 ticklocation="both",

                 ax: Axes = None,
                 width: float = 2.0,  # relative to fontsize
                 height: float = 8.0,
                 orientation: str = "vertical",

                 prop=None,
                 fontsize=None,
                 title=None,  # legend title
                 title_fontsize=None,  # legend title font size
                 title_fontproperties=None,  # legend title font size

                 loc=None,
                 bbox_to_anchor=None,
                 bbox_transform=None,

                 ):
        super().__init__()

        self.tick_width = 1
        self.tick_size = 0.25
        self.ticklocation = ticklocation

        if ax is None:
            ax = plt.gca()
        self.ax = ax

        if cmap is None:
            cmap = mpl.rcParams['image.cmap']
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax

        if fontsize is None:
            fontsize = mpl.rcParams["legend.fontsize"]
        # Copy from matplotlib/lib/legend.py
        if prop is None:
            self.prop = FontProperties(size=fontsize)
        else:
            self.prop = FontProperties._from_any(prop)
            if isinstance(prop, dict) and "size" not in prop:
                self.prop.set_size(mpl.rcParams["legend.fontsize"])

        self._fontsize = self.prop.get_size_in_points()

        self.orientation = orientation
        self.width = width * self._fontsize
        self.height = height * self._fontsize
        self.title = title
        self.title_fontsize = title_fontsize
        self.title_fontproperties = title_fontproperties

        self.loc = "upper right"
        self.bbox_to_anchor = bbox_to_anchor
        self.bbox_transform = bbox_transform

        self.textpad = mpl.rcParams['legend.handletextpad']

        self._init_colorart()

    def _init_colorart(self):
        self.cbar_canvas = DrawingArea(self.width, self.height)
        self._create_gradient()
        self._create_axis()
        self.text_canvas = self._labels()
        pack1 = HPacker(pad=0, sep=0, children=[self.cbar_canvas, self.text_canvas])
        title_canvas = TextArea(self.title, textprops={"fontweight": 600})
        title_pack = VPacker(pad=0, sep=self._fontsize/2, children=[title_canvas, pack1])
        self._cbar_box = AnchoredOffsetbox(
            self.loc, child=title_pack,
            bbox_transform=self.bbox_transform,
            bbox_to_anchor=self.bbox_to_anchor,
            frameon=False)
        self.ax.add_artist(self._cbar_box)

    def _create_axis(self):

        locator = FixedLocator(np.linspace(self.vmin, self.vmax, 6))
        self.ticks = locator.tick_values(self.vmin, self.vmax)

        # TODO: Handle ticklocations and orientation
        if self.orientation == "vertical":
            ticks1_coords = [[(0, i), (self.width * self.tick_size, i)] \
                             for i in np.linspace(0, self.height, len(self.ticks))]
            ticks2_coords = [[(self.width, i), (self.width - self.width * self.tick_size, i)] \
                             for i in np.linspace(0, self.height, len(self.ticks))]

        ticks1 = LineCollection(
            ticks1_coords,
            color="w", zorder=100,
            visible=True, linewidth=self.tick_width)

        ticks2 = LineCollection(
            ticks2_coords,
            color="w", zorder=100,
            visible=True, linewidth=self.tick_width)

        self.cbar_canvas.add_artist(ticks1)
        self.cbar_canvas.add_artist(ticks2)

    def _create_gradient(self):
        cmap_caller = get_cmap(self.cmap)

        colors = cmap_caller(np.arange(cmap_caller.N))

        x, y = 0, 0
        dy = self.height / len(colors)

        rects = []
        for c in colors:
            rects.append(
                Rectangle((x, y), width=self.width, height=dy, fc=c)
            )
            y += dy

        patches = PatchCollection(rects, match_original=True)
        # Enable clip on ellipse
        # patches.set_clip_path(Ellipse((w/2, h/2), w, h, transform=da.get_transform()))
        self.cbar_canvas.add_artist(patches)

    def _labels(self):
        texts = []
        text_canvas = DrawingArea(0, 0)
        for ix, i in enumerate(np.linspace(0, self.height, len(self.ticks))):
            t = Text(self.textpad * self._fontsize, i, text=self.ticks[ix], va="center", ha="left")
            text_canvas.add_artist(t)
        return text_canvas

    def get_children(self):
        return self._cbar_box

    def remove(self):
        self._cbar_box.remove()
