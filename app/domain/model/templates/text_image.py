from dataclasses import dataclass
from typing import Optional

from app.domain.model.file import Image
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class TextImage(SlideTemplate):
    title: str = "Text Image"
    subtitle: str = "Subtitle"
    text: str = "This is some text"
    text_color: str = "#fff"
    image: Optional[Image] = None

    def __post_init__(self):
        self.name = "Text Image"
        self.description = "A block of text with an image on the right"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"ti_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"ti_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ti_text", content=self.text),
            TemplateField(TemplateFieldType.COLOR, name=f"ti_text_color", content=self.text_color),
            TemplateField(TemplateFieldType.IMAGE, name=f"ti_image", content=self.image)
        ]

    @property
    def content(self) -> str:
        return f"""<h1 class="text-image-{self.id}">$ti_title</h1>
<p class="text-image-{self.id}">$ti_subtitle</p>
<div class="text-image-{self.id}">
    <div>$ti_text</div>
    <img src="$ti_image" />
</div>"""

    @property
    def style(self) -> str:
        return f"""
h1.text-image-{self.id} {{
    font-size: 5em;
    font-size: 3rem;
    margin-bottom: 0.2rem;
    color: $ti_text_color;
    text-shadow: 0 0 10px #000;
}}
p.text-image-{self.id} {{
    font-size: 2rem;
    color: $ti_text_color;
    max-width: 800px;
    margin: 0 auto;
    margin-bottom: 3rem;
}}
div.text-image-{self.id} * {{
    color: $ti_text_color;
}}
div.text-image-{self.id} {{
    display: grid;
    grid-template-columns: 60% auto;
    gap: 20px;
    font-size: 1.8rem;
    font-weight: 300;
}}
div.text-image-{self.id} > div {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    color: $ti_text_color;
    background-color: $background_color;
    border-radius: 4px;
    opacity: 0.8;
    padding: 1rem 2rem;
}}
div.text-image-{self.id} > img {{
    border-radius: 4px;
    width: 100%;
}}
"""

    @property
    def script(self) -> str:
        return ""
