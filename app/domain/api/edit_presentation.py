"""
    PyGenPres - A Python Presentation Generator

    Copyright (C) 2025  Cyril BOSSELUT

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import os
from pathlib import Path
from string import Template
from typing import Union

from app.domain.model.presentation import Presentation


async def edit_presentation(path: str, id: Union[str, None] = None) -> str:
    """
    Generates the HTML content for editing a presentation.

    Args:
        path: The directory path where presentation data is stored.
        id: The ID of the presentation to edit. If None, a new presentation is created.

    Returns:
        The HTML content for the edit presentation page.

    Raises:
        AssertionError: If the presentation is not found.

    """
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
