from __future__ import annotations

from abc import ABC

import matplotlib as mpl
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib import _api, cm, contour, ticker, colors
import matplotlib.scale as mscale
from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable, get_cmap
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.colors import Colormap, Normalize
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import DrawingArea, VPacker, HPacker, TextArea, AnchoredOffsetbox, AuxTransformBox
from matplotlib.patches import Rectangle
from matplotlib.text import Text


class ColorArt(Artist):

    def __repr__(self):
        return "<ColorArt>"

    def __init__(self,
                 ax: Axes = None,
                 mappable: ScalarMappable = None,
                 cmap: str | Colormap = None,
                 norm: Normalize = None,
                 alpha: float = None,
                 values=None,
                 boundaries=None,
                 extend=None,
                 extendfrac=None,
                 extendrect=False,
                 flip=False,
                 spacing='uniform',
                 orientation: str = "vertical",

                 ticks=None,
                 format=None,
                 ticklocation="both",

                 # arguments from legend
                 width: float = None,  # relative to fontsize
                 height: float = None,
                 borderpad: float = None,
                 textpad: float = None,
                 borderaxespad: float = None,

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

        if mappable is None:
            mappable = cm.ScalarMappable(norm=norm, cmap=cmap)

        if mappable.get_array() is not None:
            mappable.autoscale_None()

        self.mappable = mappable
        cmap = mappable.cmap
        norm = mappable.norm

        if isinstance(mappable, contour.ContourSet):
            cs = mappable
            alpha = cs.get_alpha()
            boundaries = cs._levels
            values = cs.cvalues
            extend = cs.extend
            if ticks is None:
                ticks = ticker.FixedLocator(cs.levels, nbins=10)
        elif isinstance(mappable, Artist):
            alpha = mappable.get_alpha()

        _api.check_in_list(['vertical', 'horizontal'], orientation=orientation)
        _api.check_in_list(['both', 'left', 'right', 'top', 'bottom'], ticklocation=ticklocation)
        _api.check_in_list(['uniform', 'proportional'], spacing=spacing)

        if extend is None:
            if (not isinstance(mappable, contour.ContourSet)) \
                    and (getattr(cmap, 'colorbar_extend', False) is not False):
                extend = cmap.colorbar_extend
            elif hasattr(norm, 'extend'):
                extend = norm.extend
            else:
                extend = 'neither'
        self.extend = extend
        self.flip = flip
        self.alpha = None
        self.set_alpha(alpha)
        self.cmap = cmap
        self.norm = norm
        self.values = values
        self.boundaries = boundaries
        self.spacing = spacing
        self._inside = _api.check_getitem(
            {'neither': slice(0, None), 'both': slice(1, -1),
             'min': slice(1, None), 'max': slice(0, -1)},
            extend=extend)
        self.orientation = orientation

        # handle locator
        self._locator = None
        self._formatter = None
        self._minorlocator = None
        self.__scale = None

        if ticklocation == 'auto':
            ticklocation = 'bottom' if orientation == 'horizontal' else 'right'
        self.ticklocation = ticklocation

        if np.iterable(ticks):
            self._locator = ticker.FixedLocator(ticks, nbins=len(ticks))
        else:
            self._locator = ticks  # Handle default in _ticker()

        if isinstance(format, str):
            # Check format between FormatStrFormatter and StrMethodFormatter
            try:
                self._formatter = ticker.FormatStrFormatter(format)
                _ = self._formatter(0)
            except TypeError:
                self._formatter = ticker.StrMethodFormatter(format)
        else:
            self._formatter = format

        self.tick_width = 1
        self.tick_size = 0.25

        if ax is None:
            ax = plt.gca()
        self.ax = ax

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
        self._set_height_width(height, width)
        self.title = title
        self.title_fontsize = title_fontsize
        self.title_fontproperties = title_fontproperties

        self._loc = loc
        self._bbox_to_anchor = bbox_to_anchor
        self._bbox_transform = bbox_transform
        if (loc is None) & (bbox_to_anchor is None) & (bbox_transform is None):
            self._loc = "center left"
            self._bbox_to_anchor = (1.05, 0.5)
            self._bbox_transform = self.ax.transAxes

        self.textpad = mpl.rcParams['legend.handletextpad'] if textpad is None else textpad
        self.borderpad = mpl.rcParams['legend.borderpad'] if borderpad is None else borderpad
        self.borderaxespad = mpl.rcParams['legend.borderaxespad'] if borderaxespad is None else borderaxespad

        # the container for title, colorbar, ticks and tick labels
        self._cbar_box = None
        self._process_values()
        self._get_locator_formatter()
        self._get_ticks()
        # self._make_cbar_box()

    def _set_height_width(self, height, width):
        if self.orientation == "vertical":
            if width is not None:
                self.width = width * self._fontsize
            else:
                self.width = mpl.rcParams["legend.handlelength"] * self._fontsize
            if height is not None:
                self.height = height * self._fontsize
            else:
                self.height = 4 * self.width

        else:
            if height is not None:
                self.height = height * self._fontsize
            else:
                self.height = mpl.rcParams["legend.handleheight"] * self._fontsize
            if width is not None:
                self.width = width * self._fontsize
            else:
                self.width = 4 * self.height

    def _add_patches(self):

    def _make_cbar_box(self):
        self._cbar_canvas = DrawingArea(self.width, self.height)

        # create colorbar
        cmap_caller = get_cmap(self.cmap)
        colors = cmap_caller(np.arange(cmap_caller.N))
        x, y = 0, 0
        rects = []
        if self.orientation == "vertical":
            dy = self.height / len(colors)

            for c in colors:
                rects.append(
                    Rectangle((x, y), width=self.width, height=dy, fc=c)
                )
                y += dy

            patches = PatchCollection(rects, match_original=True)
            # TODO: clip on ellipse / triangle
            # patches.set_clip_path(Ellipse((w/2, h/2), w, h, transform=da.get_transform()))

        else:
            dx = self.width / len(colors)
            for c in colors:
                rects.append(
                    Rectangle((x, y), width=dx, height=self.height, fc=c)
                )
                x += dx
            patches = PatchCollection(rects, match_original=True)
        self._cbar_canvas.add_artist(patches)

        # create axis
        # TODO: handle tick locator
        locator = ticker.FixedLocator(np.linspace(self.vmin, self.vmax, 6))
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

        self._cbar_canvas.add_artist(ticks1)
        self._cbar_canvas.add_artist(ticks2)

        self.text_canvas = self._labels()
        pack1 = HPacker(pad=0, sep=0, children=[self._cbar_canvas, self.text_canvas], align="center")
        title_canvas = TextArea(self.title, textprops={"fontweight": 600})
        title_pack = VPacker(pad=0, sep=self._fontsize / 2, children=[title_canvas, pack1])
        title_pack.axes = self.ax
        self._cbar_box = AnchoredOffsetbox(
            self._loc, child=title_pack,
            pad=self.borderpad,
            borderpad=self.borderaxespad,
            bbox_transform=self._bbox_transform,
            bbox_to_anchor=self._bbox_to_anchor,
            frameon=True)
        self.ax.add_artist(self._cbar_box)

    def _labels(self):
        texts = []
        text_arts = []
        text_canvas = DPIAuxTransformBox(mtransforms.IdentityTransform())  # DrawingArea(0, 0)

        for ix, i in enumerate(np.linspace(0, self.height, len(self.ticks))):
            text = self.ticks[ix]
            t = Text(self.textpad * self._fontsize, i, text=text, va="center", ha="left", fontsize=self._fontsize)
            text_arts.append(t)
            text_canvas.add_artist(t)
        return text_canvas

    def set_alpha(self, alpha):
        self.alpha = None if isinstance(alpha, np.ndarray) else alpha

    def get_children(self):
        return self._cbar_box

    def remove(self):
        self._cbar_box.remove()

    def set_border(self, *args):
        # TODO: allow user to draw border on the colorbar
        pass

    def _process_values(self):
        if self.values is not None:
            # set self._boundaries from the values...
            self._values = np.array(self.values)
            if self.boundaries is None:
                # bracket values by 1/2 dv:
                b = np.zeros(len(self.values) + 1)
                b[1:-1] = 0.5 * (self._values[:-1] + self._values[1:])
                b[0] = 2.0 * b[1] - b[2]
                b[-1] = 2.0 * b[-2] - b[-3]
                self._boundaries = b
                return
            self._boundaries = np.array(self.boundaries)
            return

        # otherwise values are set from the boundaries
        if isinstance(self.norm, colors.BoundaryNorm):
            b = self.norm.boundaries
        elif isinstance(self.norm, colors.NoNorm):
            # NoNorm has N blocks, so N+1 boundaries, centered on integers:
            b = np.arange(self.cmap.N + 1) - .5
        elif self.boundaries is not None:
            b = self.boundaries
        else:
            # otherwise make the boundaries from the size of the cmap:
            N = self.cmap.N + 1
            b = np.linspace(0, 1, N)
        # add extra boundaries if needed:
        if self._extend_lower():
            b = np.hstack((b[0] - 1, b))
        if self._extend_upper():
            b = np.hstack((b, b[-1] + 1))

        # transform from 0-1 to vmin-vmax:
        if not self.norm.scaled():
            self.norm.vmin = 0
            self.norm.vmax = 1
        self.norm.vmin, self.norm.vmax = mtransforms.nonsingular(
            self.norm.vmin, self.norm.vmax, expander=0.1)
        if (not isinstance(self.norm, colors.BoundaryNorm) and
                (self.boundaries is None)):
            b = self.norm.inverse(b)

        self._boundaries = np.asarray(b, dtype=float)
        self._values = 0.5 * (self._boundaries[:-1] + self._boundaries[1:])
        if isinstance(self.norm, colors.NoNorm):
            self._values = (self._values + 0.00001).astype(np.int16)

    def _get_locator_formatter(self):
        """Determine the locator to get ticks"""
        locator = self._locator
        formatter = self._formatter
        minorlocator = self._minorlocator
        if isinstance(self.norm, colors.BoundaryNorm):
            b = self.norm.boundaries
            if locator is None:
                locator = ticker.FixedLocator(b, nbins=10)
            if minorlocator is None:
                minorlocator = ticker.FixedLocator(b)
        elif isinstance(self.norm, colors.NoNorm):
            if locator is None:
                # put ticks on integers between the boundaries of NoNorm
                nv = len(self._values)
                base = 1 + int(nv / 10)
                locator = ticker.IndexLocator(base=base, offset=.5)
        elif isinstance(self.norm, colors.LogNorm):
            base = self.norm._scale.base
            if locator is None:
                locator = ticker.LogLocator(base=base)
            if formatter is None:
                formatter = ticker.LogFormatterSciNotation(base=base)
        elif isinstance(self.norm, colors.SymLogNorm):
            base = self.norm._scale.base
            if locator is None:
                locator = ticker.SymmetricalLogLocator(linthresh=self.norm.linthresh, base=base)
            if formatter is None:
                formatter = ticker.LogFormatterSciNotation(base=base)
        elif self.boundaries is not None:
            b = self._boundaries[self._inside]
            if locator is None:
                locator = ticker.FixedLocator(b, nbins=10)
        else:  # most cases:
            if locator is None:
                # we haven't set the locator explicitly, so use the default
                # for this axis:
                locator = ticker.AutoLocator()
            if minorlocator is None:
                minorlocator = ticker.NullLocator()

        if minorlocator is None:
            minorlocator = ticker.NullLocator()

        if formatter is None:
            formatter = ticker.ScalarFormatter()

        self._locator = locator
        self._formatter = formatter
        self._minorlocator = minorlocator

    def _get_ticks(self):
        if isinstance(self.norm, colors.NoNorm) and self.boundaries is None:
            intv = self._values[0], self._values[-1]
        else:
            intv = (np.nanmin(self._values), np.nanmax(self._values))

        locator = self._locator
        formatter = self._formatter
        locator.create_dummy_axis(minpos=intv[0])
        locator.axis.set_view_interval(*intv)
        locator.axis.set_data_interval(*intv)
        formatter.set_axis(locator.axis)

        b = np.array(locator())
        if isinstance(locator, ticker.LogLocator):
            eps = 1e-2
            b = b[(b <= intv[1] * (1 + eps)) & (b >= intv[0] * (1 - eps))]
            #b = b[(b >= intv[0] * (1 - eps))]
        # else:
        #     eps = (intv[1] - intv[0]) * 1e-10
        #     b = b[(b <= intv[1] + eps) & (b >= intv[0] - eps)]
        ticks = self._locate(b)
        ticklabels = formatter.format_ticks(b)
        offset_string = formatter.get_offset()
        return ticks, ticklabels, offset_string

    def _locate(self, v):
        locs = np.array(self.norm(i) for i in v)
        if self.orientation == "vertical":
            if self.flip:
                return locs * self.height
            return (1 - locs) * self.height
        else:
            if self.flip:
                return locs * self.width
            return (1 - locs) * self.width

    def _extend_lower(self):
        """Return whether the lower limit is open ended."""
        minmax = "max" if self.flip else "min"
        return self.extend in ('both', minmax)

    def _extend_upper(self):
        """Return whether the upper limit is open ended."""
        minmax = "min" if self.flip else "max"
        return self.extend in ('both', minmax)


# plotnine/guides/guide_colorbar.py
# Fix AuxTransformBox, Adds a dpi_transform
# See https://github.com/matplotlib/matplotlib/pull/7344
class DPIAuxTransformBox(AuxTransformBox, ABC):
    def __init__(self, aux_transform):
        AuxTransformBox.__init__(self, aux_transform)
        self.dpi_transform = mtransforms.Affine2D()

    def get_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform` applied
        to the children
        """
        return self.aux_transform + \
               self.ref_offset_transform + \
               self.dpi_transform + \
               self.offset_transform

    def draw(self, renderer):
        """
        Draw the children
        """
        dpi_cor = renderer.points_to_pixels(1.)
        self.dpi_transform.clear()
        self.dpi_transform.scale(dpi_cor, dpi_cor)

        for c in self._children:
            c.draw(renderer)

        self.stale = False


class _DummyAxis:
    __name__ = "dummy"

    def __init__(self, minpos=0):
        self.dataLim = mtransforms.Bbox.unit()
        self.viewLim = mtransforms.Bbox.unit()
        self._minpos = minpos

    def get_view_interval(self):
        return self.viewLim.intervalx

    def set_view_interval(self, vmin, vmax):
        self.viewLim.intervalx = vmin, vmax

    def get_minpos(self):
        return self._minpos

    def get_data_interval(self):
        return self.dataLim.intervalx

    def set_data_interval(self, vmin, vmax):
        self.dataLim.intervalx = vmin, vmax

    def get_tick_space(self):
        # Just use the long-standing default of nbins==9
        return 9
