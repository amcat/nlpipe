"""
Useful functions for communication with elastic

NLPipe assumes that raw texts are stored in an elastic index (see esconfig).
If multiple fields are specified, and/or a field contains multiple results,
they are joined with empty lines in between (e.g. "\n\n".join)

Results are stored in a separate document type per module (version), and are assumed to have the form:
{id: <id>,
 pipeline: [{module: <module>, version: <version>, 
            input_type: <doctype>, input_fields: [<fields>] (raw input only),
            begin_time: <time>, end_time: <time>}]
 result: <result>}
"""

import datetime

from elasticsearch import Elasticsearch

from . import esconfig

_es = Elasticsearch([{"host": esconfig.ES_HOST, "port": esconfig.ES_PORT}])

_CHECKED_MAPPINGS = set()

def _check_mapping(doc_type):
    if doc_type not in _CHECKED_MAPPINGS:
        index = esconfig.ES_RESULT_INDEX
        if not _es.indices.exists_type(index=index, doc_type=doc_type):
            mapping = {doc_type: esconfig.ES_MAPPING}
            if not _es.indices.exists(index):
                _es.indices.create(index)
            _es.indices.put_mapping(index=index, doc_type=doc_type, body=mapping)
        _CHECKED_MAPPINGS.add(doc_type)

def get_input(id):
    input_type = esconfig.ES_INPUT_DOCTYPE,
    input_fields = esconfig.ES_INPUT_FIELDS
    res = _es.get(index=esconfig.ES_INPUT_INDEX,
                  doc_type=input_type,
                  id=id, fields=esconfig.ES_INPUT_FIELDS)
    text = "\n\n".join("\n\n".join(res['fields'][f]) for f in esconfig.ES_INPUT_FIELDS)
    return Document(id, [], text, input_type, input_fields)

def get_cached_documents(ids, doc_type):
    res = _es.mget(index=esconfig.ES_RESULT_INDEX,
                   doc_type=doc_type, body={"ids": ids})
    for doc in res['docs']:
        if doc['found']:
            d = Document(int(doc['_id']), doc['_source']['pipeline'], doc['_source']['result'], doc_type)
            yield d.id, d
    
def get_document(id, doc_type):
    res= _es.get(index=esconfig.ES_RESULT_INDEX,
                 doc_type=doc_type, id=id)
    return Document(id, res['_source']['pipeline'], res['_source']['result'], doc_type)

def store_result(doc_type, id, pipeline, result):
    _check_mapping(doc_type)
    body = dict(id=id, pipeline=pipeline, result=result)
    _es.index(index=esconfig.ES_RESULT_INDEX,
              doc_type=doc_type,
              body = body,
              id = id)

def exists(doc_type, id):
    return _es.exists(index=esconfig.ES_RESULT_INDEX,
                      doc_type=doc_type, id=id)
    
class Document(object):
    def __init__(self, id, pipeline, input, input_type, input_fields=None):
        self.id = id
        self.pipeline = pipeline
        self.input = input
        self.input_type = input_type
        self.input_fields = input_fields
