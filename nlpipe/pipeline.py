from .document import get_document, get_cached_documents, get_cached_document_ids
from elasticsearch.exceptions import NotFoundError

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

def parse_background(ids, task, max=None):
    parsed = set(get_cached_document_ids(ids, task.doc_type))
    todo = list(set(ids) - set(parsed))
    toparse = todo[:max] if max else todo
    print("{nparsed}/{n} articles already parsed, assigning {ntoparse} out of {ntodo}"
          .format(n=len(ids), nparsed=len(parsed), ntoparse=len(toparse), ntodo=len(todo)))

    for id in toparse:
        task.apply_async(args=[id], queue='background')
