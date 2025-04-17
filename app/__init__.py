import os.path
from pathlib import Path
from string import Template
from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.domain.api.edit_presentation import edit_presentation
from app.domain.api.presentations import get_presentations
from app.domain.api.root import get_root
from app.domain.api.store_presentation import store_presentation
from app.domain.api.templates import get_templates
from app.domain.api.transitions import get_transitions
from app.domain.model.file import Image, Video
from app.domain.model.presentation import Presentation
from app.domain.model.slides import Slide
from app.domain.model.templates import TemplateFieldType
from app.domain.model.templates.image_text import ImageText
from app.domain.model.templates.simple_title import SimpleTitle
from app.domain.model.templates.templates import Templates
from app.domain.model.templates.text_image import TextImage
from app.domain.model.templates.three_text_columns import ThreeTextColumns
from app.domain.model.transitions import Transition
from app.domain.model.transitions.parallax import Parallax
from app.domain.model.transitions.transitions import Transitions

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
    return await get_root()

@app.get("/p")
async def presentations():
    return await get_presentations(presentations_dir)

@app.get("/t")
async def templates():
    return await get_templates()

@app.get("/tr")
async def transitions():
    return await get_transitions()

@app.get("/p/{id}.html", response_class=HTMLResponse)
async def run(id: str):
    with open(os.path.join(presentations_dir, f'{id}.json'), 'r') as file:
        presentation = Presentation.from_json(file.read())
    return presentation.get_html()

@app.get("/p/{id}.json")
async def dump(id: str):
    with open(os.path.join(presentations_dir, f'{id}.json'), 'r') as file:
        presentation = Presentation.from_json(file.read())
    return presentation.to_dict()

@app.get("/new", response_class=HTMLResponse)
async def new():
    return await edit()

@app.get("/s/{id}/{sid}.html", response_class=HTMLResponse)
async def slide(id: str, sid: str):
    with open(os.path.join(presentations_dir, f'{id}.json'), 'r') as file:
        presentation = Presentation.from_json(file.read())
    slide = [s for s in presentation.slides if s.id == sid][0]
    content = f"""<style>{slide.get_style()}
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
    with open(os.path.join(presentations_dir, f'{id}.json'), 'r') as file:
        presentation = Presentation.from_json(file.read())
    slide = [s for s in presentation.slides if s.id == sid][0]
    return slide.to_dict()

@app.get("/s/{id}/add")
async def add_slide(id: str, position: Union[int, None] = None):
    with open(os.path.join(presentations_dir, f'{id}.json'), 'r') as file:
        presentation = Presentation.from_json(file.read())
    if position is None:
        position = len(presentation.slides)
    slide = Slide(template=Templates.default(), transition=Transitions.default(), position=position)
    presentation.add_slide(slide, position=position)
    result = await store_presentation(presentation, path=presentations_dir)
    if result:
        return presentation.to_dict()
    else:
        return {'error': 'Could not add slide'}

@app.delete("/s/{id}/{sid}.json")
async def remove_slide(id: str, sid: str):
    with open(os.path.join(presentations_dir, f'{id}.json'), 'r') as file:
        presentation = Presentation.from_json(file.read())
    presentation.remove_slide(sid)
    result = await store_presentation(presentation, path=presentations_dir)
    if result:
        return presentation.to_dict()
    else:
        return {'error': 'Could not delete slide'}

@app.get("/edit/{id}", response_class=HTMLResponse)
async def edit(id: Union[str, None] = None):
    return await edit_presentation(id=id, path=presentations_dir)

@app.post("/save")
async def save(changes: dict):
    try:
        pres_id = changes['id']
        file_path = os.path.join(presentations_dir, f'{pres_id}.json')
        if os.path.exists(file_path):
            with open(os.path.join(presentations_dir, f'{pres_id}.json'), 'r') as file:
                presentation = Presentation.from_json(file.read())
        else:
            presentation = Presentation()
        for change in changes['changes']:
            match change['field']:
                case 'title':
                    presentation.title = change['value']
                case 'footer':
                    presentation.footer = change['value']
                case 'slide':
                    slide_id = change['id']
                    slide = [s for s in presentation.slides if s.id == slide_id][0]
                    for field in change['value']:
                        match field['field']:
                            case 'position':
                                presentation = presentation.move_slide(slide_id, field['value'])
                            case 'title':
                                slide.title = field['value']
                            case 'description':
                                slide.description = field['value']
                            case 'background_color':
                                value: str = field['value']
                                if not value.startswith('#'):
                                    value = f'#{value}'
                                slide.background_color = value
                            case 'background_image':
                                slide.background_image = field['value']
                            case 'transition':
                                transition = Transitions(field['value']["id"])
                                slide.transition = transition.new_instance()
                            case 'duration':
                                slide.transition.duration = field['value']
                            case 'template':
                                template = Templates(field['value']["id"])
                                slide.template = template.new_instance()
                            case _:
                                if field['field'] in [f.name for f in slide.template.fields]:
                                    field_index = [f.name for f in slide.template.fields].index(field['field'])
                                    if field['field'].endswith('image'):
                                        if isinstance(field['value'], dict):
                                            slide.template.fields[field_index].content = Image(**field['value'])
                                        else:
                                            slide.template.fields[field_index].content = None
                                    elif field['field'].endswith('video'):
                                        if isinstance(field['value'], dict):
                                            slide.template.fields[field_index].content = Video(**field['value'])
                                        else:
                                            slide.template.fields[field_index].content = None
                                    else:
                                        slide.template.fields[field_index].content = field['value']
                                else:
                                    raise ValueError(f'Unknown field: {field["field"]}')
                    presentation.update_slide(slide)
                case _:
                    raise ValueError(f'Unknown field: {change["field"]}')
        result = await store_presentation(presentation, path=presentations_dir)
        if result:
            return presentation.to_dict()
        else:
            return {'error': 'Could not save presentation'}
    except Exception as e:
        print(e)
        return {'error': f'{e}'}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("res/static/favicon.ico")
