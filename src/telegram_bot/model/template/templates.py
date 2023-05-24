import re
import jinja2
from configurate import config


class RenderTemplate:

    # def __init__(self):
    #     tags = {
    #         "{FOURSPACE}": "    "
    #     }

    def render_template(self, template_name: str, data: dict | None = None) -> str:
        if data is None:
            data = {}
        template = self.__get_template_env().get_template(template_name)
        rendered = template.render(**data).replace("\n", " ")
        rendered = rendered.replace("<br>", "\n")
        rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
        rendered = "\n".join(line.strip() for line in rendered.split("\n"))
        rendered = rendered.replace("{FOURPACES}", "    ")
        rendered = rendered.replace("{ONE_SPACE}", " ")
        return rendered

    def __get_template_env(self):
        template_loader = jinja2.FileSystemLoader(searchpath=config.TEMPLATES_DIR)
        env = jinja2.Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )
        return env

render = RenderTemplate()
