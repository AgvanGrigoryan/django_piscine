import sys

def parse_single_line(line: str) -> dict[str, str]:
	properties = dict()

	fullname, other = line.split('=', 1)
	for prop in other.split(','):
		name, value = prop.split(":")
		properties[name.strip()] = value.strip()

	properties["fullname"] = fullname.strip()
	return properties

def parse_file_data(filename: str) -> list[dict[str, str]]:
	result: list[dict] = list()

	with open(filename, mode="r") as file:
		for line in file:
			single_element = parse_single_line(line)
			result.append(single_element)
		
	return sorted(result, key=lambda x: int(x["number"]))

def create_single_elem_box(elem: dict) -> str:
	return f"""
		<td class='elem' >
			<h4 class='elem_fullname' >{elem['fullname']}</h4>
			<ul>
				<li>No {elem['number']}</li>
				<li>{elem['small']}</li>
				<li>{elem['molar']}</li>
				<li>{elem['electron'].replace(' ', ', ')}</li>
			</ul>
		</td>
		"""

def create_empty_column() -> str:
	return "<td class='elem empty_elem' ></td>\n"

def create_row(elem_list: list[dict]) -> str:
	row_html = "<tr>\n"
	for pos in range(18):
		if elem_list and pos == int(elem_list[0]['position']):
			row_html += create_single_elem_box(elem_list[0])
			elem_list.pop(0)
		else:
			row_html += create_empty_column()
	row_html += "</tr>\n"
	return row_html

def create_rows(elems: list[dict]) -> str:
	elem_list = elems.copy()
	rows = ""
	while elem_list:
		rows += create_row(elem_list)
	return rows

def html_table(elems: list[dict]) -> str:
	content = f"""
<table>
	{create_rows(elems)}
</table>
"""
	return content

# The Content of Style Tag
def html_style() -> str:
	return """
	<style>
	@import url('https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,100..1000&display=swap');
	* {
		font-family: "Roboto Flex", sans-serif;
		font-weight: 400;
		font-style: normal;
		color: #3d3d3d !important;
		font-variation-settings:
		"slnt" 0,
		"wdth" 100,
		"GRAD" 0,
		"XOPQ" 96,
		"XTRA" 468,
		"YOPQ" 79,
		"YTAS" 750,
		"YTDE" -203,
		"YTFI" 738,
		"YTLC" 514,
		"YTUC" 712;
	}
	body {
		font-family: 'Segoe UI', sans-serif;
		background: #f3f6fb;
		margin: 20px;
		text-align: center;
	}

	table {
		margin: auto;
		border-collapse: collapse;
	}

	.elem {
		width: 80px;
		height: 80px;
		border-radius: 6px;
		padding: 4px;
		font-size: 11px;
		border: 2px solid white;
		box-shadow: inset 0 0 3px rgba(0,0,0,0.1);
		text-align: left;
		vertical-align: top;
		transition: transform 0.2s;
	}
	.elem_fullname {
		font-size: 14px;
		
	}

	.elem:hover {
		transform: scale(1.05);
		z-index: 1;
		position: relative;
	}

	.empty_elem {
		background: transparent !important;
		border: none;
		box-shadow: none;
	}

	h4 {
		margin: 0 0 4px 0;
		font-size: 12px;
		font-weight: bold;
		color: #1c3b5a;
	}

	ul {
		list-style: none;
		margin: 0;
		padding: 0;
		color: #333;
	}

	li {
		line-height: 1.1;
	}

	tr:not(:first-of-type) > td.elem:nth-child(1),
	tr:not(:first-of-type) > td.elem:nth-child(2) {
		background: linear-gradient(to bottom, #ff810d, #ffc39a);
	}

	tr:not(:first-of-type) > td.elem:nth-child(n+3):nth-child(-n+12) {
		background: linear-gradient(to bottom, #93b7c3, #d3e4eb);
	}
	tr:not(:first-of-type) > td.elem:nth-child(n+13):nth-child(-n+18) {
		background: linear-gradient(to bottom, #977ca8, #d9cfe1);
	}
	tr:first-of-type > td.elem {
		background: linear-gradient(to bottom, #ff810d, #ffc39a);
	}
	</style>
	"""

# The Content of Head Tag
def html_head() -> str:
	return f"""
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{__file__}</title>
	{html_style()}
</head>
"""

# The Content of Body Tag
def html_body(elems: list[dict]) -> str:
	return f"""
<body>
	<h1>Periodic Table Of Elements</h1>
	{html_table(elems)}
</body>
"""

# The Content of hole html
def build_html(elems: list[dict]) -> str:
	DOCTYPE = "<!DOCTYPE html>"
	LANG = "en"
	return f"""
{DOCTYPE}
<html lang={LANG}>
{html_head()}
{html_body(elems)}
</html>
"""

def create_html_file(filename: str, content: str) -> None:
	with open(filename, "w", encoding="UTF-8") as html:
		html.write(content)

def process(filename: str) -> None:
	elems: list[dict] = parse_file_data(filename)
	html_content: str = build_html(elems)
	create_html_file("periodic_table.html", html_content)

if __name__ == "__main__":
    FILENAME: str = "periodic_table.txt"
    process(FILENAME)