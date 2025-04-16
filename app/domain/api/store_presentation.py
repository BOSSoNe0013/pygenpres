import os

from app.domain.model.presentation import Presentation


async def store_presentation(presentation: Presentation, path: str) -> bool:
    try:
        with open(os.path.join(path, f'{presentation.id}.json'), 'w+') as f:
            f.write(presentation.to_json())
        return True
    except Exception as e:
        print(e)
        return False
