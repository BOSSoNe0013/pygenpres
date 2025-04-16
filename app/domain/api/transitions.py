from app.domain.model.transitions.transitions import Transitions


async def get_transitions() -> dict:
    records = []
    for transition in Transitions.__members__.values():
        records.append({'id': transition, 'text': ' '.join([word.capitalize() for word in transition.split('_')])})
    return {'records':records}
