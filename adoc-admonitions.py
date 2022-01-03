#!/usr/bin/env python3

"""
Pandoc filter that processes asciidoc-style admonitions and encloses them in a DIV with
a specified class

The admonitions are uppercase words appearing in the first column of a paragraph followed by a
colon (:) and a space. For example:

NOTE: this is a note

These are invalid:

NOTE:this  (no space after the colon)

 NOTE: this (not in the first column)

The default admonition names/classes are coded in the LINKS dictionary. This can be overriden or
expanded using a metadata block in markdown with the name `adoc-admonition`:

    ---
    adoc-admonition:
        xxx: admonitionnote
        TIP: TIPADMONITION
...

With that in place, the changes will be:

    xxx: xxx enclosed in a admonitionnote Div

    TIP: overrides the default class and sets the new one as TIPADMONITION


In the specific case of Latex/Beamer output the adminitions are output inside an
environment like:

    NOTE: the note

    \begin{admonitionnote}
    the note.
    \end{admonitionnote}

## Installation

1. Install python 3 (version >3.9) and pandoc

2. Install panflute python libraries

    pip3 install panflute

3. Download and place the file in directory:

    ~/.pandoc/filters


## Usage in pandoc

    pandoc -s test.md  -t beamer --filter adoc-admonitions.py

# Author

    Prof. Georgios Pappas Jr
    University of Brasilia (UnB) - Brazil

"""

from panflute import *

# The default filter name to appear in the metadata block
FILTERNAME= "adoc-admonition"
# Admonition mapping. Key is the ADMONITION name (case is considered) and the
# value is the classname the admonition should be mapped into
ADMONITIONS = {
        "NOTE": "note",
        "TIP": "tip",
        "ERROR": "error",
        "CODE": "term",
        "WARNING": "warn",
        "QUOTE": "quote"
        }

def prepare(doc):
    pass


def action(elem, doc):
    """
    Tries to find in the paragraphs words starting with the defined LINKS
    defined. Then strips the admonition keyword and encloses the remaing text
    in a DIV with the class given by the value of the keyword in the LINKS dict

    :param elem:
    :param doc:
    :return:
    """

    # Skip non Div elements
    if not isinstance(elem, Para):
        return

    #
    # getting the document metadata. To guarantee that this procedure is executed only once
    # check if variable META is defined in the global scope. Then gets the variable
    # from markdown metadata and merge with the default LINKS dict
    #
    if 'META' not in globals():
        META = doc.get_metadata(FILTERNAME, {})
        # Merging admonition names and types with metadata
        admonitions = {**ADMONITIONS, **META}
        globals()['META'] = META

    # Getting the text
    text = stringify(elem)
    # Skip empty lines
    if not len(text):
        return
    # Getting the first word
    first_word = text.split(": ", 1)[0]
    if first_word not in admonitions:
        return
    else:
        classname = admonitions[first_word]


    newtext = text.removeprefix(first_word+": ")
    # Creating a RawBlock with a Latex environment
    if doc.format in ["latex", "beamer"]:
        return [
                RawBlock(u'\\begin{' + classname + u'}', "tex"),
                Para(Str(newtext)),
                RawBlock(u'\\end{' + classname + u'}', "tex"),
        ]

    div = Div(Para(Str(newtext)), classes=[classname])

    return div



def finalize(doc):
    pass


def main_test(doc=None):
    file_name = "test_admonition.json"
    file = open(file_name, "r")

    run_filter(action,
               prepare=prepare,
               finalize=finalize,
               input_stream=file,
               doc=doc)
    # convert_text(doc, output_format="latex", standalone=True)


def main(doc=None):
    return run_filter(action,
                      prepare=prepare,
                      finalize=finalize,
                      doc=doc)


if __name__ == '__main__':
    main_test()
    # main()
