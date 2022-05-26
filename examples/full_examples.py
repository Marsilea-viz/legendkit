import matplotlib.pyplot as plt
from legendkit import ListLegend, Colorbar, EllipseColorbar, hstack, vstack

legend_items=[
        ('square', 'L1', {'color': "#e76f51"}),
        ('circle', 'L2', {'color': "#2a9d8f"}),
        ('rect', 'L3', {'color': "#e9c46a"}),
    ]
fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
legend1 = ListLegend(legend_items=legend_items, title="Title Left", title_align="left")
legend2 = ListLegend(legend_items=legend_items, title="Title Center", title_align="center")
legend3 = ListLegend(legend_items=legend_items, title="Title Right", title_align="right")

s1 = hstack([legend1, legend2, legend3], spacing=30, frameon=True, title="Stack 3 Legends Horizontally")
ax.add_artist(s1)

legend1 = ListLegend(legend_items=legend_items, title="Title Top", title_pos="top", title_align="left")
legend2 = ListLegend(legend_items=legend_items, title="Title Bottom", title_pos="bottom", title_align="left")
legend3 = ListLegend(legend_items=legend_items, title="Title Right", title_pos="right", ncol=3)
legend4 = ListLegend(legend_items=legend_items, title="Title Left", title_pos="left", ncol=3)

s2 = vstack([legend1, legend2, legend3, legend4], spacing=20, frameon=True, loc="upper left", title="Stack 3 Legends Vertically")
ax.add_artist(s2)

Colorbar(vmin=0, vmax=10, title="Colorbar", title_align="left")
Colorbar(vmin=0, vmax=10, title="Colorbar", title_align="left", orientation="horizontal",
             bbox_to_anchor=(1.3, 0.5, 0, 0), bbox_transform=ax.transAxes)

EllipseColorbar(vmin=0, vmax=10, cmap="RdBu", bbox_to_anchor=(1.05, 0, 0, 0), title="Ellipse Colorbar", title_align="left",
                    loc="lower left", bbox_transform=ax.transAxes)

EllipseColorbar(vmin=0, vmax=10, cmap="RdBu", bbox_to_anchor=(1.3, 0, 0, 0), title="Ellipse Colorbar", title_align="left",
                    orientation="horizontal",
                    loc="lower left", bbox_transform=ax.transAxes)


plt.savefig("images/showcase.svg", bbox_inches="tight")
