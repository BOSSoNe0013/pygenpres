from dataclasses import dataclass, field
from string import Template
from typing import Optional
from uuid import uuid4

from app.domain.model.templates.templates import Templates
from app.domain.model import ModelObject
from app.domain.model.file import Image, Video
from app.domain.model.templates import SlideTemplate
from app.domain.model.transitions import Transition


class SlideId(str):
    pass


@dataclass
class Slide(ModelObject):
    template: SlideTemplate
    transition: Transition
    title: str = "New slide"
    description: str = ""
    background_image: Optional[Image] = None
    background_color: str = "#ffffff"
    id: Optional[SlideId] = field(
        default_factory=lambda: SlideId(str(uuid4())))
    position: int = 0

    @property
    def __html_template__(self) -> str:
        return """
    <slide id="slide_$slide_position">
        <div class="parallax-layer bg-1"></div>
        <div class="parallax-layer bg-2"></div>
        <div class="content">
            $slide_content
        </div>
    </slide>
"""

    def get_html(self) -> str:
        values = {
            field.name: field.get_html() for field in self.template.fields
        }
        values['title'] = self.title
        content = Template(self.template.content).safe_substitute(values)
        return Template(self.__html_template__).safe_substitute({
            'slide_position': self.position,
            'slide_content': content
        })

    def get_script(self) -> str:
        return self.template.script

    def get_style(self) -> str:
        values = {
            field.name: field.content for field in self.template.fields
        }
        values['background_color'] = self.background_color
        style = f"""
#slide_{self.position} {{
    background-color: {self.background_color};
}}
#slide_{self.position} .bg-1 {{
    --i: {self.position};
    background-image: url('{self.background_image.data_url if self.background_image else ''}');
    {self.transition.get()}
}}
slide_{self.position} thead {{
    background-color: {self.background_color};
}}
{self.transition.get_keyframe()}
{Template(self.template.style).safe_substitute(values)}
"""
        return style

    @classmethod
    def from_dict(cls, d: dict, infer_missing=False):
        t_name = d.get('template').get('name').lower().replace(' ', '_')
        fields = d.get('template').get('fields')
        f = {}
        for field in fields:
            n = field.get('name').split('_')
            n.pop(0)
            name = '_'.join(n)
            if name.endswith('image'):
                if isinstance(field.get('content'), dict):
                    f[name] = Image(**field.get('content'))
                else:
                    f[name] = None
            elif name.endswith('video'):
                if isinstance(field.get('content'), dict):
                    f[name] = Video(**field.get('content'))
                else:
                    f[name] = None
            else:
                f[name] = field.get('content')
        t = Templates(t_name).new_instance(**f)
        p = super().from_dict(d, infer_missing=infer_missing)
        p.template = t
        return p
