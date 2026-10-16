DEFAULT_MODEL = "busecarik/berturk-sunlp-ner-turkish"
PERSON_LABELS = {"PER", "PERSON"}

_pipelines = {}


def _get_pipeline(model_name: str):
    if model_name not in _pipelines:
        from transformers import pipeline
        _pipelines[model_name] = pipeline(
            "ner", model=model_name, aggregation_strategy="simple", stride=128
        )
    return _pipelines[model_name]


def find_person(text: str, model_name: str = DEFAULT_MODEL) -> list[str]:
    ner = _get_pipeline(model_name)
    result = []
    for entity in ner(text):
        if entity["entity_group"] in PERSON_LABELS:
            name = text[entity["start"]:entity["end"]].strip()
            if name and name not in result:
                result.append(name)
    result.sort(key=len, reverse=True)
    return result