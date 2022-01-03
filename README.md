# Introduction

This repository contains several filters to
be used with [Pandoc](https://pandoc.org/), the excellent document processing system that converts several text markup formats. These [Pandoc filters](https://pandoc.org/filters.html) were created in Python using the [Panflute library](http://scorreia.com/software/panflute/) and are called by Pandoc during the conversion process, resulting in transformations of the final source. Several useful filters can be found at:

* [Pandoc Filters](https://github.com/jgm/pandoc/wiki/Pandoc-Filters)
* [jgm/pandocfilters: A python module for writing pandoc filters, with a collection of examples](https://github.com/jgm/pandocfilters)
* [sergiocorreia/panflute-filters: Pandoc filters that use Panflute](https://github.com/sergiocorreia/panflute-filters)
* [pandoc/lua-filters: A collection of lua filters for pandoc](https://github.com/pandoc/lua-filters)
* [ickc/pantable: CSV Tables in Markdown: Pandoc Filter for CSV Tables](https://github.com/ickc/pantable)
 
# Available filters

In short, the filters in this repo are:

1. `adoc-admonitions.py`
	* Simplified syntax to create admonition boxes to present notes, warnings, tips, etc.
2. `beamer-twocol.py`
	* Specific for generating slides with [LaTeX beamer](https://ctan.org/pkg/beamer?lang=en), adding an easier syntax to create content in two columns
3. `divs-to-latex.py`
	* This is a LaTeX (beamer) specific filter transforming Markdown's fenced Divs into latex environments. An alternative is [chdemko/pandoc-latex-environment: Pandoc filter for adding LaTeX environment on specific div](https://github.com/chdemko/pandoc-latex-environment)
4. `super-links.py`
   * Facilitate the creation of links using a configurable and alternative syntax 


## Installation

1. Install python 3 (version >3.9 required) and pandoc

2. Install Panflute python libraries

    	pip3 install panflute

3. Download and place the file in directory:

    	~/.pandoc/filters
	* See [Pandoc User’s Guide](https://pandoc.org/MANUAL.html) instructions at (`-F PROGRAM, --filter=PROGRAM`)

## Usage in pandoc

    pandoc -s test.md  -t beamer --filter adoc-admonitions.py
    pandoc -s test.md  -t html -F super-links.py

* See [Pandoc User’s Guide](https://pandoc.org/MANUAL.html) instructions at (`-F PROGRAM, --filter=PROGRAM`)


# Author

    Prof. Georgios Pappas Jr
    University of Brasilia (UnB) - Brazil