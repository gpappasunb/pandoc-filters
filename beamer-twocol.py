#!/usr/bin/env python3

"""
Pandoc filter that creates a Div with simpler syntax for columns
in Latex/Beamer. It works for only two columns and the delimiter for
the columns is a HorizontalRule element (--- or * * *).

The upper text goes to the left column and the lower to the right

The syntax is:

::: twocol

Content left

* * *
Content right

Content right

::::::::::

Alternatively, it is possible to pass some options controlling the columns, namely
'width' and 'align'. For these,specify the values inside quotes and separated by commas. If
no commas, then the value will be applied to both columns.

::: {.twocol align="top,center" width="20%,80%" .onlytextwidth}

Content left

1. asd
2. sdf sdffds

* * *
Content right

date
:  sdfkj skdfjfskd

:::


Georgios Pappas Jr
University of Brasilia (UnB) - Brazil

"""

from panflute import *


DIVNAME="twocol"

def prepare(doc):
    pass


def action(elem, doc):
    """
    Tries to find a div named FILTERNAME (should be the first class)
    Inside this div, tries to find an horizontalrule (* * *). If not found return
    At the position of the rule create, split the div contents in two
    and encapsulate both in a new Div of class "column"
    Finally change the parent div class to "columns" and return
    :param elem:
    :param doc:
    :return:
    """
    # Works only for beamer
    if doc.format != 'beamer':
        pass

    # Skip non Div elements
    if not isinstance(elem, Div):
        return

    if elem.classes[0] != DIVNAME:
        return

    # Finding an horizontal line and recording its position
    ruler_pos = [i for i,d in enumerate(elem.content) if isinstance(d,HorizontalRule)]
    if not len(ruler_pos):
        debug(f"No ruler in this div!!! {ruler_pos}")
        return
    else:
        ruler_pos = ruler_pos[0]

    num_elements = len(elem.content)

    #
    # Processing attributes: if given attributes align and width
    # should have a special syntax to be applied to each of the columns
    # The values should be inside quotes and comma-separated
    # align="top,bottom" width="20%,80%"
    # align="bottom" --> in this case BOTH columns get the same value
    cols_attributes = process_attributes(elem.attributes)

    # Changing the class from FILTERNAME to "columns", which is later processed by beamer converter
    elem.classes[0] = "columns"
    # Take all elements up to the horizontal line and creating a new div
    beforeContent = [elem.content[i] for i in range(ruler_pos)]
    beforeDiv = Div(*beforeContent,classes=["column"], attributes={**elem.attributes,**cols_attributes['left']})

    # Enclose in div After the ruler
    if ruler_pos<num_elements:
        # elem.content.insert(ruler_pos,afterDiv)
        afterContent = [elem.content[i] for i in range(ruler_pos+1,num_elements)]
        afterDiv = Div(*afterContent,classes=["column"], attributes={**elem.attributes,**cols_attributes['right']})
    else:
        afterDiv = []

    # Joinining both contents
    contents = [
            beforeDiv,afterDiv
    ]
    finalDiv = Div(*contents,classes=["columns"])
    return finalDiv


def finalize(doc):
    pass

def process_attributes(attributes):
    """
    Processes the attribute string (only align and width) to create left and right values
    :param attributes:
    :return:
    """
    shared_attributes = {'left': {}, 'right': {}}
    for i in ["align", "width"]:
        if i not in attributes:
            continue
        split_attributes(attributes[i],i, shared_attributes)
        del attributes[i]

    return shared_attributes

def split_attributes(attr,attr_name,shared_attr):
    """
    Called by process_attributes. Performs actual attribute string parsing and splitting
    :param attr:
    :param attr_name:
    :param shared_attr:
    :return:
    """
    attrs = attr.split(",", maxsplit=2)
    shared_attr['left'].update({f"{attr_name}": attrs[0]})
    split_pos=0
    if len(attrs)>1:
        split_pos=1
    shared_attr['right'].update({f"{attr_name}": attrs[split_pos]})
    # return split_attribute

def main_test(doc=None):
    file_name = "test_col.json"
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
