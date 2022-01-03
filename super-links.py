#!/usr/bin/env python3

"""
Pandoc filter that creates custom links from bracketed spans
with a specific ID (#l), written as:

1. with a 'type' attribute

        [text]{#l type=wiki}

2. with a 'class' name starting with a dot

        [text]{#l .wiki}

Inside the brackets we have the link text. Its URL is configured
in the dictionary LINKS or in the markdown metadata (see later).

The keys of the LINKS dictionary contain the type or class name that will
provide the URL mapping for the link. In the simpler case there will
be a string containing the URL. The final URL will be the URL in the
dictionary appended by the text inside the brackets.

    [text]{#l type=github}

    URL => https://github.com/text

The default LINKS dict contains (showing only the github entry):

    LINKS = {"github" : "https://github.com/"}

## Changing the displayed text

If the attribute "title"  is set, then it will replace the link text.
The original text in brackets will still be used to create the link URL

    [Arabidopsis_thaliana]{#l .wiki title="Thale cress"}
    -> <p><a href="https://en.wikipedia.org/wiki/Arabidopsis_thaliana" class="wiki" title="Arabidopsis thaliana">Thale cress</a></p>

Also, the "before' and 'after' attributes can be used to preprend or append
text to the link text

    [Arabidopsis_thaliana]{#l .wiki title="Thale cress" before="wikipedia:"}
    -> <p><a href="https://en.wikipedia.org/wiki/Arabidopsis_thaliana" class="wiki" title="Arabidopsis thaliana">wikipedia:Thale cress</a></p>

## Specifying new link types

Aside from the default cases, additional links can be configured in
the pandoc metadata header:

    ---
    super-links:
        foo: "https://hello.co"
        other:
            url: "HTTP://foo.com/"
            encode: true
            before: "SOMETEXT:"
            after: " <--AFTER"

    ...

Any output format should be supported, and in the case above we will have the
following results, using the HTML output format:

    [FOO]{#l .foo}
    -> <p><a href="https://hello.co/FOO" class="foo">FOO</a></p>

    [Some text]{#l type=other}
    -> <p><a href="HTTP://foo.com//Some+text" type="other">SOMETEXT:Some text&lt;–AFTER</a></p>

    [1233211]{#l type=pubmed}
    -> <p><a href="https://pubmed.ncbi.nlm.nih.gov//1233211" type="pubmed">pubmed:1233211</a></p>

    [Arabidopsis_thaliana]{#l .wiki title="Arabidopsis thaliana" before="WIKI:"}
    -> <p><a href="https://en.wikipedia.org/wiki//Arabidopsis_thaliana" class="wiki" title="Arabidopsis thaliana" data-before="WIKI:">WIKI:Arabidopsis thaliana</a></p>

    [10.1007/978-1-4613-8850-0_3]{#l .doi}
    -> <p><a href="https://doi.org//10.1007/978-1-4613-8850-0_3" class="doi">DOI:10.1007/978-1-4613-8850-0_3</a></p>


## Advantages

This filter, in some cases, requires less typing to represent a link.
For instance:

Plain markdown
:
            ![thale cress](https://en.wikipedia.org/wiki/Arabidopsis_thaliana)

With filter
:
           [Arabidopsis_thaliana]{#l .wiki}


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
    version 0.1
    Last modification: Sun Jan  2 21:11:25 -03 2022

"""
import urllib.parse
from panflute import *

# The default filter name to appear in the metadata block
FILTERNAME = "super-links"
IDNAME = "l"
# Admonition mapping. Key is the ADMONITION name (case is considered) and the
# value is the classname the admonition should be mapped into
LINKS = {
        "wiki"   : {
                "url"   : "https://en.wikipedia.org/wiki",
                "encode": True,
                "before": "",
                "after" : ""
        },
        "pubmed" : {
                "url"   : "https://pubmed.ncbi.nlm.nih.gov/",
                "before": "pubmed:"
        },
        "doi"    : {
                "url"   : "https://doi.org/",
                "before": "DOI:"
        },
        "github" : "https://github.com/",
        "youtube": "https://www.youtube.com/"
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
    if not isinstance(elem, Span):
        return

    #
    # getting the document metadata. To guarantee that this procedure is executed only once
    # check if variable META is defined in the global scope. Then gets the variable
    # from markdown metadata and merge with the default LINKS dict
    #
    if 'META' not in globals():
        META = doc.get_metadata(FILTERNAME, {})
        # Merging admonition names and types with metadata
        globals()['LINKS'] = {**LINKS, **META}
        globals()['META'] = META

    # Checking if the exact ID and if at least one class were provided
    if elem.identifier != IDNAME:
        return

    # The type should be a key in the LINKS dict. Initially, we hove none
    type = ""
    # Now the link url selection is performed
    # First check for the presence of an attribute named "type"
    # {#l type=wiki}
    try:
        type = get_option(elem.attributes, "type")
    except ValueError:
        # If type not present, then use the first class for the URL selection
        # {#l .wiki}
        if len(elem.classes):
            type = elem.classes[0]

    # Getting the class, which should correspond to one of the
    # elements provided in the links dictionary
    if type not in LINKS:
        return

    # Creating the URL and text shown, based on the given
    # attributes.
    (text, url) = get_link_text(type, elem)

    # Getting the span text
    # text = stringify(elem)
    # Getting the url from LINKS
    # url  = LINKS[type]

    # Removing the identifier
    elem.identifier = ""
    # Getting the link string to add to the end of the URL
    # Initially we take the text content
    # title=""
    # try:
    #     title = get_option(elem.attributes, "title")
    # except:
    #     title=""

    newlink = Link(Str(text), url=url,
                   classes=elem.classes,
                   attributes=elem.attributes,
                   # title=title
                   )
    # Getting the text
    return newlink


def finalize(doc):
    pass


def get_link_text(type, elem):
    """

    :param type:
    :param elem:
    :return:
    """
    # Getting the span text
    link_text = stringify(elem)
    # Getting the url from LINKS
    url_data = LINKS[type]
    title = elem.attributes.get('title')
    url = ""

    if isinstance(url_data, str):
        slash = "" if url_data.endswith("/") else "/"
        url = url_data + slash + link_text
        if title:
            link_text = title
    elif isinstance(url_data, dict):
        slash = "" if url_data['url'].endswith("/") else "/"
        # Encoding the URL in case encode attribute is set
        if url_data.get("encode"):
            encoded_text = urllib.parse.quote_plus(link_text)
            url = url_data['url'] + slash + encoded_text
        else:
            url = url_data['url'] + slash + link_text

        if title:
            link_text = title

        prepend = url_data.get('before', "")
        prepend = elem.attributes.get('before', prepend)
        link_text = prepend + link_text
        append = url_data.get('after', "")
        append = elem.attributes.get('after', append)
        link_text = link_text + append

    return (link_text, url)


def main_test(doc=None):
    file_name = "test_links.json"
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
