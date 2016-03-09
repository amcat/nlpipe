from __future__ import unicode_literals

from nose.tools import assert_equal, assert_not_equal, assert_raises
from nlpipe import module

from elasticsearch import Elasticsearch, client
from elasticsearch.exceptions import NotFoundError

from _util import clean_es, create_input
from nlpipe.celery import app


@app.task(base=module.NLPipeModule, version="0.1")
def uppertask(text):
    return text.upper()
    
@app.task(base=module.NLPipeModule, doc=True, output_doc_type="XXX")
def doclowertask(doc):
    return doc.text.lower()
    
def test_doc_type():
    assert_equal(uppertask.doc_type, "uppertask__0_1")
    assert_equal(doclowertask.doc_type, "XXX")
                 

def test_module():
    with clean_es():
        id = create_input("Dit is een Test")
        uppertask(id)
        d = uppertask.get_result(id)
        assert_equal(d.text, "DIT IS EEN TEST")
        assert_equal(d.pipeline[0]["module"], "test_module.uppertask")
        assert_equal(d.pipeline[0]["version"], "0.1")

        doclowertask(id)
        d = doclowertask.get_result(id)
        assert_equal(d.text, "dit is een test")

@app.task(base=module.NLPSystemModule)
def errortask(text):
    pass
    
@app.task(base=module.NLPSystemModule, cmd="perl -ne 'print lc'")
def systemtask(text):
    pass
        
@app.task(base=module.NLPSystemModule, cmd="perl -ne 'print uc'")
def systemtask_postprocess(text):
    return text + " (postprocessed)"
    
def test_system_module():
    with clean_es():
        id = create_input("DIT IS EEN TEST")
        assert_raises(ValueError, errortask, id)
        systemtask(id)
        d = systemtask.get_result(id)
        assert_equal(d.text, "dit is een test")
        
        id = create_input("Nog een test")
        systemtask_postprocess(id)
        d = systemtask_postprocess.get_result(id)
        assert_equal(d.text, "NOG EEN TEST (postprocessed)")
