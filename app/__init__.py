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
import os.path
from pathlib import Path
from string import Template
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse

from .domain.model import TemplateRecords, TransitionRecords, PresentationRecords, ErrorResponse
from .domain.api.edit_presentation import edit_presentation
from .domain.api.presentation import remove_slide_from_presentation, get_presentation, add_slide_to_presentation
from .domain.api.presentations import get_presentations
from .domain.api.root import get_root
from .domain.api.store_presentation import store_presentation, save_presentation_changes
from .domain.api.templates import get_templates
from .domain.api.transitions import get_transitions
from .domain.model.presentation import PresentationResponse
from .domain.model.slides import SlideResponse

"""
This module defines the FastAPI application for the PyGenPres project.
"""
app = FastAPI()
app.mount("/static", StaticFiles(directory="res/static"), name="static")
home_dir = Path.home()
config_dir = os.path.join(home_dir, '.config', 'pygenpres')
if not os.path.exists(config_dir):
    os.makedirs(config_dir)
config_file = os.path.join(config_dir, 'config.json')
if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        f.write('{}')
presentations_dir = os.path.join(config_dir, 'presentations')
if not os.path.exists(presentations_dir):
    os.makedirs(presentations_dir)



@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """
    Returns the root HTML page.
    """
    return await get_root()

@app.get("/p", response_model=PresentationRecords)
async def presentations():
    """
    Returns a list of available presentations.
    """
    return await get_presentations(presentations_dir)

@app.get("/t", response_model=TemplateRecords)
async def templates():
    """
    Returns a list of available templates.
    """
    return await get_templates()

@app.get("/tr", response_model=TransitionRecords)
async def transitions():
    """
    Returns a list of available transitions.
    """
    return await get_transitions()

@app.get("/p/{id}.html", response_class=HTMLResponse, include_in_schema=False)
async def run(id: str):
    """
    Returns the HTML representation of a presentation.

    Args:
        id: The ID of the presentation.
    """
    presentation = await get_presentation(id, presentations_dir)
    if not presentation:
        raise HTTPException(status_code=400, detail='Presentation not found')

    return presentation.get_html()

@app.get("/p/{id}.json", response_model=PresentationResponse)
async def get_json_presentation(id: str):
    """
    Returns the JSON representation of a presentation.

    Args:
        id: The ID of the presentation.
    """
    presentation = await get_presentation(id, presentations_dir)
    if not presentation:
        raise HTTPException(status_code=400, detail='Presentation not found')

    return presentation.to_response()

@app.get("/new", response_class=HTMLResponse, include_in_schema=False)
async def new():
    return await edit()

@app.get("/s/{id}/{sid}.html", response_class=HTMLResponse, include_in_schema=False)
async def get_html_slide(id: str, sid: str):
    """
    Returns the HTML representation of a specific slide.

    Args:
        id: The ID of the presentation.
        sid: The ID of the slide.
    """
    presentation = await get_presentation(id, presentations_dir)
    if not presentation:
        raise HTTPException(status_code=400, detail='Presentation not found')

    slide = [s for s in presentation.slides if s.id == sid][0]
    content = f"""<style>{Template(slide.get_style()).safe_substitute({'font_family': presentation.font_family})}
footer {{
    position: absolute;
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
}}
</style>
{slide.get_html(hidden=False)}
<footer>{Template(presentation.get_footer()).safe_substitute({'slide_position': slide.position + 1})}</footer>"""
    return content

@app.get("/s/{id}/{sid}.json", response_model=SlideResponse)
async def get_json_slide(id: str, sid: str):
    """
    Returns the JSON representation of a specific slide.

    Args:
        id: The ID of the presentation.
        sid: The ID of the slide.
    """
    presentation = await get_presentation(id, presentations_dir)
    if not presentation:
        raise HTTPException(status_code=400, detail='Presentation not found')

    slides = [s for s in presentation.slides if s.id == sid]
    if not slides:
        raise HTTPException(status_code=400, detail='Slide not found')

    slide = slides[0]
    return slide.to_response()

@app.get(
    "/s/{id}/add",
    response_model=PresentationResponse,
    responses={400: {"model": ErrorResponse}},
    status_code=201
)
async def add_slide(id: str, position: Union[int, None] = None):
    """
    Adds a new slide to a presentation.

    Args:
        id: The ID of the presentation.
        position: The position where to insert the new slide.
    """
    presentation = await get_presentation(id, presentations_dir)
    if not presentation:
        raise HTTPException(status_code=400, detail='Presentation not found')
    result = await add_slide_to_presentation(presentation, position, presentations_dir)

    if result:
        return presentation.to_response()
    else:
        return JSONResponse(status_code=400, content={'message': 'Could not add slide'})

@app.delete(
    "/s/{id}/{sid}.json",
    response_model=PresentationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def remove_slide(id: str, sid: str):
    """
    Removes a slide from a presentation.

    Args:
        id: The ID of the presentation.
        sid: The ID of the slide to remove.
    """
    presentation = await get_presentation(id, presentations_dir)
    if not presentation:
        raise HTTPException(status_code=400, detail='Presentation not found')

    result = await remove_slide_from_presentation(presentation, sid, presentations_dir)

    if result:
        return presentation.to_response()
    else:
        return JSONResponse(status_code=400, content={'message': 'Could not delete slide'})

@app.get("/edit/{id}", response_class=HTMLResponse, include_in_schema=False)
async def edit(id: Union[str, None] = None):
    """
    Returns the HTML page for editing a presentation.

    Args:
        id: The ID of the presentation to edit.
    """
    return await edit_presentation(id=id, path=presentations_dir)

@app.post("/save", response_model=PresentationResponse, responses={400: {"model": ErrorResponse}})
async def save_presentation(changes: dict):
    """
    Saves changes made to a presentation.
    """
    try:
        presentation = await save_presentation_changes(changes, presentations_dir)
        result = await store_presentation(presentation, presentations_dir=presentations_dir)
        if result:
            return presentation.to_response()
        else:
            return JSONResponse(status_code=400, content={'message': 'Could not save presentation'})
    except Exception as e:
        print(e)
        return {'error': f'{e}'}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Returns the favicon.
    """
    return FileResponse("res/static/favicon.ico")
