import os.path
from pathlib import Path
from string import Template
from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from .domain.api.edit_presentation import edit_presentation
from .domain.api.presentation import remove_slide_from_presentation, get_presentation, add_slide_to_presentation
from .domain.api.presentations import get_presentations
from .domain.api.root import get_root
from .domain.api.store_presentation import store_presentation, save_presentation_changes
from .domain.api.templates import get_templates
from .domain.api.transitions import get_transitions

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



@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Returns the root HTML page.
    """
    return await get_root()

@app.get("/p")
async def presentations():
    """
    Returns a list of available presentations.
    """
    return await get_presentations(presentations_dir)

@app.get("/t")
async def templates():
    """
    Returns a list of available templates.
    """
    return await get_templates()

@app.get("/tr")
async def transitions():
    """
    Returns a list of available transitions.
    """
    return await get_transitions()

@app.get("/p/{id}.html", response_class=HTMLResponse)
async def run(id: str):
    """
    Returns the HTML representation of a presentation.

    Args:
        id: The ID of the presentation.
    """
    presentation = await get_presentation(id, presentations_dir)

    return presentation.get_html()

@app.get("/p/{id}.json")
async def dump(id: str):
    """
    Returns the JSON representation of a presentation.

    Args:
        id: The ID of the presentation.
    """
    presentation = await get_presentation(id, presentations_dir)

    return presentation.to_dict()

@app.get("/new", response_class=HTMLResponse)
async def new():
    return await edit()

@app.get("/s/{id}/{sid}.html", response_class=HTMLResponse)
async def slide(id: str, sid: str):
    """
    Returns the HTML representation of a specific slide.

    Args:
        id: The ID of the presentation.
        sid: The ID of the slide.
    """
    presentation = await get_presentation(id, presentations_dir)

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

@app.get("/s/{id}/{sid}.json")
async def slide(id: str, sid: str):
    """
    Returns the JSON representation of a specific slide.

    Args:
        id: The ID of the presentation.
        sid: The ID of the slide.
    """
    presentation = await get_presentation(id, presentations_dir)

    slide = [s for s in presentation.slides if s.id == sid][0]
    return slide.to_dict()

@app.get("/s/{id}/add")
async def add_slide(id: str, position: Union[int, None] = None):
    """
    Adds a new slide to a presentation.

    Args:
        id: The ID of the presentation.
        position: The position where to insert the new slide.
    """
    presentation = await get_presentation(id, presentations_dir)

    result = await add_slide_to_presentation(presentation, position, presentations_dir)

    if result:
        return presentation.to_dict()
    else:
        return {'error': 'Could not add slide'}

@app.delete("/s/{id}/{sid}.json")
async def remove_slide(id: str, sid: str):
    """
    Removes a slide from a presentation.

    Args:
        id: The ID of the presentation.
        sid: The ID of the slide to remove.
    """
    presentation = await get_presentation(id, presentations_dir)

    result = await remove_slide_from_presentation(presentation, sid, presentations_dir)

    if result:
        return presentation.to_dict()
    else:
        return {'error': 'Could not delete slide'}

@app.get("/edit/{id}", response_class=HTMLResponse)
async def edit(id: Union[str, None] = None):
    """
    Returns the HTML page for editing a presentation.

    Args:
        id: The ID of the presentation to edit.
    """
    return await edit_presentation(id=id, path=presentations_dir)

@app.post("/save")
async def save(changes: dict):
    """
    Saves changes made to a presentation.
    """
    try:
        presentation = await save_presentation_changes(changes, presentations_dir)
        result = await store_presentation(presentation, presentations_dir=presentations_dir)
        if result:
            return presentation.to_dict()
        else:
            return {'error': 'Could not save presentation'}
    except Exception as e:
        print(e)
        return {'error': f'{e}'}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Returns the favicon.
    """
    return FileResponse("res/static/favicon.ico")
