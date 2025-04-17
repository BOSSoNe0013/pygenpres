import os
from dataclasses import dataclass, field
from pathlib import Path
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
    font_family: str = "Roboto"
    header_alignment: str = "center"
    id: Optional[SlideId] = field(
        default_factory=lambda: SlideId(str(uuid4())))
    position: int = 0

    @property
    def templates_path(self) -> str:
        return os.path.join(Path.cwd(), 'res', 'slides')

    @property
    def __html_template__(self) -> str:
        with open(os.path.join(self.templates_path, 'base_slide.html'), 'r') as html_file:
            html_template = html_file.read()
        return html_template

    def get_html(self, hidden: bool = True) -> str:
        values = {
            field.name: field.get_html() for field in self.template.fields
        }
        values['title'] = self.title
        content = Template(self.template.content).safe_substitute(values)
        return Template(self.__html_template__).safe_substitute({
            'slide_position': self.position,
            'slide_content': content,
            'class_list': 'hidden' if self.position != 0 and hidden else ''
        })

    def get_script(self) -> str:
        return self.template.script

    def get_style(self) -> str:
        templates_values = {
            field.name: field.content for field in self.template.fields
        }
        templates_values['background_color'] = self.background_color
        templates_values['header_alignment'] = self.header_alignment
        values = {
            'background_color': self.background_color,
            'background_image': self.background_image.data_url if self.background_image else '',
            'slide_position': self.position,
            'transition': self.transition.get(self.position),
            'template': Template(self.template.style).safe_substitute(templates_values),
            'z_index': 500 - self.position,
        }
        with open(os.path.join(self.templates_path, 'base_slide.css'), 'r') as css_file:
            css_template = css_file.read()
        style = Template(css_template).safe_substitute(values)
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
