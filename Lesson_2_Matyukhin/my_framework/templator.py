from jinja2 import Template

from os.path import join



def render(template_name, folder='templates', **kwargs):
    path = join(folder, template_name)
    with open(path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
