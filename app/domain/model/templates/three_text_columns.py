from dataclasses import dataclass

from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class ThreeTextColumns(SlideTemplate):
    title: str = "Three Text Columns"
    subtitle: str = "Subtitle"
    text_1: str = "This is the first text"
    text_2: str = "This is the second text"
    text_3: str = "This is the third text"
    text_color: str = "#fff"
    image: str = ""

    def __post_init__(self):
        self.name = "Three text columns"
        self.description = "A block of three text columns"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"ttc_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"ttc_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ttc_text_1", content=self.text_1),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ttc_text_2", content=self.text_2),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ttc_text_3", content=self.text_3),
            TemplateField(TemplateFieldType.COLOR, name=f"ttc_text_color", content=self.text_color),
        ]

    @property
    def content(self) -> str:
        return f"""<h1 class="three-text-cols-{self.id}">$ttc_title</h1>
<p class="three-text-cols-{self.id}">$ttc_subtitle</p>
<div class="three-text-cols-{self.id}">
    <div>$ttc_text_1</div>
    <div>$ttc_text_2</div>
    <div>$ttc_text_3</div>
</div>
"""

    @property
    def style(self) -> str:
        return f"""
h1.three-text-cols-{self.id} {{
    font-size: 5em;
    font-size: 3rem;
    margin-bottom: 0.2rem;
    color: $ttc_text_color;
    text-shadow: 0 0 10px #000;
}}
p.three-text-cols-{self.id} {{
    font-size: 2rem;
    color: $ttc_text_color;
    max-width: 800px;
    margin: 0 auto;
    margin-bottom: 3rem;
}}
div.three-text-cols-{self.id} {{
    display: grid;
    grid-template-columns: 30% 30% 30%;
    gap: 20px;
    font-size: 1.8rem;
    font-weight: 300;
}}
div.three-text-cols-{self.id} > div {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    color: $ttc_text_color;
    background-color: $background_color;
    border-radius: 4px;
    opacity: 0.8;
    padding: 1rem 2rem;
}}
"""

    @property
    def script(self) -> str:
        return ""
