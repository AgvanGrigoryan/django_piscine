from django.shortcuts import render

def generate_shade(color_name: str, shade_num: int):
    value = 255 - int((255 / 50) * shade_num)

    if color_name == "noir":
        return f"rgb({value}, {value}, {value})"
    elif color_name == "rouge":
        return f"rgb({value}, 0, 0)"
    elif color_name == "bleu":
        return f"rgb(0, 0, {value})"
    elif color_name == "vert":
        return f"rgb(0, {value}, 0)"
    return None


def index(request):
    colors: list[str] = ["noir", "rouge", "bleu", "vert"]
    shades_table: list[list[str]] = list()
    
    for i in range(50):
        row: list[str] = list()
        for color in colors:
            shade = generate_shade(color, i)
            row.append(shade)

        shades_table.append(row)

    context: dict = dict()
    context.update({"title": "Shades Catalog"})
    context.update({"colors": colors})
    context.update({"shades_table" : shades_table})
    return render(request, "ex03_index.html", context)