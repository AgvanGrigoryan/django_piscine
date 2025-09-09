from django import template
import hashlib

register = template.Library()

ROW_CLASSES = ["table-primary", "table-secondary", "table-success",
                "table-danger", "table-warning", "table-info",
                "table-light"]

@register.filter
def deterministic_class(value):
    a = 6  # коэффициент, выбираем взаимно простой с количеством цветов
    c = 3
    m = len(ROW_CLASSES)
    index = (a * int(value) + c) % m
    return ROW_CLASSES[index]