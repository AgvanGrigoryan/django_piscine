from elements import *

class Page:
    ALLOWED_TAGS = {"html", "head", "body", "title", "meta", "img",
                    "table", "th", "tr", "td", "ul", "ol", "li",
                    "h1", "h2", "p", "div", "span", "hr", "br"}
    def __init__(self, html_elem: Elem):
        self.elem = html_elem
        self.validators = {
            "html": self._check_html,
            "head": self._check_head,
            "body": self._check_body_and_div,
            "title": self._is_contain_only_one_Text,
            "meta": self._check_meta,
            "img": self._check_img,
            "table": self._check_table,
            "th": self._is_contain_only_one_Text,
            "tr": self._check_tr,
            "td": self._is_contain_only_one_Text,
            "ul": self._check_list,
            "ol": self._check_list,
            "li": self._is_contain_only_one_Text,
            "h1": self._is_contain_only_one_Text,
            "h2": self._is_contain_only_one_Text,
            "p": self._check_p,
            "div": self._check_body_and_div,
            "span": self._check_span,
            "hr": self._check_hr,
            "br": self._check_br
        }

    def __str__(self):
        doc_type = "<!DOCTYPE html>\n" if isinstance(self.elem, Html) else ""
        return doc_type + str(self.elem)

    def write_to_file(self, filename: str):
        try:
            with open(filename, 'w') as f:
                doc_type = "<!DOCTYPE html>\n" if isinstance(self.elem, Html) else ""
                f.write(doc_type + str(self.elem))
        except OSError as exc:
            print(f"File error with '{filename}': {exc}")

    def is_valid(self) -> bool:
        return isinstance(self.elem, Elem) and self._validate_tag(self.elem)
    
    def _validate_tag(self, tag: Elem):
        if isinstance(tag, Text):
            return True
        
        if tag.tag not in self.ALLOWED_TAGS:
            return False
        
        validator = self.validators.get(tag.tag)
        if validator and not validator(tag):
            return False

        for inner_tag in tag.content:
            if not self._validate_tag(inner_tag):
                return False

        return True
    
    def _only_contain(self, tag: Elem, allowed_list: tuple, required_cnt: int | None = None):
        count: int = 0
        for inner_tag in tag.content:
            if not isinstance(inner_tag, allowed_list):
                return False
            elif required_cnt is not None:
                count += 1
        if required_cnt is not None and count != required_cnt:
            return False
        return True

    def _is_contain_only_one_Text(self, node: Elem) -> bool:
        return self._only_contain(node, (Text,), 1)

    def _only_li_and_at_least_one(self, node: Elem) -> bool:
        if not node.content:
            return False
        return all(isinstance(child, Li) for child in node.content)

    def _check_body_and_div(self, node: Elem) -> bool:
        return self._only_contain(node, (H1, H2, Div, Table, Ul, Ol, Span, Text))


    def _check_html(self, node: Elem) -> bool:
        if len(node.content) != 2:
            return False
        return isinstance(node.content[0], Head) and isinstance(node.content[1], Body)

    def _check_head(self, node: Elem) -> bool:
        return self._only_contain(node, (Title,), 1)

    def _check_meta(self, node: Elem) -> bool:
        return True

    def _check_img(self, node: Elem) -> bool:
        return True

    def _check_table(self, node: Elem) -> bool:
        return self._only_contain(node, (Tr,))

    def _check_tr(self, node: Elem) -> bool:
        if not self._only_contain(node, (Td, Th)):
            return False
        
        count_td = sum(isinstance(child, Td) for child in node.content)
        count_th = sum(isinstance(child, Th) for child in node.content)

        if count_td > 0 and count_th > 0:
            return False
        if count_td == 0 and count_th == 0:
            return False
        return True

    def _check_list(self, node: Elem) -> bool:
        return self._only_li_and_at_least_one(node)

    def _check_p(self, node: Elem) -> bool:
        return self._only_contain(node, (Text,))

    def _check_span(self, node: Elem) -> bool:
        return self._only_contain(node, (Text, P))

    def _check_br(self, node: Elem) -> bool:
        return True

    def _check_hr(self, node: Elem) -> bool:
        return True

if __name__ == "__main__":
    # 1. Valid example
    valid_tree = Html([
        Head(Title(Text("My Title"))),
        Body([
            H1(Text("Header")),
            Div([
                H2(Text("Subheader")),
                Ul([Li(Text("Item 1")), Li(Text("Item 2"))]),
                Table([
                    Tr([Th(Text("Name")), Th(Text("Age"))]),
                    Tr([Td(Text("Alice")), Td(Text("30"))])
                ])
            ])
        ])
    ])
    page1 = Page(valid_tree)
    print("Valid page1:", page1.is_valid())       # True
    print(page1)                                  # __str__ method
    page1.write_to_file("valid_page.html")        # write_to_file method

    # 2. Invalid example (Tr includes Td and Th)
    invalid_tree = Html([
        Head(Title(Text("Oops"))),
        Body([
            Table([
                Tr([Th(Text("Bad")), Td(Text("Mix"))])
            ])
        ])
    ])
    page2 = Page(invalid_tree)
    print("Invalid page2 (mixed Td and Th):", page2.is_valid())  # False
