---
super-links:
    foo: "https://hello.co"
    other:
        url: "HTTP://foo.com/"
        encode: true
        before: "SOMETEXT:"
        after: " <--AFTER"

...

[FOO]{#l .foo}

[Some text]{#l type=other}

[1233211]{#l type=pubmed}  

[Arabidopsis_thaliana]{#l .wiki title="Arabidopsis thaliana" before="WIKI:"}

[10.1007/978-1-4613-8850-0_3]{#l .doi}
