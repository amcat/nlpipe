from contextlib import contextmanager
import logging
from unittest import SkipTest
from elasticsearch import Elasticsearch, client
from nlpipe import backend, esconfig, celeryconfig

ES_TEST_INDEX = "nlpipe__unittest"

@contextmanager
def clean_es():
    "provide a clean elasticsearch instance for unittests"
    if not backend._es.ping():
        raise SkipTest("ElasticSearch host not found, skipping elastic tests")
        
    indexclient = client.indices.IndicesClient(backend._es)
    if indexclient.exists(ES_TEST_INDEX):
        logging.info("Deleting existing test index")
        indexclient.delete(ES_TEST_INDEX)
    logging.info("Creating test index")        
    indexclient.create(ES_TEST_INDEX)
    backend._CHECKED_MAPPINGS = set()

    _old = esconfig.ES_INPUT_INDEX, esconfig.ES_RESULT_INDEX
    esconfig.ES_INPUT_INDEX = esconfig.ES_RESULT_INDEX = ES_TEST_INDEX
    try:
        yield 
    finally:
        logging.info("Deleting test index")
        indexclient.delete(ES_TEST_INDEX)
        esconfig.ES_INPUT_INDEX, esconfig.ES_RESULT_INDEX = _old

@contextmanager
def eager_celery():
    _old = celeryconfig.CELERY_ALWAYS_EAGER
    celeryconfig.CELERY_ALWAYS_EAGER = True
    try:
        yield
    finally:
        celeryconfig.CELERY_ALWAYS_EAGER = _old
        
    
def create_input(text="dit is een test"):
    x = backend._es.index(index=esconfig.ES_INPUT_INDEX, doc_type=esconfig.ES_INPUT_DOCTYPE, body={"text": text})
    backend._es.indices.flush()
    return x['_id']
