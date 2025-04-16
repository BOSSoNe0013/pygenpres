import os
from dataclasses import dataclass
from string import Template
from typing import Optional

from app.domain.model.file import Video
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class Video(SlideTemplate):

    title: str = "Video"
    subtitle: str = "Subtitle"
    text_color: str = "#fff"
    video: Optional[Video] = None
    controls: bool = False
    loop: bool = True
    autoplay: bool = True

    def __post_init__(self):
        self.name = "Video"
        self.description = "A video slide"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"v_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"v_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.COLOR, name=f"v_text_color", content=self.text_color),
            TemplateField(TemplateFieldType.VIDEO, name=f"v_video", content=self.video),
            TemplateField(TemplateFieldType.BOOL, name=f"v_controls", content=self.controls),
            TemplateField(TemplateFieldType.BOOL, name=f"v_loop", content=self.loop),
            TemplateField(TemplateFieldType.BOOL, name=f"v_autoplay", content=self.autoplay),
        ]

    @property
    def style(self) -> str:
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'video.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        js_values = {
            'id': self.id,
            'autoplay': 'true' if self.autoplay else 'false'
        }
        with open(os.path.join(self.templates_path, 'video.css'), 'r') as js_file:
            js_template = js_file.read()
        return Template(js_template).safe_substitute(js_values)

    @property
    def content(self) -> str:
        html_values = {
            'id': self.id,
            'controls': 'controls' if self.controls else '',
            'loop': 'loop' if self.loop else '',
        }
        with open(os.path.join(self.templates_path, 'video.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)
