"""Paired-circle size legend.

Renders min/max size as two circles connected by either two external tangent
lines or a single center-to-center line, with configurable orientation, order,
and label placement.
"""

from __future__ import annotations

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt, ticker
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import (
    AnchoredOffsetbox,
    HPacker,
    TextArea,
    VPacker,
)
from matplotlib.patches import Circle, Polygon

from ._colorart import DrawingArea
from ._locs import Locs


_ORIENT_OPTIONS = {"horizontal", "vertical"}
_CONNECTOR_OPTIONS = {"tangent", "center", "none"}
_LABEL_LOC_OPTIONS = {
    "auto",
    "outside",
    "above",
    "below",
    "left",
    "right",
    "center",
    "none",
}


def _tangent_hull(c1, r1, c2, r2, n_arc=32):
    """Return Nx2 polygon vertices enclosing both circles + tangent region.

    Walks: tangent_top on c1 -> tangent_top on c2 -> outer arc on c2 (away
    from c1) -> tangent_bot on c2 -> tangent_bot on c1 -> outer arc on c1
    (away from c2) -> close.
    """
    segs = _external_tangents(c1, r1, c2, r2)
    if not segs:
        return None
    (p1a, p2a), (p1b, p2b) = segs
    c1 = np.asarray(c1, dtype=float)
    c2 = np.asarray(c2, dtype=float)

    # angles of each tangent point relative to its center
    def ang(p, c):
        v = p - c
        return np.arctan2(v[1], v[0])

    a1a, a1b = ang(p1a, c1), ang(p1b, c1)
    a2a, a2b = ang(p2a, c2), ang(p2b, c2)
    # axis vector c1->c2
    axis = c2 - c1
    axis_ang = np.arctan2(axis[1], axis[0])
    # on c2, the outer arc is the one going AWAY from c1 (around the side
    # opposite to c1). Sweep from a2a to a2b through axis_ang (angle pointing
    # away from c1).
    outer_c2 = axis_ang  # +x relative to c2 axis-aligned = away from c1
    arc_c2 = _arc_between(c2, r2, a2a, a2b, through=outer_c2, n=n_arc)
    # on c1, outer arc goes away from c2; that direction = axis_ang + pi
    outer_c1 = axis_ang + np.pi
    arc_c1 = _arc_between(c1, r1, a1b, a1a, through=outer_c1, n=n_arc)
    # build the closed polygon
    verts = [p1a, p2a, *arc_c2, p2b, p1b, *arc_c1]
    return np.array(verts)


def _arc_between(center, r, a_start, a_end, through, n=32):
    """Sample n points along arc on circle (center, r) going from a_start to
    a_end such that the sweep passes through angle ``through``."""

    # normalize so the sweep direction includes `through`
    # try going counterclockwise
    def norm(a):
        return (a + np.pi) % (2 * np.pi) - np.pi

    a_start = norm(a_start)
    a_end = norm(a_end)
    through = norm(through)
    # ccw delta
    delta_ccw = (a_end - a_start) % (2 * np.pi)
    # check if `through` falls within ccw sweep
    rel_through = (through - a_start) % (2 * np.pi)
    if rel_through <= delta_ccw:
        sweep = np.linspace(0, delta_ccw, n)
    else:
        # go clockwise instead
        delta_cw = (a_start - a_end) % (2 * np.pi)
        sweep = -np.linspace(0, delta_cw, n)
    angles = a_start + sweep
    return [center + r * np.array([np.cos(a), np.sin(a)]) for a in angles]


