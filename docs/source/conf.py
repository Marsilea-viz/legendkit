project = 'legendkit'
copyright = '2022, Mr-Milk'
author = 'Mr-Milk'
release = '0.2.6'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'matplotlib.sphinxext.plot_directive',
    'numpydoc',
    'sphinx.ext.intersphinx',
]

# setting autosummary
autosummary_generate = True

# setting plot direction
plot_include_source = True
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ['svg']
plot_pre_code = "import numpy as np; from matplotlib import pyplot as plt;" \
                "import matplotlib as mpl; np.random.seed(0);" \
                "mpl.rcParams['savefig.bbox'] = 'tight';" \
                "plt.style.use('https://github.com/dhaitz/" \
                "matplotlib-stylesheets/raw/master/pacoty.mplstyle');"

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ['_static']
html_favicon = "../../images/legendkit-logo.svg"

intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org/stable', None),
}
