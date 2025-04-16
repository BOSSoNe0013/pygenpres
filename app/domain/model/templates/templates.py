from enum import Enum


class Templates(str, Enum):
    SIMPLE_TITLE = 'simple_title'
    IMAGE_TEXT = 'image_text'
    TEXT_IMAGE = 'text_image'
    THREE_TEXT_COLUMNS = 'three_text_columns'
    VIDEO = 'video'

    def new_instance(self, **kwargs):
        match self:
            case Templates.SIMPLE_TITLE:
                from app.domain.model.templates.simple_title import SimpleTitle
                return SimpleTitle(**kwargs)
            case Templates.IMAGE_TEXT:
                from app.domain.model.templates.image_text import ImageText
                return ImageText(**kwargs)
            case Templates.TEXT_IMAGE:
                from app.domain.model.templates.text_image import TextImage
                return TextImage(**kwargs)
            case Templates.THREE_TEXT_COLUMNS:
                from app.domain.model.templates.three_text_columns import ThreeTextColumns
                return ThreeTextColumns(**kwargs)
            case Templates.VIDEO:
                from app.domain.model.templates.video import Video
                return Video(**kwargs)
            case _:
                raise ValueError(f'Unknown template: {self}')

    @classmethod
    def default(cls):
        return cls.SIMPLE_TITLE.new_instance()
