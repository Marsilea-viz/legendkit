from __future__ import annotations

import matplotlib as mpl
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib import _api, cm, contour, ticker, colors
from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import DrawingArea, VPacker, TextArea, \
    AnchoredOffsetbox
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.text import Text

from ._locs import Locs


def get_colormap(cmap):
    if isinstance(cmap, colors.Colormap):
        return cmap
    return mpl.colormaps.get(cmap)


class ColorArt(Artist):
    """Axes-independent colorbar

    Parameters
    ----------
    mappable
    cmap
    norm
    ax
    alpha
    values
    boundaries
    flip
    orientation
    ticks
    format
    tick_width
    tick_size
    tick_color
    ticklocation
    width
    height
    borderpad
    textpad
    borderaxespad
    prop
    fontsize
    title
    title_fontsize
    title_fontproperties
    alignment
    loc
    deviation
    bbox_to_anchor
    bbox_transform
    rasterized : bool
        Whether to rasterize the colorart,
        reduce file size in vectorized backend.

    """

    def __repr__(self):
        return "<ColorArt>"

    def __init__(self,
                 mappable=None,
                 cmap=None,
                 norm=None,
                 *,
                 ax: Axes = None,
                 alpha=None,
                 values=None,
                 boundaries=None,
                 # extend=None,
                 # extendfrac=None,
                 # extendrect=False,
                 flip=False,
                 # spacing='uniform',
                 orientation="vertical",
                 shape="rect",

                 ticks=None,
                 format=None,
                 tick_width=1,
                 tick_size=0.25,
                 tick_color="white",
                 ticklabel_loc="auto",
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
                 alignment="left",

                 loc=None,
                 deviation=0.05,
                 bbox_to_anchor=None,
                 bbox_transform=None,

                 rasterized=True,

                 ):
        if ax is None:
            ax = plt.gca()
        self.ax = ax

        super().__init__()
        if rasterized:
            # Force rasterization
            self._rasterized = True

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
        _api.check_in_list(['both', 'left', 'right', 'top', 'bottom'],
                           ticklocation=ticklocation)
        # _api.check_in_list(['uniform', 'proportional'], spacing=spacing)

        extend = None
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
        # self.spacing = spacing
        self._inside = _api.check_getitem(
            {'neither': slice(0, None), 'both': slice(1, -1),
             'min': slice(1, None), 'max': slice(0, -1)},
            extend=extend)
        self.orientation = orientation
        self.shape = shape

        # handle locator
        self._locator = None
        self._formatter = None
        self._minorlocator = None
        self.__scale = None

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

        self.tick_width = tick_width
        self.tick_size = tick_size
        self.tick_color = tick_color
        self.ticklocation = ticklocation
        self.ticklabel_loc = ticklabel_loc

        if fontsize is None:
            fontsize = mpl.rcParams["legend.fontsize"]
        # Copy from matplotlib/lib/plot_simple_tutorial.py
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
        self.alignment = alignment

        self._loc, self._bbox_to_anchor, self._bbox_transform = \
            Locs().transform(ax, loc, bbox_to_anchor=bbox_to_anchor,
                             bbox_transform=bbox_transform,
                             deviation=deviation)

        self.textpad = mpl.rcParams[
            'legend.handletextpad'] if textpad is None else textpad
        self.borderpad = mpl.rcParams[
            'legend.borderpad'] if borderpad is None else borderpad
        self.borderaxespad = mpl.rcParams[
            'legend.borderaxespad'] if borderaxespad is None else borderaxespad

        # the container for title, colorbar, ticks and tick labels
        self._cbar_box = None
        self._process_values()
        self._get_locator_formatter()
        self._get_ticks()
        self._make_cbar_box()

    def _set_height_width(self, height, width):
        if self.orientation == "vertical":
            if width is not None:
                self.width = width * self._fontsize
            else:
                self.width = mpl.rcParams[
                                 "legend.handlelength"] * self._fontsize
            if height is not None:
                self.height = height * self._fontsize
            else:
                self.height = 5 * self.width

        else:
            if height is not None:
                self.height = height * self._fontsize
            else:
                self.height = mpl.rcParams[
                                  "legend.handleheight"] * self._fontsize
            if width is not None:
                self.width = width * self._fontsize
            else:
                self.width = 5 * self.height

    def _make_cbar_box(self):
        locs, ticks1, ticks2, ticklabels, offset_string = self._get_ticks()
        x_offset, y_offset = self._get_text_size(ticklabels)
        width, height = self.width, self.height
        textpad = self.textpad * self._fontsize
        if self.orientation == "vertical":
            width = self.width + x_offset + textpad
        else:
            height = self.height + y_offset + textpad

        # Add cbar
        canvas = DrawingArea(width, height, clip=True)
        # self._add_color_patches(self._cbar_canvas)

        cmap_caller = get_colormap(self.cmap)
        colors_list = cmap_caller(np.arange(cmap_caller.N))
        if self.flip:
            colors_list = colors_list[::-1]

        rects = []
        x, y = 0, 0
        if self.orientation == "vertical":
            dy = self.height / len(colors_list)
            for c in colors_list:
                rects.append(Rectangle((x, y), width=self.width, height=dy,
                                       fc=c, antialiased=False,
                                       alpha=self.alpha))
                y += dy

        else:
            dx = self.width / len(colors_list)
            for c in colors_list:
                rects.append(Rectangle((x, y), width=dx, height=self.height,
                                       fc=c, antialiased=False,
                                       alpha=self.alpha))
                x += dx
        patches = PatchCollection(rects, match_original=True)

        if self.shape == "ellipse":
            patches.set_clip_path(
                Ellipse((self.width / 2, self.height / 2),
                        self.width, self.height,
                        transform=canvas.get_transform()))
        canvas.add_artist(patches)

        # Add ticks
        if self.shape == "rect":
            # the tick will only be added if shape is rect
            ticks1_lines = LineCollection(
                ticks1,
                color=self.tick_color, zorder=100,
                visible=True, linewidth=self.tick_width)

            ticks2_lines = LineCollection(
                ticks2,
                color=self.tick_color, zorder=100,
                visible=True, linewidth=self.tick_width)

            if self.ticklocation == "both":
                canvas.add_artist(ticks1_lines)
                canvas.add_artist(ticks2_lines)
            elif self.ticklocation in ["bottom", "left"]:
                canvas.add_artist(ticks1_lines)
            else:
                canvas.add_artist(ticks2_lines)

            label_x = self.width + textpad
            label_y = self.height + textpad
            va, ha = "bottom", "center"
            if self.orientation == "vertical":
                va, ha = "center", "left"
            options = dict(va=va, ha=ha, fontsize=self._fontsize,
                           fontproperties=self.prop)
            for loc, label in zip(locs, ticklabels):
                if self.orientation == "vertical":
                    t = Text(label_x, loc, label, **options)
                else:
                    t = Text(loc, label_y, label, **options)
                canvas.add_artist(t)

        if self.title is not None:
            if self.title_fontproperties is None:
                textprops = dict(fontweight=600)
            else:
                textprops = dict(fontproperties=self.title_fontproperties)
            title_canvas = TextArea(self.title, textprops=textprops)
            title_pack = VPacker(pad=0,
                                 # A heuristic value to make the title
                                 # not overlap with labels
                                 sep=0.4 * self._fontsize,
                                 children=[title_canvas, canvas],
                                 align=self.alignment
                                 )
            title_pack.axes = self.ax
            final_pack = title_pack
        else:
            final_pack = canvas
        self._cbar_box = AnchoredOffsetbox(
            self._loc, child=final_pack,
            pad=self.borderpad,
            borderpad=self.borderaxespad,
            bbox_transform=self._bbox_transform,
            bbox_to_anchor=self._bbox_to_anchor,
            frameon=False)
        self.ax.add_artist(self._cbar_box)

    def _get_text_size(self, ticklabels):
        """Used to get the proper size for drawing area"""
        fig = self.ax.get_figure()
        renderer = fig.canvas.get_renderer()
        all_texts = []
        for t in ticklabels:
            text_obj = Text(0, 0, t, fontsize=self._fontsize,
                            fontproperties=self.prop)
            self.ax.add_artist(text_obj)
            all_texts.append(text_obj)
        x_sizes, y_sizes = [], []
        for t in all_texts:
            bbox = t.get_window_extent(renderer)
            x_sizes.append(bbox.xmax - bbox.xmin)
            y_sizes.append(bbox.ymax - bbox.ymin)
            t.remove()  # so it won't be drawn
        x_offset = np.max(x_sizes) / (fig.dpi / 72)
        y_offset = np.max(y_sizes) / (fig.dpi / 72)
        return x_offset, y_offset

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
        # TODO: For CenteredNorm and TwoSlopeNorm
        #   Maybe need to ask user to scaled it first
        if isinstance(self.norm, colors.CenteredNorm):
            if self.norm.halfrange is None:
                self.norm.halfrange = 1
            self.norm.vmin = self.norm.vcenter - self.norm.halfrange
            self.norm.vmax = self.norm.vcenter + self.norm.halfrange

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
                locator = ticker.FixedLocator(b, nbins=5)
            if minorlocator is None:
                minorlocator = ticker.FixedLocator(b)
        elif isinstance(self.norm, colors.NoNorm):
            if locator is None:
                # put ticks on integers between the boundaries of NoNorm
                nv = len(self._values)
                base = 1 + int(nv / 10)
                locator = ticker.IndexLocator(base=base, offset=0)
        elif isinstance(self.norm, colors.LogNorm):
            base = self.norm._scale.base
            if locator is None:
                locator = ticker.LogLocator(base=base)
            if formatter is None:
                formatter = ticker.LogFormatterSciNotation(base=base)
        elif isinstance(self.norm, colors.SymLogNorm):
            base = self.norm._scale.base
            if locator is None:
                locator = ticker.SymmetricalLogLocator(
                    linthresh=self.norm.linthresh, base=base)
            if formatter is None:
                formatter = ticker.LogFormatterSciNotation(base=base)
        elif self.boundaries is not None:
            b = self._boundaries[self._inside]
            if locator is None:
                locator = ticker.FixedLocator(b, nbins=5)
        else:
            # AsinhNorm is introduced at 3.6
            if hasattr(colors, 'AsinhNorm'):
                if isinstance(self.norm, colors.AsinhNorm):
                    base = 10  # self.norm._scale.base
                    if locator is None:
                        locator = ticker.AsinhLocator(
                            linear_width=self.norm.linear_width, base=base)
                    if formatter is None:
                        if base > 1:
                            formatter = ticker.LogFormatterSciNotation(
                                base=base)
                        else:
                            formatter = ticker.StrMethodFormatter('{x:.3g}')
            # most cases:
            if locator is None:
                # we haven't set the locator explicitly, so use the default
                # for this axis:
                locator = ticker.MaxNLocator(nbins=5, steps=[1, 2, 2.5, 5, 10])
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
            eps = 1e-10
            b = b[(b <= intv[1] * (1 + eps)) & (b >= intv[0] * (1 - eps))]
            # b = b[(b >= intv[0] * (1 - eps))]
        else:
            eps = (intv[1] - intv[0]) * 1e-10
            b = b[(b <= intv[1] + eps) & (b >= intv[0] - eps)]
        locs, ticks1, ticks2 = self._locate(b)
        ticklabels = formatter.format_ticks(b)
        offset_string = formatter.get_offset()
        return locs, ticks1, ticks2, ticklabels, offset_string

    def _locate(self, v):
        if isinstance(self.norm, (colors.NoNorm, colors.BoundaryNorm)):
            arr = self._boundaries
            normalize = colors.Normalize(vmin=np.min(arr), vmax=np.max(arr))
            locs = np.array([normalize(i) for i in v])
        else:
            locs = np.array([self.norm(i) for i in v])
        if self.orientation == "vertical":
            locs = (
                           1 - locs) * self.height if self.flip else locs * self.height

            ticks_left = [[(0, loc), (self.width * self.tick_size, loc)] for
                          loc in locs]
            ticks_right = [
                [(self.width, loc), (self.width * (1 - self.tick_size), loc)]
                for loc in locs]
            return locs, ticks_left, ticks_right
        else:
            locs = (1 - locs) * self.width if self.flip else locs * self.width

            ticks_bottom = [[(loc, 0), (loc, self.height * self.tick_size)] for
                            loc in locs]
            ticks_top = [
                [(loc, self.height), (loc, self.height * (1 - self.tick_size))]
                for loc in locs]
            return locs, ticks_bottom, ticks_top

    def _extend_lower(self):
        """Return whether the lower limit is open ended."""
        minmax = "max" if self.flip else "min"
        return self.extend in ('both', minmax)

    def _extend_upper(self):
        """Return whether the upper limit is open ended."""
        minmax = "min" if self.flip else "max"
        return self.extend in ('both', minmax)

    def set_alpha(self, alpha):
        self.alpha = None if isinstance(alpha, np.ndarray) else alpha

    def get_children(self):
        return self._cbar_box

    def remove(self):
        self._cbar_box.remove()

    def set_border(self, *args):
        # TODO: allow user to draw border on the colorbar
        pass


