import os
from pathlib import Path

from app.domain.model import Record, ThemeRecords
from app.utils.decorators import classproperty
from app.utils.files import list_files


class Themes:

    @classproperty
    def themes_path(cls) -> str:
        """
        Returns the path to the directory containing the themes.

        Returns:
            str: The path to the themes' directory.
        """
        return os.path.join(Path.cwd(), 'res', 'themes')

    @classmethod
    async def list_themes(cls) -> ThemeRecords:
        records = []
        files = list_files(cls.themes_path, ['.css'])
        for file in files:
            file_name = file.split('/')[-1].split('.')[0]
            records.append(Record(id=file_name, text=file_name))
        return ThemeRecords(status='success', total=len(files),records=records)

    @classmethod
    async def get_theme(cls, name: str) -> str:
        if not os.path.exists(os.path.join(cls.themes_path, f'{name}.css')):
            raise FileNotFoundError(f"The theme '{name}' does not exist.")
        with open(os.path.join(cls.themes_path, f'{name}.css'), 'r') as theme_file:
            theme = theme_file.read()
        return theme

