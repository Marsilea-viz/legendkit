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
from matplotlib.offsetbox import DrawingArea
from matplotlib.patches import Rectangle


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

                 ):
        super().__init__()

        self.tick_width = 1
        self.tick_size = 0.25
        self.ticklocation = ticklocation

        if ax is None:
            ax = plt.gca()
        self.ax = ax

        if self.cmap is None:
            cmap = mpl.rcParams['image.cmap']
        self.cmap = cmap

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

    def _init_colorart(self):
        self.cbar_canvas = DrawingArea(self.width, self.height)
        self._create_gradient()
        self._create_axis()

    def _create_axis(self):
        lines1 = LineCollection([[(0, i), (cbar_w * ticklen, i)] for i in np.linspace(0, cbar_h, len(ticks))],
                                color="w", zorder=100,
                                visible=True, linewidth=linewidth)

        lines2 = LineCollection(
            [[(cbar_w, i), (cbar_w - cbar_w * ticklen, i)] for i in np.linspace(0, cbar_h, len(ticks))],
            color="w", zorder=100,
            visible=True, linewidth=linewidth)

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
