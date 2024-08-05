from jinja2 import BaseLoader, TemplateNotFound, Environment, PackageLoader, select_autoescape, Template
from os.path import join, exists, getmtime

class TemplateLoader(BaseLoader):
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: mtime == getmtime(path)

class Prompt(object):

    def __init__(self, template:str) -> None:
        super().__init__()
        self.Template:str = template
        # template_str = "Hello, {{ name }}!"

    def Render(self, langDesc:str, description:str)->str:
        template = Template(self.Template)
        rendered_str = template.render(langDesc=langDesc,description=description)
        return rendered_str

        # env = Environment(loader=TemplateLoader(rootPath), autoescape=select_autoescape())
        # template = env.get_template("projects\\POC\\Form.html")
        # render: str = template.render(the="variables", go="here")