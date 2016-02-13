import os
ES_HOST=os.environ.get("XTAS_ES_HOST", 'localhost')
ES_PORT=int(os.environ.get("XTAS_ES_PORT", 9200))

ES_INPUT_INDEX = "amcat"
ES_INPUT_DOCTYPE = "article"
ES_INPUT_FIELDS = ["headline", "text"]

ES_RESULT_INDEX = "nlpipe"

_ES_ID = dict(type="string", index="not_analyzed")
_ES_DATA = dict(type="string", index="no")
_ES_TIME = dict(type="date", format="dateOptionalTime")

ES_MAPPING = {"properties": {
    "id": _ES_ID,
    "result": _ES_DATA,
    "pipeline": {"properties": {"begin_time": _ES_TIME,
                                "end_time": _ES_TIME,
                                "module": _ES_ID,
                                "version": _ES_ID,
                                "input_type": _ES_ID,
                                "input_fields": _ES_ID}}}}