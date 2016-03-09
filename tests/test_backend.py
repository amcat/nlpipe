from __future__ import unicode_literals

from nose.tools import assert_equal, assert_not_equal, assert_raises
from nlpipe import backend

from elasticsearch import Elasticsearch, client
from elasticsearch.exceptions import NotFoundError

from _util import clean_es, create_input

def test_get_input():
    with clean_es():
        id = create_input(text="Een test")
        d = backend.get_input(id)
        assert_equal(d.text, "Een test")
        assert_equal(d.id, id)


def test_get_results():
    with clean_es():
        id, id2 = create_input(text="Een test"), create_input(text="Nog een test")
        
        doc_type = "TEST"
        assert_raises(NotFoundError, backend.get_document, id, doc_type)
        assert_equal([], list(dict(backend.get_cached_documents([id, id2], doc_type)).keys()))

        backend.store_result(doc_type, id, [{"module": "TEST"}], "test result")
        backend._es.indices.flush()
        d2 = backend.get_document(id, doc_type)
        assert_equal(d2.pipeline, [{"module": "TEST"}])
        assert_equal(d2.text, "test result")

        assert_equal([id], list(dict(backend.get_cached_documents([id, id2], doc_type)).keys()))
        assert_equal(1, dict(backend.count_cached([id, id2]))[doc_type])
        
