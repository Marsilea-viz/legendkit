Colorbar Creation
=================

The colorbar in legendkit is similar to matplotlib's colorbar,
you can change the shape of the colorbar.

.. plot::
    :context: close-figs

    >>> from legendkit import colorbar
    >>> _, ax = plt.subplots()
    >>> m = np.random.randn(10, 10)
    >>> mappable = ax.pcolormesh(m, cmap="Wistia")
    >>> colorbar(mappable, loc="out right upper", shape="ellipse")
    >>> colorbar(mappable, ax=ax, orientation="horizontal", loc="out upper center")
    >>> colorbar(mappable, ax=ax, loc="out right lower", shape="triangle")


When to use ``colorart`` vs ``colorbar``
-----------------------------------------

Both produce a colorbar-like element, but they differ in one important way:

- **colorbar** — wraps matplotlib's built-in ``Colorbar`` and is drawn on a
  dedicated inset axes. Use it when you want a standalone colorbar without
  needing to group it with other legends.

- **colorart** — is a pure ``Artist`` (no inset axes). Because it is an Artist,
  it can be passed directly to :func:`vstack` / :func:`hstack` together with
  legends. Use it when you need to arrange multiple colorbars and legends into a
  single composite layout.

**Quick rule:** If you only need a colorbar → use ``colorbar``.
If you need to stack it with legends → use ``colorart``.

Legendkit also provides the ``colorart`` Artist-based implementation of colorbar,
useful when laying out multiple legends and colorbars together.

.. plot::
    :context: close-figs

    >>> from legendkit import colorart
    >>> _, ax = plt.subplots()
    >>> m = np.random.randn(10, 10)
    >>> mappable = ax.pcolormesh(m, cmap="cool")
    >>> colorart(mappable, ax=ax, loc="out right center")