from .document import get_document, get_cached_documents
from elasticsearch.exceptions import *

def get_result(id, task):
    try:
        return get_document(id, task.doc_type)
    except NotFoundError:
        t = task.delay(id)
        t.wait()
        return get_document(id, task.doc_type)
        

def get_results(ids, task, only_cached=False):
    docs = dict(get_cached_documents(ids, task.doc_type))
    if not only_cached:
        for id in ids:
            if id not in docs:
                docs[id] = get_result(id, task)
    return docs
