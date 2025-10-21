import sys
import requests
from bs4 import BeautifulSoup, Tag

def print_road_info(dead_end: bool, road: list[str]):
    if dead_end:
        print("It's a dead end !")
    else:
        for title in road:
            print(title)
        print(f"{len(road)} from {road[0]} to philosophy !")

def process_title(title: str, passed_titles_set: set[str], passed_titles_list: list[str]):
    if title in passed_titles_set:
        sys.exit("It leads to an infinite loop !")
    passed_titles_set.add(title)
    passed_titles_list.append(title)

def is_inside_parentheses(a) -> bool:
    parent = a.find_parent("p")
    if not parent:
        return False
    parent_text = parent.get_text()
    idx = parent_text.find(a.get_text())
    if idx == -1:
        return False
    text_up_to_link = parent_text[:idx]
    return text_up_to_link.count("(") > text_up_to_link.count(")")

def get_first_link_to_article(soup: BeautifulSoup):
    WIKIPEDIA_URL = "https://en.wikipedia.org"

    content = soup.find(id="mw-content-text")
    if content is None:
        return None
    paragraphs = content.find_all("p")
    if not paragraphs:
        return None
    for p in paragraphs:
        links = p.find_all("a")
        for a in links:
            parents = (parent.name for parent in a.parents)
            if "table" in parents :
                continue
            elif is_inside_parentheses(a) or a.find_parent(["i", "em"]):
                continue
            href = a.get("href")
            if (
                href and
                href.startswith("/wiki/") and
                ":" not in href and
                "#" not in href
            ):
                return WIKIPEDIA_URL + href
    return None

def get_article_title(soup: BeautifulSoup, page_url: str):
    first_heading = soup.find(id="firstHeading")
    if first_heading is None:
        sys.exit(f"First Heading not found in [{page_url}]")
    return first_heading.text


def process_redirection(soup: BeautifulSoup, passed_titles_set: set[str], passed_titles_list: list[str]) -> None:
    redirected_from = soup.find(class_="mw-redirectedfrom")
    if redirected_from:
        redirected_link = redirected_from.find("a")
        if redirected_link and redirected_link.text:
            redirected_title = redirected_link.text
            process_title(redirected_title, passed_titles_set, passed_titles_list)


def process(url: str) -> None:
    passed_titles_set: set[str] = set()
    passed_titles_list: list[str] = []
    dead_end = False
    headers = {
        "User-Agent": "roads_to_philosophers.py (https://github.com/agvangrigoryan)"
    }

    while True:
        response = requests.get(url, headers=headers)
        if response.ok is False:
            dead_end = True
            break
        soup = BeautifulSoup(response.text, "html.parser")

        process_redirection(soup, passed_titles_set, passed_titles_list)
        title = get_article_title(soup, response.url)

        process_title(title, passed_titles_set, passed_titles_list)
        if title == "Philosophy":
            break
        url = get_first_link_to_article(soup)
        if url is None:
            dead_end = True
            break
    print_road_info(dead_end, passed_titles_list)


if __name__ == "__main__":
    if (argc := len(sys.argv) - 1) != 1:
        raise sys.exit(f"takes 1  positional arguments <any wikipedia title>, given {argc}")
    wiki_title = sys.argv[1]
    process("https://en.wikipedia.org/wiki/" + wiki_title)
