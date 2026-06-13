import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

from legendkit import (
    cat_legend,
    colorart,
    legend,
    paired_size_legend,
    size_legend,
    hstack,
    vstack,
)

mpl.rcParams["legend.handleheight"] = 1
mpl.rcParams["legend.handlelength"] = 1
mpl.rcParams["legend.labelspacing"] = 0.3
mpl.rcParams["legend.fontsize"] = 8
mpl.rcParams["legend.title_fontsize"] = 9

CAT4 = ["#7A76C2", "#f62196", "#18c0c4", "#f3907e"]
CAT2 = CAT4[:2]
ACCENT = "#0089A7"
TITLE_KW = {"fontsize": 8, "fontweight": 600}
TITLE_FP = {"size": 8, "weight": 600}

norm = Normalize(vmin=0, vmax=10)
sizes = np.array([10, 40, 100])

fig, ax = plt.subplots(figsize=(3, 3))
ax.set_axis_off()
T = ax.transAxes

_cat = cat_legend(
    colors=CAT4,
    labels=["Alpha", "Beta", "Gamma", "Delta"],
    handle="circle",
    title="category",
    title_fontproperties=TITLE_FP,
    draw=False,
)
_leg = legend(
    legend_items=[
        ("square", "L1", {"color": CAT4[0]}),
        ("circle", "L2", {"color": CAT4[1]}),
        ("triangle", "L3", {"color": CAT4[2]}),
        ("line", "L4", {"color": CAT4[3]}),
    ],
    title="legend",
    title_fontproperties=TITLE_FP,
    draw=False,
)
_siz = size_legend(
    sizes,
    num_handle=3,
    handle="circle",
    colors=[ACCENT] * len(sizes),
    title="size",
    title_fontproperties=TITLE_FP,
    draw=False,
)
_normal_legs = hstack([_cat, _leg, _siz], spacing=8)
_ph = paired_size_legend(
    sizes,
    orientation="horizontal",
    fill_between=True,
    fill_between_alpha=0.65,
    color=ACCENT,
    title="size",
    title_fontproperties=TITLE_KW,
    draw=False,
)
_pv = paired_size_legend(
    sizes,
    orientation="vertical",
    fill_between=True,
    fill_between_alpha=0.65,
    color=CAT4[1],
    label_loc="right",
    title="size",
    title_fontproperties=TITLE_KW,
    draw=False,
)
_paired_legs = hstack([_ph, _pv], spacing=8)

_cr = colorart(
    norm=norm,
    cmap="viridis",
    ax=ax,
    orientation="horizontal",
    title="colorbar",
    title_fontproperties=TITLE_KW,
)

_vs = vstack(
    [_normal_legs, _paired_legs, _cr],
    title="What's in legendkit?",
    spacing=8,
    title_fontproperties=TITLE_KW,
    align="center",
    ax=ax,
)
