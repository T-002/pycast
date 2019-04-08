#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuration for the Sphinx documentation."""

import sphinx_bootstrap_theme

extensions = [
    'sphinx.ext.autodoc',
#    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
#    'sphinx.ext.coverage',
#    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon',
    'sphinxcontrib.confluencebuilder'
]

templates_path = ['doc/_templates']
source_suffix = '.rst'
master_doc = 'readme'

# General information about the project.
project = "pycast - A Python Forecasting and Smoothing Library"
copyright = "2015-2019, Christian Schwarz"
author = "Christian Schwarz"

version = "0"
release = "1"

language = None

autosummary_generate = True
exclude_patterns = []
pygments_style = 'sphinx'

todo_include_todos = True

# -- Options for HTML output
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

html_static_path = ['doc/_static']
html_logo = "doc/_static/logo.png"
html_favicon = "doc/_static/favicon.ico"
html_show_sphinx = False

# Output file base name for HTML help builder.
htmlhelp_basename = 'pycast'

# Bootstrap Template
html_theme_options = {
    "navbar_site_name": "Sub Pages",
    "navbar_sidebarrel": False,
    "navbar_pagenav": True,
    "navbar_pagenav_name": "This Page",

    "globaltoc_depth": 1,
    "globaltoc_includehidden": "true",
    "navbar_fixed_top": "true",
    "source_link_position": "nav",
    "bootstrap_version": "3",
}
