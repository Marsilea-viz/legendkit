import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

from legendkit import legend, cat_legend, colorbar, colorart, hstack, vstack, size_legend

mpl.rcParams['legend.handleheight'] = 1
mpl.rcParams['legend.handlelength'] = 1
mpl.rcParams['legend.labelspacing'] = .3

legend_items = [
    ('square', 'L1', {'color': "#e76f51"}),
    ('circle', 'L2', {'color': "#2a9d8f"}),
    ('triangle', 'L3', {'color': "#e9c46a"}),
]

fig, ax = plt.subplots(figsize=(5.5, 6))
legend1 = legend(legend_items=legend_items,
                 title="Title Left",
                 alignment="left")
legend2 = legend(legend_items=legend_items,
                 title="Title Center",
                 alignment="center")
legend3 = legend(legend_items=legend_items,
                 title="Title Right",
                 alignment="right")

s1 = hstack([legend1, legend2, legend3], spacing=30,
            title="Stack Horizontally")

legend1 = legend(legend_items=legend_items, title="Title Top",
                 title_loc="top", alignment="left")
legend2 = legend(legend_items=legend_items, title="Title Bottom",
                 title_loc="bottom", alignment="left")
legend3 = legend(legend_items=legend_items, title="Title Right",
                 title_loc="right", ncol=3)
legend4 = legend(legend_items=legend_items, title="Title Left",
                 title_loc="left", ncol=3)

hs = hstack([legend1, legend2], spacing=30)
vs = vstack([legend3, legend4], spacing=20)

s2 = vstack([hs, vs],
            spacing=20, align="center",
            title="Stack Vertically")

s3 = vstack([s1, s2], spacing=30, frameon=True, align="center",
            loc="upper left",
            title="Stack of Stacks of legends", ax=ax,
            title_fontproperties={"fontsize": 14, "fontweight": 600,
                                  "color": "#0089A7"})

norm = Normalize(vmin=0, vmax=10)

colorbar(ax=ax, norm=norm,
         orientation="horizontal",
         title="Colorbar", alignment="left",
         loc="upper left", bbox_to_anchor=(1, 0.4),
         bbox_transform=ax.transAxes)

colorbar(ax=ax, norm=norm,
         orientation="horizontal",
         shape="ellipse", cmap="RdBu",
         title="Ellipse Colorbar", alignment="left",
         loc="upper left", bbox_to_anchor=(1, 0.2),
         bbox_transform=ax.transAxes)

colorbar(ax=ax, norm=norm,
         orientation="horizontal",
         shape="triangle", cmap="PuRd",
         title="Triangle Colorbar", alignment="left",
         loc="upper left", bbox_to_anchor=(1.4, 0.4),
         bbox_transform=ax.transAxes)

colorbar(ax=ax, norm=norm,
         orientation="horizontal",
         shape="trapezoid", cmap="coolwarm",
         title="Trapezoid Colorbar", alignment="left",
         loc="upper left", bbox_to_anchor=(1.4, 0.2),
         bbox_transform=ax.transAxes)

args = dict(
    colors=["#A7D2CB", "#F2D388", "#A7D2CB", "#F2D388"],
    labels=["Item 1", "Item 2", "Item 3", "Item 4"],
)
legend1 = cat_legend(**args, title="Category", handle="circle")
legend2 = size_legend(sizes=np.arange(1, 401), title="Size", handle="circle")
cart = colorart(norm=norm, cmap="cool", ax=ax, title="Colorart")
hstack([legend1, legend2, cart], spacing=20, title="Stack colorbar and legend",
       alignment="left",
       loc="upper left", bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes,
       frameon=True, ax=ax, padding=2)

ax.set_axis_off()
