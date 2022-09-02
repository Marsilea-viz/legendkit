project = 'legendkit'
copyright = '2022, Mr-Milk'
author = 'Mr-Milk'
release = '0.2.0'

extensions = [
    'sphinx_gallery.gen_gallery',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'matplotlib.sphinxext.plot_directive'
]

sphinx_gallery_conf = {
    'examples_dirs': 'examples',  # path to your example scripts
    'gallery_dirs': 'gallery_examples',  # path to where to save gallery generated output
    # 'image_scrapers': (matplotlib_svg_scraper(),),
    # 'image_srcset': ["2x"],
}
# setting autosummary
autosummary_generate = True

# setting plot direction
plot_include_source = True
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ['svg']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ['_static']
html_favicon = "../../images/legendkit-logo.svg"
