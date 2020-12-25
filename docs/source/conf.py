# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('../../..'))
sys.path.insert(0, os.path.abspath('..'))
# sys.path.append('/Users/russgarner/OneDrive/Python/lookml_project/lookml')


# -- Project information -----------------------------------------------------

project = 'pylookml'
copyright = '2020, Russell Garner'
author = 'Russell Garner'

# The full version, including alpha/beta/rc tags
release = '2.0.0'

#P0: Things to doc:
# Iteration
# subscriptability
# subclassing
# primary key accessor _View__pk
# removing properties (del obj.prop)
# _json() method
# which properties del and which .remove() i.e. anonymous plural constructs
# How to use the lang map generator
# Updated EAV
# How to create a new model file
# How to load a project from the filestystem
# Omitting defaults
# logging issues to a csv
# dim.filters + {'view.field':'>1'}
# adding and subtracting properties
# view + 'sql_table_name: order_items ;;'
# view - 'sql_table_name'
# x.foo.setName_replace_references('bar')
# 


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx.ext.autodoc', 
    'sphinx.ext.coverage',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
# html_theme = 'nature'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'
