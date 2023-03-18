Layout multiple legends
=======================

When you have multiple legends that you want to group
in a plot, manually adjust the position to avoid
overlapping would be too tedious.

Use legendkit layout features to help you out.

.. plot::
    :context: close-figs

    >>> from legendkit import cat_legend, vstack, hstack
    >>> _, ax = plt.subplots(figsize=(6, 3)); ax.set_axis_off()
    >>> args = dict(
    ...     colors = ["#A7D2CB", "#F2D388"],
    ...     labels = ["Item 1", "Item 2"],
    ... )
    >>> legends = [cat_legend(**args, title=f"Legend {i+1}") for i in range(6)]
    >>> vstack(legends[0:3], title="Stack Vertically",
    ...        loc="upper left", spacing=10, frameon=True, ax=ax)
    >>> hstack(legends[3:6], title="Stack Horizontally",
    ...        loc="upper right", spacing=10, frameon=True, ax=ax)


It's also possible to create complex layout by stack other stacks.

.. plot::
    :context: close-figs

    >>> _, ax = plt.subplots(figsize=(1, 3)); ax.set_axis_off()
    >>> legends = [cat_legend(**args, title=f"Legend {i+1}") for i in range(6)]
    >>> vs = vstack(legends[0:3], spacing=10)
    >>> hs = hstack(legends[3:6], spacing=10)
    >>> hstack([vs, hs], spacing=20, title="Stack of stacks",
    ...        frameon=True, align="center", ax=ax)

Apart from legends, you can stack both legends and colorart. You cannot layout colorbar since it's
actually an axes.

.. plot::
    :context: close-figs

    >>> from legendkit import colorart
    >>> _, ax = plt.subplots(figsize=(1, 3)); ax.set_axis_off()
    >>> m = np.random.randn(10, 2)
    >>> mappable = ax.pcolormesh(m, cmap="cool")
    >>> cbar = colorart(mappable, ax=ax, title="Colorart")
    >>> legend = cat_legend(**args, title="Legend")
    >>> vstack([legend, cbar], spacing=10, title="Stack Legend and Colorart",
    ...        alignment="left", loc="out right center", frameon=False, ax=ax)