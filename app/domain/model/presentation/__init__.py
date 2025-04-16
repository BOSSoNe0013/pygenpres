from dataclasses import dataclass, field
from string import Template
from typing import Optional, Self
from uuid import uuid4
import json

from app.domain.model import ModelObject
from app.domain.model.slides import Slide


class PresentationId(str):
    pass


@dataclass
class Presentation(ModelObject):
    id: Optional[PresentationId] = field(
        default_factory=lambda: PresentationId(str(uuid4())))
    title: str = ""
    footer: str = ""
    style: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)

    def __post_init__(self):
        self._slides: list[Slide] = list()

    @property
    def slides(self) -> list[Slide]:
        return self._slides

    def add_slide(self, slide: Slide, position: Optional[int] = None):
        if position is not None:
            self._slides.insert(position, slide)
            for i, slide in enumerate(self._slides):
                slide.position = i
            return
        slide.position = len(self._slides)
        self._slides.append(slide)

    def move_slide(self, id: str, position: int) -> Self:
        slide = [s for s in self._slides if s.id == id][0]
        self._slides.remove(slide)
        self._slides.insert(position, slide)
        for i, slide in enumerate(self._slides):
            slide.position = i
        return self

    def remove_slide(self, id: str):
        slide = [s for s in self._slides if s.id == id][0]
        self._slides.remove(slide)
        for i, slide in enumerate(self._slides):
            slide.position = i
        return self

    def update_slide(self, slide: Slide):
        if len(self._slides) > slide.position:
            self._slides[slide.position] = slide

    def to_dict(self, encode_json=False):
        d = super().to_dict(encode_json=encode_json)
        d['slides'] = [slide.to_dict(encode_json=encode_json) for slide in self._slides]
        return d

    @classmethod
    def from_dict(cls, d: dict, infer_missing=False):
        p = super().from_dict(d, infer_missing=infer_missing)
        p._slides = [Slide.from_dict(slide, infer_missing=infer_missing) for slide in d['slides']]
        return p

    @classmethod
    def from_json(cls, s, *, parse_float=None, parse_int=None, parse_constant=None, infer_missing=False, **kw):
        o = json.loads(s)
        return cls.from_dict(o, infer_missing=infer_missing)

    def _load_scripts(self) -> str:
        return f"""
let page = 0;
document.addEventListener('DOMContentLoaded', function() {{
    const total_pages = {len(self._slides)};
    document.querySelector('#current-page').innerHTML = page + 1;
    document.querySelector('#total-pages').innerHTML = total_pages;
    const firstSlide = document.querySelector(`#slide_0`);
    firstSlide.scrollIntoView({{
        behavior: 'smooth'
    }});

    document.addEventListener('keyup', function(e) {{
        if (e.key == " " ||
            e.code == "Space" ||      
            e.keyCode == 32      
        ) {{
            page += 1;
            if (page >= total_pages) {{
                page = 0;
            }}
        }}
        const targetSlide = document.querySelector(`#slide_${{page}}`);
        targetSlide.scrollIntoView({{
            behavior: 'smooth'
        }});
        document.querySelector('#current-page').innerHTML = page + 1;
    }});

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
        anchor.addEventListener('click', function (e) {{
            e.preventDefault();
            if (e.target.href.endsWith("#next")) {{
                page += 1;
                if (page >= total_pages) {{
                    page = total_pages - 1;
                }}
            }}
            if (e.target.href.endsWith("#prev")) {{
                page -= 1;
                if (page < 0) {{
                    page = 0;
                }}
            }}
            if (e.target.href.endsWith("#first")) {{
                page = 0;
            }}
            if (e.target.href.endsWith("#last")) {{
                page = total_pages - 1;
            }}
            const targetSlide = document.querySelector(`#slide_${{page}}`);
            targetSlide.scrollIntoView({{
                behavior: 'smooth'
            }});                
            document.querySelector('#current-page').innerHTML = page + 1;
        }});
    }});
}});
{''.join(self.scripts)}
{''.join([slide.get_script() for slide in self.slides])}
       """

    def _load_style(self) -> str:
        base_style = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: 'Roboto', sans-serif;
    line-height: 1.6;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
    font-smoothing: antialiased;
}
footer {
    position: fixed;
    z-index: 10;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 4px 16px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    color: #fff;
    font-size: 0.7rem
}
.container {
    width: 100%;
    min-height: 100vh;
    overflow-x: hidden;
    padding: 0;
}
slide {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    padding: 2rem 4rem;
}
ul, ol {
    list-style-position: inside;
    margin: 0.2rem 0;
}
slide p {
    margin: 0.2rem 0;
}
slide table {
  width: 100%;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ffffff;
}
slide thead {
    font-weight: 900;
}
slide th {
    padding: 6px 12px;
}
slide tbody tr {
    background: #f6f6f6;
}
slide tbody tr:nth-of-type(odd) {
    background: #e9e9e9;
}
slide td {
    color: #3b3b3b !important;
    padding: 6px 12px;
}
.navigation {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 20px;
    z-index: 999;
    padding: 4px 8px;
    border-radius: 4px;
    background-color: #00000055;
    opacity: 0;
    transition: opacity linear 1s
}
.navigation:hover {
    opacity: 1;
    transition: opacity linear 1s
}
.navigation a {
    color: #fff;
    text-decoration: none;
    font-size: 1.2rem;
}
.parallax-layer {
    position: absolute;
    width: 100%;
    height: 100%;
    view-timeline-name: --slide;
    view-timeline-axis: block;
}
.bg-1, .bg-2 {
    background-size: cover;
    background-position: center;
}
.bg-1 {
    transform: translateZ(-5px);
    z-index: 1;
    background-color: #ff000000;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    opacity: 0.2;
}
.bg-2 {
    transform: translateZ(-10px);
    z-index: 2;
    background-color: #0000ff00;
    animation-delay: 0.4s;
}
.content {
    position: relative;
    z-index: 3;
    padding: 4px 8px;
}
"""
        return f"""
{base_style}
{''.join(self.style)}
{''.join([slide.get_style() for slide in self._slides])}
        """

    @property
    def __html_template__(self) -> str:
        return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>$title</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    $style
    </style>
</head>
<body>
    <div class="container">
    $slides
    </div>
    <nav class="navigation">
        <a href="#first">⏪ First</a>
        <a href="#prev">◀️ Previous</a>
        <span>-</span>
        <a href="#next">Next ▶️</a>
        <a href="#last">Last ⏩</a>
    </nav>
    <footer>$footer</footer>
    <script>
    $script
    </script>
</body>
</html>
"""

    def get_footer(self) -> str:
        return f'<span>{self.footer}</span><span><span id=\"current-page\">$slide_position</span>/<span id=\"total-pages\">{len(self._slides)}</span></span>'

    def get_html(self) -> str:
        html = Template(self.__html_template__).safe_substitute({
            'style': self._load_style(),
            'script': self._load_scripts(),
            'slides': ''.join([slide.get_html() for slide in self._slides]),
            'title': self.title,
            'footer': self.get_footer()
        })
        return "".join([s for s in html.strip().splitlines(True) if s.strip()])
