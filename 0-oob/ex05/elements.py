from elem import Elem, Text

class Html(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="html", content=content, tag_type="double", attr=attr)

class Head(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="head", content=content, tag_type="double", attr=attr)

class Body(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="body", content=content, tag_type="double", attr=attr)

class Title(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="title", content=content, tag_type="double", attr=attr)

class Meta(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="meta", content=content, tag_type="single", attr=attr)

class Img(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="img", content=content, tag_type="single", attr=attr)

class Table(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="table", content=content, tag_type="double", attr=attr)

class Th(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="th", content=content, tag_type="double", attr=attr)

class Tr(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="tr", content=content, tag_type="double", attr=attr)

class Td(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="td", content=content, tag_type="double", attr=attr)

class Ul(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="ul", content=content, tag_type="double", attr=attr)

class Ol(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="ol", content=content, tag_type="double", attr=attr)

class Li(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="li", content=content, tag_type="double", attr=attr)
        
class H1(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="h1", content=content, tag_type="double", attr=attr)

class H2(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="h2", content=content, tag_type="double", attr=attr)

class P(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="p", content=content, tag_type="double", attr=attr)

class Div(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="div", content=content, tag_type="double", attr=attr)

class Span(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="span", content=content, tag_type="double", attr=attr)

class Hr(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="hr", content=content, tag_type="single", attr=attr)

class Br(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__(tag="br", content=content, tag_type="single", attr=attr)

if __name__ == "__main__":
    e = Html([
        Head(Title(Text('Hello ground!'))),
        Body([
            H1(Text('Oh no, not again!')),
            Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})
        ])
    ])
    print(e)