from app.domain.model.presentation import Presentation
from app.utils.files import list_files


async def get_presentations(path: str) -> dict:
    records = []
    files = list_files(path, ['.json'])
    for file in files:
        with open(file, 'r') as f:
            presentation = Presentation.from_json(f.read())
            records.append({'id': presentation.id, 'text': presentation.title})
    return {'records':records}
