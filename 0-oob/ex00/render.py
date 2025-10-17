import os
import sys
import re

def is_valid_file(filename: str, expected_ext: str) -> bool:
    """check file's extension"""
    if not os.path.exists(filename):
        print("File not found", file=sys.stderr)
        return False
    if os.path.splitext(filename)[1] != expected_ext:
        print("Wrong file extension", file=sys.stderr)
        return False
    return True

def get_output_filename(filename: str) -> str:
    """generate the output filename based on input filename"""
    base, _ = os.path.splitext(filename)
    return base + ".html"

def get_context(settings_filename: str) -> dict:
    """Executes the settings file and returns its variables as a dictionary."""

    context: dict = {}
    try:
        with open(settings_filename, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError as e:
        raise SystemExit(f"Settings file not found, expected {settings_filename}") from e
    except PermissionError as e:
        raise SystemExit("Permission denied while reading settings") from e
    except Exception as e:
        raise SystemExit("Unexpected error in settings file") from e

    pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$'

    for line in content.splitlines():
        match = re.match(pattern, line)
        if match:
            name, value_str = match.groups()
        try:
            value = eval(value_str, {"__builtins__": None}, {})
        except:
            value = value_str.strip()
        context[name] = value
    return context

def render_line(line: str, context: dict) -> str:
    """substitutes values from the context into the corresponding fields of the string"""
    try:
        return line.format(**context)
    except KeyError as e:
        raise SystemExit(f"Missing required variable in settings '{e}'") from e

def process_template_file(input_filename: str, output_filename: str, context: dict) -> None:
    """read line by line from infile, substitutes values and write it to the outfile"""
    try:
        with open(input_filename, 'r', encoding='utf-8') as fin, \
                open(output_filename, 'w', encoding='utf-8') as fout:
            for line in fin:
                rendered_line = render_line(line, context)
                fout.write(rendered_line)
    except FileNotFoundError as e:
        raise SystemExit("File not found") from e
    except PermissionError as e:
        raise SystemExit("Permission denied") from e
    except Exception as e:
        raise SystemExit("Unexpected error in template file") from e

if __name__ == "__main__":
    if (
        len(sys.argv) != 2 
        or not is_valid_file(sys.argv[1], ".template")
    ):
        raise SystemExit("Invalid arguments, expected <filename>.template")
    SETTINGS_FILE = "settings.py"
    context: dict[str, str] = get_context(SETTINGS_FILE)
    process_template_file(sys.argv[1], get_output_filename(sys.argv[1]), context)
    
