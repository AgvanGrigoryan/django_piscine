from django.shortcuts import render

COLOR_GENERATORS = {
    "noir": lambda v: f"rgb({v}, {v}, {v})",
    "rouge": lambda v: f"rgb({v}, 0, 0)",
    "bleu": lambda v: f"rgb(0, 0, {v})",
    "vert": lambda v:  f"rgb(0, {v}, 0)",
}

def generate_shade(color_name: str, shade_num: int, step: int):
    value = 255 - int((255 / step) * shade_num)
    return COLOR_GENERATORS[color_name](value)

def build_shades_table(colors: list[str], lines:int=50):
    shades_table: list[list[str]] = []

    for i in range(lines):
        row: list[str] = []
        for color in colors:
            shade = generate_shade(color, i, lines)
            row.append(shade)

        shades_table.append(row)
    return shades_table

def index(request):
    colors: list[str] = [color for color in COLOR_GENERATORS.keys()]

    context = {
        "title": "Shades Catalog",
        "colors": colors,
        "shades_table" : build_shades_table(colors),
    }
    return render(request, "ex03_index.html", context)