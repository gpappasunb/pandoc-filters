#!/usr/bin/env python3

"""
Pandoc filter for adding LaTeX environment on specific div
"""

from panflute import *

META = {}

md = """---
pandoc-latex-environment:
  bashterm:        [bash]
  ubuntu:          [ubuntu]
  admonitionnote:  [note]
  admonitiontip :  [tip]
  admonitionerror: [error]
  admonitionwarn:  [warn]
  admonitionterm:  [term]
  admonitionquote: [quote]
  message:         [message]
  messagenote:     [msgnote]
  messagetip :     [msgtip]
  messageerror:    [msgerror]
  messagewarn:     [msgwarn]
  messageterm:     [msgterm]
  messagequote:    [msgquote]
 
...


::: ubuntu
ubuntu div
::::::

"""


def prepare(doc):
    pass


def action(elem, doc):
    """

    :param elem:
    :param doc:
    :return:
    """
    # Works only for Latex
    if doc.format not in ['beamer', 'latex']:
        pass

    # Skip non Div elements
    if not isinstance(elem, Div):
        return

    # getting the document metadata. First checking if META is defined
    try:
        META
    except NameError:
        META = doc.get_metadata('div-env', None)
    finally:
        if not META:
            return

    attributes = elem.attributes

    #
    # Checks if one of the div classes is in the metadata
    # Otherwise the Div is unchanged
    #
    if not (len(elem.classes) and elem.classes[0] in META):
        return
    div = elem.classes[0]
    env = META[div]

    # Getting the label, which is the div id ( ::: {#div .env} )
    label = ''
    if elem.identifier != '':
        label = '\\label{' + elem.identifier + '}'

    if 'title' in attributes:
        title = f"[{attributes['title']}]"
    else:
        title = ''

    # Temporarily filling some properties in a temporary doc attribute (called div)
    doc.div = (env, title, label)
    # Finding the first paragraph and adding the opening environment statement
    # This is required to avoid an extra line inserted after the opening
    #
    #   Adding like this, causes this side effect
    #       before = Plain(RawInline(format='tex', text='\\begin{' + env + '}' + title + label))
    #       elem.content.insert(0,before)
    elem.walk(add_before_first_paragraph, doc)

    # Adding a last Plain element containing the closing statement as a RawLatex string
    after = Plain(RawInline(format='tex', text='\\end{' + env + '}'))

    elem.content.append(after)


def finalize(doc):
    pass


def latex(txt=""):
    """
    Creates an Inline Latex string
    :param txt: Text to be written
    :return: RawInline element
    """
    return RawInline(format='tex', text=txt)


def add_before_first_paragraph(elem, doc):
    """
    Gets the first paragraph of the Div and adds
    a latex inline before the first paragraph
    This avoids an extra newline after the environment opening,
    which causes a side effect when displaying source code
    :param elem:
    :param doc:
    :return:
    """

    # Double-checking the presence of added data in "div" field
    if not hasattr(doc, "div"):
        return
    if type(elem) == Para:
        # Getting the required data
        env, title, label = doc.div
        before = latex('\\begin{' + env + '}' + title + label)
        # before = RawInline(format='tex', text='\\begin{' + env + '}' + title + label)
        elem.content.insert(0, before)

        # Removing the temporary data
        del doc.div
        return elem
    else:
        pass


def main_test(doc=None):
    file_name = "test.json"
    file = open(file_name, "r")

    run_filter(action,
               prepare=prepare,
               finalize=finalize,
               input_stream=file,
               doc=doc)
    convert_text(doc, output_format="latex", standalone=True)


def main(doc=None):
    return run_filter(action,
                      prepare=prepare,
                      finalize=finalize,
                      doc=doc)


if __name__ == '__main__':
    # main_test()
    main()
