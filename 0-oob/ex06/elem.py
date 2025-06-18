#!/usr/bin/python3

class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        html_escape = (
            ('&', '&amp;'),
            ('<', '&lt;'),
            ('>', '&gt;'),
            ('"', '&quot;'),
            ("'", '&apos;'),
        )
        s = super().__str__()
        for char, replacement in html_escape:
            s = s.replace(char, replacement)
        return s.replace('\n', '\n<br />\n')


class Elem:
    """
    Elem will permit us to represent our HTML elements.
    """
    class ValidationError(Exception):
        def __init__(self):
            super().__init__("Validation error!")

    def __init__(self, tag='div', attr=None, content=None, tag_type='double'):
        """
        __init__() method.

        Obviously.
        """
        self.tag = tag
        self.tag_type = tag_type
        self.attr = attr if attr else dict()
        self.content = []
        self.add_content(content=content)

    def __str__(self):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded
        elements...)."""
        result = ""
        if self.tag_type == "double":
            result = f"<{self.tag}{self.__make_attr()}>"
            result += self.__make_content()
            result += f"</{self.tag}>"
        elif self.tag_type == "single":
            result = f"<{self.tag}{self.__make_attr()} />"
        return result

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        result = ''
        for key, value in sorted(self.attr.items()):
            result += ' ' + str(key) + '="' + str(value) + '"'
        return result

    def __make_content(self):
        """
        Here is a method to render the content, including embedded elements.
        """

        if len(self.content) == 0:
            return ''
        result = '\n'
        
        for elem in self.content:
            for line in str(elem).split('\n'):
                if line.strip() != '':
                    result += '  ' + line + '\n'
        return result

    def add_content(self, content):
        if content is None:
            return
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))


if __name__ == '__main__':
    e = Elem('html', content=[
        Elem('head', content=Elem('title', content=Text('Hello ground!'))),
        Elem('body', content=[
            Elem('h1', content=Text('Oh no, not again!')),
            Elem('img', attr={'src': 'http://i.imgur.com/pfp3T.jpg'}, tag_type='single')
        ])
    ])
    print(e)
