from app.domain.model.templates.templates import Templates


async def get_templates() -> dict:
    records = []
    for template in Templates.__members__.values():
        records.append({'id': template, 'text': ' '.join([word.capitalize() for word in template.split('_')])})
    return {'records':records}
