from dataclasses import dataclass
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class SimpleTitle(SlideTemplate):
    title: str = "Simple Title"
    subtitle: str = "Subtitle"
    text_color: str = "#fff"

    def __post_init__(self):
        self.name = "Simple title"
        self.description = "A simple title slide"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"st_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"st_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.COLOR, name=f"st_text_color", content=self.text_color),
        ]

    @property
    def content(self) -> str:
        return f"""<h1 class="simple-title-{self.id}">$st_title</h1>
<p class="simple-title-{self.id}">$st_subtitle</p>
"""

    @property
    def style(self) -> str:
        return f"""
h1.simple-title-{self.id} {{
    font-size: 5em;
    font-size: 3rem;
    margin-bottom: 1rem;
    color: $st_text_color;
    text-shadow: 0 0 10px #000;
}}
p.simple-title-{self.id} {{
    font-size: 2rem;
    color: $st_text_color;
    max-width: 800px;
    margin: 0 auto;
}}
"""

    @property
    def script(self) -> str:
        return ""