def _external_tangents(c1, r1, c2, r2):
    """Return two external common-tangent segments as ((p1a, p2a), (p1b, p2b)).

    Each segment goes from a tangent point on circle 1 to the corresponding
    tangent point on circle 2. r1 may equal r2 (parallel tangents).
    """
    c1 = np.asarray(c1, dtype=float)
    c2 = np.asarray(c2, dtype=float)
    d_vec = c2 - c1
    d = np.linalg.norm(d_vec)
    if d == 0:
        return []
    # angle of center-line
    theta = np.arctan2(d_vec[1], d_vec[0])
    # angle between center-line and tangent on each circle
    ratio = (r1 - r2) / d
    if abs(ratio) > 1:
        # one circle contains the other — no external tangent
        return []
    alpha = np.arcsin(ratio)
    # Tangent points: rotate the perpendicular (theta + pi/2) by ±alpha
    segments = []
    for sign in (+1, -1):
        perp = np.array([-np.sin(theta), np.cos(theta)]) * sign
        # rotate perp by -alpha around z:
        ca, sa = np.cos(alpha), np.sin(alpha)
        # rotated perp = ca*perp + sa*(-along) where along=(cos theta, sin theta)
        along = np.array([np.cos(theta), np.sin(theta)])
        n = ca * perp - sa * along
        p1 = c1 + r1 * n
        p2 = c2 + r2 * n
        segments.append((p1, p2))
    return segments


