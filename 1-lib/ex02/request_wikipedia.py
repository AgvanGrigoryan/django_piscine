import sys
import json
import dewiki
import requests

def save_to_file(title: str, text: str) -> None:
    filename = title.replace(" ", "_") + ".wiki"
    try:
        with open(filename, mode="w", encoding="utf-8") as fout:
            fout.write(text)
    except OSError as exc:
        sys.exit(f"File error with '{filename}': {exc}")

def make_api_request(title: str):
    WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
    headers = {
        "User-Agent": "request_wikipedia.py (https://github.com/agvangrigoryan)"
    }

    params: dict[str, str | int]= {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": 1,
        "titles": title,
        "redirects": 1
    }
    try:
        response = requests.get(WIKI_API_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        page = next(iter(data["query"]["pages"].values()))
        if "extract" not in page or not page["extract"]:
            raise ValueError("No content found for the query.")
        
        return page["title"], page["extract"]
    except Exception as exc:
        sys.exit(f"Error: {exc}")

def process(query: str) -> None:
    title, content = make_api_request(query)
    clean_content = dewiki.from_string(content)
    save_to_file(query, clean_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Expected one argument")
    query = sys.argv[1]
    process(query)