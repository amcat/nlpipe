from .document import get_document
from elasticsearch.exceptions import *

def get_result(id, task):
    try:
        return get_document(id, task.doc_type)
    except NotFoundError:
        t = task.delay(id)
        t.wait()
        return get_document(id, task.doc_type)
        

def get_results(ids, task):
    return [get_result(id, task) for id in ids]