class PairedSizeLegend(Artist):
    """Size legend with two circles (min, max) connected by lines.

    Parameters
    ----------
    sizes : array-like
        Sizes in point**2 (same unit as :meth:`Axes.scatter` ``s=``). Only the
        min and max are used for the circles; intermediate values are ignored.
    ax : :class:`Axes <matplotlib.axes.Axes>`, optional
        Target axes (default ``plt.gca()``).
    labels : 2-tuple of str, optional
        ``(min_label, max_label)`` to use literally. Defaults to formatted
        min/max of ``array`` (or ``sizes`` if ``array`` is None).
    array : array-like, optional
        Data array used to derive label values when ``labels`` is None.
    fmt : str or :class:`Formatter <matplotlib.ticker.Formatter>`, optional
        Format spec for labels. Strings use ``StrMethodFormatter`` (``"{x:.1f}"``).
    func : callable, default: identity
        Applied to array values before formatting.
    orientation : {"horizontal", "vertical"}, default: "horizontal"
        Layout direction of the two circles.
    reverse : bool, default: False
        Swap min/max position (max comes first along the layout axis).
    connector : {"tangent", "center", "none"}, default: "tangent"
        Line(s) connecting the two circles.

        - ``"tangent"``: two external common tangents, touching each circle's
          edge.
        - ``"center"``: single straight line through both centers, clipped to
          the circle edges (visible only in the gap between circles).
        - ``"none"``: no connector.
    label_loc : str, default: "auto"
        Where to place labels relative to circles. Options:
        ``"auto"`` (below for horizontal, right for vertical), ``"above"``,
        ``"below"``, ``"left"``, ``"right"``, ``"center"`` (label at circle
        center), ``"none"`` (no labels).
    color : color, default: "black"
        Default for both facecolor and edgecolor.
    facecolor, edgecolor : color, optional
        Override ``color`` for fill / outline.
    linewidth : float, default: 1.0
        Line width of circle outline and connectors.
    fill : bool, default: True
        Whether to fill circles. If False, only outline drawn.
    alpha : float, optional
        Opacity.
    gap : float, optional
        Extra gap (in points) between the two circles. Defaults to
        ``max(8, 0.3 * d_max)`` where ``d_max`` is the big circle diameter.
    title : str, optional
        Legend title.
    title_fontsize, title_fontproperties : optional
        Title font controls.
    prop, fontsize : optional
        Label font controls.
    alignment : {"center", "left", "right"}, default: "center"
        Alignment of title vs. body.
    loc : str, default: "upper right"
        Anchor location (supports ``"out *"`` prefixes via :class:`Locs`).
    deviation : float, default: 0.05
        Outside-anchor offset.
    bbox_to_anchor, bbox_transform : optional
        Standard offsetbox anchor arguments.
    borderpad, borderaxespad : optional
        Standard legend pad arguments (in font-size units).
    frameon : bool, default: False
        Draw frame around the legend box.
    textpad : float, optional
        Pad between circles and labels (font-size units). Defaults to
        rcParams legend.handletextpad.

    Examples
    --------
    .. plot::
        :context: close-figs

        >>> import numpy as np, matplotlib.pyplot as plt
        >>> from legendkit import paired_size_legend
        >>> _, ax = plt.subplots(figsize=(3, 2)); ax.set_axis_off()
        >>> paired_size_legend([10, 1000], ax=ax)
    """

    def __repr__(self):
        return "<PairedSizeLegend>"

    def __init__(
        self,
        sizes,
        *,
        ax=None,
        labels=None,
        array=None,
        fmt=None,
        func=lambda x: x,
        orientation="horizontal",
        reverse=False,
        connector="tangent",
        fill_between=True,
        fill_between_alpha=0.7,
        label_loc="auto",
        color="black",
        facecolor=None,
        edgecolor=None,
        linewidth=1.0,
        fill=True,
        alpha=None,
        gap=None,
        title=None,
        title_fontsize=None,
        title_fontproperties=None,
        prop=None,
        fontsize=None,
        alignment="center",
        loc=None,
        deviation=0.05,
        bbox_to_anchor=None,
        bbox_transform=None,
        borderpad=None,
        borderaxespad=None,
        textpad=None,
        frameon=False,
        draw=True,
    ):
        super().__init__()
        self._draw = draw  # store early — used immediately below

        if orientation not in _ORIENT_OPTIONS:
            raise ValueError(f"`orientation` must be one of {_ORIENT_OPTIONS}")
        if connector not in _CONNECTOR_OPTIONS:
            raise ValueError(f"`connector` must be one of {_CONNECTOR_OPTIONS}")
        if label_loc not in _LABEL_LOC_OPTIONS:
            raise ValueError(f"`label_loc` must be one of {_LABEL_LOC_OPTIONS}")

        _headless = ax is None and not self._draw
        if ax is None and self._draw:
            ax = plt.gca()
        self.is_axes = isinstance(ax, Axes) if ax is not None else False
        if _headless:
            # No axes yet — figure will be set when added to a stack.
            self.figure = None
            self.axes = None
        elif self.is_axes:
            self.axes = ax
            self.figure = ax.figure
        else:
            self.figure = ax
            self.axes = None

        # ---- sizes / labels ----
        sizes = np.asarray(sizes, dtype=float).flatten()
        if sizes.size < 2:
            raise ValueError("`sizes` must contain at least 2 values")
        if np.any(sizes < 0):
            raise ValueError("`sizes` must be non-negative (point**2)")
        s_min, s_max = float(np.min(sizes)), float(np.max(sizes))

        if array is None:
            array = sizes
        array = np.asarray(array).flatten()
        a_min = func(np.min(array))
        a_max = func(np.max(array))

        if labels is None:
            if fmt is None:
                # Default: short {:.3g} — significant-digit format keeps both
                # ints and floats compact (e.g. 9.93, 497, 1e3).
                def _fmt(v):
                    return f"{v:.3g}"

                _label_fmt = _fmt
            elif isinstance(fmt, str):
                _label_fmt = ticker.StrMethodFormatter(fmt)
            else:
                _label_fmt = fmt
            min_label = (
                _label_fmt(a_min)
                if callable(_label_fmt)
                else _label_fmt.format_data(a_min)
            )
            max_label = (
                _label_fmt(a_max)
                if callable(_label_fmt)
                else _label_fmt.format_data(a_max)
            )
        else:
            if len(labels) != 2:
                raise ValueError("`labels` must be a 2-tuple (min_label, max_label)")
            min_label, max_label = str(labels[0]), str(labels[1])

        # ---- colors / style ----
        if facecolor is None:
            facecolor = color
        if edgecolor is None:
            edgecolor = color
        self._fc = facecolor if fill else "none"
        self._ec = edgecolor
        self._lw = linewidth
        self._alpha = alpha

        # ---- font ----
        if fontsize is None:
            fontsize = mpl.rcParams["legend.fontsize"]
        if prop is None:
            self.prop = FontProperties(size=fontsize)
        else:
            self.prop = FontProperties._from_any(prop)
        self._fontsize = self.prop.get_size_in_points()

        if title_fontsize is None:
            title_fontsize = mpl.rcParams["legend.title_fontsize"]
        self._title_fontsize = title_fontsize
        self._title_fontproperties = title_fontproperties
        self._title = title

        if textpad is None:
            textpad = mpl.rcParams["legend.handletextpad"]
        self.textpad = textpad
        if borderpad is None:
            borderpad = mpl.rcParams["legend.borderpad"]
        self.borderpad = borderpad
        if borderaxespad is None:
            borderaxespad = mpl.rcParams["legend.borderaxespad"]
        self.borderaxespad = borderaxespad
        self.alignment = alignment
        self.frameon = frameon

        # ---- loc ----
        if loc is None:
            loc = "upper right"
        if ax is not None:
            self._loc, self._bbox_to_anchor, self._bbox_transform = Locs().transform(
                ax,
                loc,
                bbox_to_anchor=bbox_to_anchor,
                bbox_transform=bbox_transform,
                deviation=deviation,
            )
        else:
            # Headless (draw=False, ax=None) — loc params unused; stack will
            # position the legend via its own AnchoredOffsetbox.
            self._loc = loc
            self._bbox_to_anchor = bbox_to_anchor
            self._bbox_transform = bbox_transform

        # ---- geometry ----
        # diameters in points
        d_min = float(np.sqrt(s_min))
        d_max = float(np.sqrt(s_max))
        r_min, r_max = d_min / 2, d_max / 2
        # rough label width in points (0.6 * fontsize per char is a reasonable
        # mono-ish estimate; refined later by matplotlib via offsetbox).
        approx_char_w = 0.6 * self._fontsize
        max_label_w = approx_char_w * max(len(min_label), len(max_label))
        if gap is None:
            # default gap: enough so the two labels don't collide when stacked
            # below circles (label width straddles each circle center).
            gap = max(8.0, 0.3 * d_max, max_label_w + 4.0)
        self._gap = gap
        self._approx_label_w = max_label_w

        # resolve label location
        if label_loc == "auto":
            label_loc = "below" if orientation == "horizontal" else "right"
        self._label_loc = label_loc
        self._orientation = orientation
        self._reverse = reverse
        self._connector = connector
        self._sizes_pair = (s_min, s_max)
        self._radii = (r_min, r_max)
        self._labels_pair = (min_label, max_label)
        self._fill_between = fill_between and connector == "tangent"
        self._fill_between_alpha = fill_between_alpha

        self._make_box()

    # ------------------------------------------------------------------
    # build
    # ------------------------------------------------------------------
    def _make_box(self):
        r_min, r_max = self._radii
        d_max = 2 * r_max
        gap = self._gap
        orientation = self._orientation
        reverse = self._reverse

        # which circle is on the "first" side along layout axis
        if not reverse:
            first_r, second_r = r_min, r_max
            first_label, second_label = self._labels_pair
        else:
            first_r, second_r = r_max, r_min
            first_label, second_label = self._labels_pair[1], self._labels_pair[0]

        # center-to-center distance: first_r + gap + second_r
        center_dist = first_r + gap + second_r

        if orientation == "horizontal":
            # both centers share y = d_max/2 (so big circle fits)
            cy = d_max / 2
            c1 = np.array([first_r, cy])
            c2 = np.array(
                [first_r + gap + 2 * second_r if False else first_r + center_dist, cy]
            )
            # width / height of drawing canvas
            da_w = c2[0] + second_r
            da_h = d_max
        else:  # vertical — first at bottom or top? Convention: "first" at bottom (small bottom = grows up).
            # But matching matplotlib coords (y up), put first at bottom.
            cx = d_max / 2
            c1 = np.array([cx, first_r])
            c2 = np.array([cx, first_r + center_dist])
            da_w = d_max
            da_h = c2[1] + second_r

        canvas = DrawingArea(da_w, da_h, clip=False)
        if self.figure is not None:
            canvas.set_figure(self.figure)

        # circles
        circ1 = Circle(
            c1, radius=first_r, fc=self._fc, ec=self._ec, lw=self._lw, alpha=self._alpha
        )
        circ2 = Circle(
            c2,
            radius=second_r,
            fc=self._fc,
            ec=self._ec,
            lw=self._lw,
            alpha=self._alpha,
        )

        # connector lines
        line_segments = []
        hull_poly = None
        if self._connector == "tangent":
            if self._fill_between:
                hull = _tangent_hull(c1, first_r, c2, second_r)
                if hull is not None:
                    # Use the facecolor (fall back to edgecolor if circles
                    # are outline-only) for the hull fill.
                    fill_c = self._fc if self._fc != "none" else self._ec
                    hull_poly = Polygon(
                        hull,
                        closed=True,
                        fc=fill_c,
                        ec="none",
                        alpha=self._fill_between_alpha,
                    )
            else:
                segs = _external_tangents(c1, first_r, c2, second_r)
                for p1, p2 in segs:
                    line_segments.append([p1.tolist(), p2.tolist()])
        elif self._connector == "center":
            # center-to-center, clipped at circle edges
            d_vec = c2 - c1
            d = np.linalg.norm(d_vec)
            if d > 0:
                u = d_vec / d
                p1 = c1 + first_r * u
                p2 = c2 - second_r * u
                line_segments.append([p1.tolist(), p2.tolist()])

        # add: hull (if any) below circles so circle outlines crisp on top
        if hull_poly is not None:
            canvas.add_artist(hull_poly)
        patches = PatchCollection([circ1, circ2], match_original=True)
        canvas.add_artist(patches)

        if line_segments:
            lc = LineCollection(
                line_segments, colors=self._ec, linewidths=self._lw, alpha=self._alpha
            )
            canvas.add_artist(lc)

        # label centers should hit circle centers — TextAreas can't, so we
        # build the label row/column separately and pack via HPacker/VPacker.
        body = self._pack_with_labels(canvas, first_label, second_label, c1, c2)

        if self._title is not None:
            if self._title_fontproperties is None:
                title_props = dict(fontweight="bold", fontsize=self._title_fontsize)
            elif isinstance(self._title_fontproperties, dict):
                # pass keys directly to Text — fontsize/fontweight/color are
                # valid Text kwargs, but NOT valid FontProperties kwargs, so we
                # must NOT nest them under a 'fontproperties' key.
                title_props = dict(self._title_fontproperties)
            else:
                title_props = dict(fontproperties=self._title_fontproperties)
            title_area = TextArea(self._title, textprops=title_props)
            if self.figure is not None:
                title_area.set_figure(self.figure)
            final = VPacker(
                pad=0,
                sep=0.4 * self._fontsize,
                children=[title_area, body],
                align=self.alignment,
            )
            if self.figure is not None:
                final.set_figure(self.figure)
        else:
            final = body
        self._final_pack = final

        self._box = AnchoredOffsetbox(
            self._loc,
            child=final,
            pad=self.borderpad,
            borderpad=self.borderaxespad,
            bbox_transform=self._bbox_transform,
            bbox_to_anchor=self._bbox_to_anchor,
            frameon=self.frameon,
        )
        if self.figure is not None:
            self._box.set_figure(self.figure)

        if self._draw:
            if self.is_axes:
                self.axes.add_artist(self._box)
            else:
                self.figure.add_artist(self._box)

    def _pack_with_labels(self, canvas, first_label, second_label, c1, c2):
        """Place labels relative to the circle canvas using offsetboxes.

        For "above"/"below"/"left"/"right" we build a small two-column-or-row
        TextArea row and stack with VPacker/HPacker so labels visually land
        under their circle. For "center" we draw text inside the canvas; for
        "none" no label. For "outside" we put labels at the far ends.
        """
        from matplotlib.text import Text

        loc = self._label_loc
        sep = self.textpad * self._fontsize
        text_props = dict(fontproperties=self.prop)

        if loc == "none":
            return canvas

        if loc == "center":
            # draw text inside circles
            for c, label in zip((c1, c2), (first_label, second_label)):
                t = Text(
                    c[0],
                    c[1],
                    label,
                    ha="center",
                    va="center",
                    fontsize=self._fontsize,
                    fontproperties=self.prop,
                )
                canvas.add_artist(t)
            return canvas

        # ------- align labels with their circle centers via per-side panels ----
        # Strategy: build a second DrawingArea same size as canvas containing
        # two Text artists positioned at the circle x or y. Stack it with the
        # circle canvas using VPacker (for above/below) or HPacker.

        def _make_label_strip(axis):
            """axis='x' positions labels horizontally at c1.x/c2.x; 'y' vertically."""
            if axis == "x":
                # Strip must extend past the canvas edges if a label centered
                # on circle 1 (at x=c1.x) is wider than 2*c1.x; same on right.
                half_lw = self._approx_label_w / 2
                left_overhang = max(0.0, half_lw - c1[0])
                right_overhang = max(0.0, (c2[0] + half_lw) - canvas.width)
                w = canvas.width + left_overhang + right_overhang
                h = self._fontsize * 1.4
                strip = DrawingArea(w, h, clip=False)
                if self.figure is not None:
                    strip.set_figure(self.figure)
                # Note: strip is stacked with canvas via VPacker(align="center"),
                # so its content x-coords align with canvas content shifted by
                # left_overhang. Shift label positions accordingly.
                for c, label in zip((c1, c2), (first_label, second_label)):
                    t = Text(
                        c[0] + left_overhang,
                        h / 2,
                        label,
                        ha="center",
                        va="center",
                        fontsize=self._fontsize,
                        fontproperties=self.prop,
                    )
                    strip.add_artist(t)
                # Stash so we can shift canvas if alignment matters.
                strip._left_overhang = left_overhang
                return strip
            else:
                w = max(self._approx_label_w + 4.0, self._fontsize * 2)
                h = canvas.height
                strip = DrawingArea(w, h, clip=False)
                if self.figure is not None:
                    strip.set_figure(self.figure)
                for c, label in zip((c1, c2), (first_label, second_label)):
                    # When loc == "left", anchor at right edge (ha="right");
                    # when loc == "right", anchor at left (ha="left").
                    ha = "left" if loc == "right" else "right"
                    x_anchor = 0 if ha == "left" else w
                    t = Text(
                        x_anchor,
                        c[1],
                        label,
                        ha=ha,
                        va="center",
                        fontsize=self._fontsize,
                        fontproperties=self.prop,
                    )
                    strip.add_artist(t)
                return strip

        if loc == "below":
            strip = _make_label_strip("x")
            pack = VPacker(pad=0, sep=sep, children=[canvas, strip], align="center")
        elif loc == "above":
            strip = _make_label_strip("x")
            pack = VPacker(pad=0, sep=sep, children=[strip, canvas], align="center")
        elif loc == "right":
            strip = _make_label_strip("y")
            pack = HPacker(pad=0, sep=sep, children=[canvas, strip], align="center")
        elif loc == "left":
            strip = _make_label_strip("y")
            pack = HPacker(pad=0, sep=sep, children=[strip, canvas], align="center")
        elif loc == "outside":
            # labels at the two ends of the layout axis
            # horizontal: first label left of small circle, second right of big
            # vertical: first label below first circle, second above second
            if self._orientation == "horizontal":
                left_area = TextArea(first_label, textprops=text_props)
                right_area = TextArea(second_label, textprops=text_props)
                pack = HPacker(
                    pad=0,
                    sep=sep,
                    children=[left_area, canvas, right_area],
                    align="center",
                )
            else:
                top_area = TextArea(second_label, textprops=text_props)
                bot_area = TextArea(first_label, textprops=text_props)
                pack = VPacker(
                    pad=0,
                    sep=sep,
                    children=[top_area, canvas, bot_area],
                    align="center",
                )
        else:
            pack = canvas

        if self.figure is not None:
            pack.set_figure(self.figure)
        return pack

    # ------------------------------------------------------------------
    # Artist protocol — delegate to offsetbox
    # ------------------------------------------------------------------
    def get_bbox(self, renderer=None):
        return self._final_pack.get_bbox(renderer=renderer)

    def get_window_extent(self, renderer=None):
        return self._box.get_window_extent(renderer=renderer)

    def set_offset(self, offset):
        self._final_pack.set_offset(offset)

    def get_children(self):
        return [self._box]

    def remove(self):
        self._box.remove()
