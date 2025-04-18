import os

from app.domain.model.presentation import Presentation


async def store_presentation(presentation: Presentation, path: str) -> bool:
    """
    Stores a presentation as a JSON file in the specified path.

    Args:
        presentation: The Presentation object to store.
        path: The directory path where the presentation should be stored.

    Returns:
        True if the presentation was successfully stored, False otherwise.

    """
    try:
        with open(os.path.join(path, f'{presentation.id}.json'), 'w+') as f:
            f.write(presentation.to_json())
        return True
    except Exception as e:
        print(e)
        return False
