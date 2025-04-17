import os
from pathlib import Path
from string import Template
from typing import Union

from app.domain.model.presentation import Presentation


async def edit_presentation(path: str, id: Union[str, None] = None) -> str:
    presentation = None
    if id is None:
        presentation = Presentation()
        with open(os.path.join(path, f'{presentation.id}.json'), 'w+') as f:
            f.write(presentation.to_json())
    else:
        with open(os.path.join(path, f'{id}.json'), 'r') as f:
            presentation = Presentation.from_json(f.read())
    if presentation is None:
        raise AssertionError('Presentation not found')
    slides = [f"{{id: '{slide.id}', text: '{slide.title}', order: {slide.position}, icon: 'fa fa-rectangle-list'}}" for slide in presentation.slides]
    first_slide_id = presentation.slides.pop(0).id if presentation.slides else ''
    templates_path = os.path.join(Path.cwd(), 'res')

    with open(os.path.join(templates_path, 'edit_presentation.css'), 'r') as css_file:
        css = css_file.read()

    js_values = {
        'presentation_id': presentation.id,
        'presentation_title': presentation.title,
        'presentation_footer': presentation.footer,
        'slide_items': ',\n    '.join(slides),
        'first_slide_id': first_slide_id,
    }
    with open(os.path.join(templates_path, 'edit_presentation.js'), 'r') as js_file:
        js_template = js_file.read()
    javascript = Template(js_template).safe_substitute(js_values)

    html_values = {
        'css': css,
        'javascript': javascript
    }
    with open(os.path.join(templates_path, 'edit_presentation.html'), 'r') as html_file:
        html_template = html_file.read()

    return Template(html_template).safe_substitute(html_values)
