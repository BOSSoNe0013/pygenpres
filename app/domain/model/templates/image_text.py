from dataclasses import dataclass
from typing import Optional

from app.domain.model.file import Image
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class ImageText(SlideTemplate):
    title: str = "Image Text"
    subtitle: str = "Subtitle"
    text: str = "This is some text"
    text_color: str = "#fff"
    image: Optional[Image] = None

    def __post_init__(self):
        self.name = "Image Text"
        self.description = "A block of text with an image on the left"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"it_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"it_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"it_text", content=self.text),
            TemplateField(TemplateFieldType.COLOR, name=f"it_text_color", content=self.text_color),
            TemplateField(TemplateFieldType.IMAGE, name=f"it_image", content=self.image)
        ]

    @property
    def content(self) -> str:
        return f"""<h1 class="image-text-{self.id}">$it_title</h1>
<p class="image-text-{self.id}">$it_subtitle</p>
<div class="image-text-{self.id}">
    <img src="$it_image" />
    <div>$it_text</div>
</div>
"""

    @property
    def style(self) -> str:
        return f"""
h1.image-text-{self.id} {{
    font-size: 5em;
    font-size: 3rem;
    margin-bottom: 0.2rem;
    color: $it_text_color;
    text-shadow: 0 0 10px #000;
}}
p.image-text-{self.id} {{
    font-size: 2rem;
    color: $it_text_color;
    max-width: 800px;
    margin: 0 auto;
    margin-bottom: 3rem;
}}
div.image-text-{self.id} {{
    display: grid;
    grid-template-columns: auto 60%;
    gap: 20px;
    font-size: 1.8rem;
    font-weight: 300;
}}
div.image-text-{self.id} > div {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    color: $it_text_color;
    background-color: $background_color;
    border-radius: 4px;
    opacity: 0.8;
    padding: 1rem 2rem;
}}
div.image-text-{self.id} > img {{
    border-radius: 4px;
    width: 100%;
}}
"""

    @property
    def script(self) -> str:
        return ""
