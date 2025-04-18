import os

from app.domain.model.templates.templates import Templates
from app.domain.model.transitions.transitions import Transitions
from app.domain.model.presentation import Presentation
from app.domain.model.file import Image, Video


async def save_presentation_changes(changes: dict, presentations_dir: str) -> Presentation:
    """
    Saves changes to a presentation.

    This function takes a dictionary of changes and a directory path,
    loads the existing presentation (or creates a new one), applies the changes,
    and returns the updated presentation object.

    Args:
        changes: A dictionary containing the changes to apply.
        presentations_dir: The directory where presentations are stored.

    Returns:
        The updated Presentation object.
    """
    pres_id = changes["id"]
    file_path = os.path.join(presentations_dir, f"{pres_id}.json")
    presentation = (
        Presentation.from_json(open(file_path, "r").read())
        if os.path.exists(file_path)
        else Presentation()
    )
    for change in changes["changes"]:
        if change["field"] == "title":
            presentation.title = change["value"]
        elif change["field"] == "footer":
            presentation.footer = change["value"]
        elif change["field"] == "font_family":
            presentation.font_family = change["value"]
        elif change["field"] == "slide":
            slide_id = change["id"]
            slide = next(s for s in presentation.slides if s.id == slide_id)
            for field in change["value"]:
                field_name = field["field"]
                field_value = field["value"]
                if field_name == "position":
                    presentation = presentation.move_slide(slide_id, field_value)
                elif field_name == "title":
                    slide.title = field_value
                elif field_name == "description":
                    slide.description = field_value
                elif field_name == "font_family":
                    presentation.font_family = field_value["id"]
                    slide.font_family = field_value["id"]
                elif field_name == "header_alignment":
                    slide.header_alignment = field_value["id"]
                elif field_name == "background_color":
                    slide.background_color = f"#{field_value}" if not field_value.startswith("#") else field_value
                elif field_name == "background_image":
                    slide.background_image = field_value
                elif field_name == "transition":
                    slide.transition = Transitions(field_value["id"]).new_instance()
                elif field_name == "duration":
                    slide.transition.duration = field_value
                elif field_name == "template":
                    slide.template = Templates(field_value["id"]).new_instance()
                elif field_name in (f.name for f in slide.template.fields):
                    field_index = [f.name for f in slide.template.fields].index(field_name)
                    if field_name.endswith("image") and isinstance(field_value, dict):
                        slide.template.fields[field_index].content = Image(**field_value)
                    elif field_name.endswith("video") and isinstance(field_value, dict):
                        slide.template.fields[field_index].content = Video(**field_value)
                    else:
                        slide.template.fields[field_index].content = field_value
                else:
                    raise ValueError(f'Unknown field: {field_name}')
            presentation.update_slide(slide)
        else:
            raise ValueError(f'Unknown field: {change["field"]}')
    return presentation


async def store_presentation(presentation: Presentation, presentations_dir: str) -> bool:
    """
    Stores a presentation as a JSON file in the specified path.

    Args:
        presentation: The Presentation object to store.
        presentations_dir: The directory path where the presentation should be stored.

    Returns:
        True if the presentation was successfully stored, False otherwise.

    """
    try:
        with open(os.path.join(presentations_dir, f'{presentation.id}.json'), 'w+') as f:
            f.write(presentation.to_json())
        return True
    except Exception as e:
        print(e)
        return False
