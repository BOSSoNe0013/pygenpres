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

from app.domain.api.store_presentation import store_presentation
from app.domain.model.presentation import Presentation
from app.domain.model.slides import Slide
from app.domain.model.templates.templates import Templates
from app.domain.model.transitions.transitions import Transitions
from typing import Union


async def get_presentation(id: str, presentations_dir: str) -> Presentation:
    """
    Retrieves a presentation from its JSON file.
    """
    with open(os.path.join(presentations_dir, f'{id}.json'), 'r') as file:
        presentation = Presentation.from_json(file.read())
    return presentation


async def add_slide_to_presentation(presentation: Presentation, position: Union[int, None], presentations_dir: str):
    """
    Adds a new slide to a presentation.

    Args:
        presentation: The presentation to add the slide to.
        position: The position to insert the slide at. If None, the slide is added to the end.
        presentations_dir: The directory where presentations are stored.

    """
    if position is None:
        position = len(presentation.slides)
    slide = Slide(template=Templates.default(), transition=Transitions.default(), position=position)
    presentation.add_slide(slide, position=position)
    return await store_presentation(presentation, presentations_dir)


async def remove_slide_from_presentation(presentation: Presentation, sid: str, presentations_dir: str):
    """
    Removes a slide from a presentation.

    Args:
        presentation: The presentation to remove the slide from.
        sid: The ID of the slide to remove.
        presentations_dir: The directory where presentations are stored.

    Returns:
        The updated presentation.
    """
    presentation.remove_slide(sid)
    return await store_presentation(presentation, presentations_dir)
