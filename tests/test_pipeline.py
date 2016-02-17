from nose.tools import assert_equal, assert_not_equal, assert_raises
from nlpipe import pipeline, module

from elasticsearch import Elasticsearch, client
from elasticsearch.exceptions import NotFoundError

from _util import clean_es, eager_celery, create_input
from nlpipe.celery import app


@app.task(base=module.NLPipeModule)
def uppertask(text):
    return text.upper()


def test_pipeline():
    with clean_es(), eager_celery():
        id = create_input(text="Een test")
        doc = pipeline.get_result(id, uppertask)
        assert_equal(doc.text, "EEN TEST")

def test_pipeline_multiple():
    with clean_es(), eager_celery():
        id, id2 = create_input(text="Een test"), create_input(text="Nog een tesT?")
        assert_equal({}, pipeline.get_results([id, id2], uppertask, only_cached=True))
        uppertask.delay(id).get()
        results = pipeline.get_results([id, id2], uppertask, only_cached=True)
        assert_equal([id], results.keys())
        assert_equal("EEN TEST", results[id].text)
        results = pipeline.get_results([id, id2], uppertask, only_cached=False)
        assert_equal({id, id2}, set(results.keys()))
        assert_equal("NOG EEN TEST?", results[id2].text)
        
