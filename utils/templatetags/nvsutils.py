from django import template
from django.conf import settings
from django.templatetags.static import static
import os

register = template.Library()

@register.filter
def replace_v(value, arg):
    if len(arg.split('|')) != 2:
        return value
    what, to = arg.split('|')
    value = value.replace(what, to)
    print(value)
    return value

@register.filter(name='add_ob_js')
def add_ob_js(value):
    file_path = value
    file_name = os.path.basename(file_path)
    fn_without_ex = os.path.splitext(file_name)[0]
    directory_path = os.path.dirname(file_path)
    js_file = f'{fn_without_ex}.obfuscated.js' if settings.USE_OBFUSCATED_JS else f'{fn_without_ex}.js'
    return static(f'{directory_path}/{js_file}')