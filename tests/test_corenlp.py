

from __future__ import unicode_literals

import os
import logging
from unittest import SkipTest
from nlpipe.modules import corenlp

from nose.tools import assert_equal, assert_in

from io import BytesIO

from KafNafParserPy import KafNafParser


def _check_corenlp():
    v = corenlp.get_corenlp_version()
    if not v:
        raise SkipTest("CoreNLP not found at CORENLP_HOME")

def test_parse():
    _check_corenlp()
    result = corenlp.parse("This is a test", annotators=corenlp.LEMMATIZER)
    assert_in("<lemma>be</lemma>", result)

def test_corenlp2naf():
    xml = open(os.path.join(os.path.dirname(__file__), "test_corenlp.xml")).read()
    naf_bytes = corenlp.corenlp2naf(xml, corenlp.PARSER)
    naf = KafNafParser(BytesIO(naf_bytes))
    terms = {t.get_id(): t.get_lemma() for t in naf.get_terms()}
    assert_equal(set(terms.values()), {"John", "attack", "I", "in", "London", "hit", "he", "back", "."})
    london = [t for t in naf.get_terms() if t.get_lemma() == 'London'][0]
    assert_equal(london.get_pos(), 'R')
    assert_equal(london.get_morphofeat(), 'NNP')

    ents = {}
    for e in naf.get_entities():
        for ref in e.get_references():
            for term_id in ref.get_span().get_span_ids():
                ents[terms[term_id]] = e.get_type()
    assert_equal(ents, {"John": "PERSON", "London": "LOCATION"})

    deps = {terms[d.get_from()]: (d.get_function(), terms[d.get_to()])
            for d in naf.get_dependencies()}
    expected = {'I': ('nsubj', 'hit'),
                'John': ('nsubj', 'attack'),
                'London': ('prep_in', 'attack'),
                'back': ('advmod', 'hit'),
                'he': ('dobj', 'hit')}
    assert_equal(deps, expected)

    corefs = []
    for coref in naf.get_corefs():
        corefs.append(set())
        for span in coref.get_spans():
            corefs[-1] |= {terms[t] for t in span.get_span_ids()}
    assert_in({"John", "he"}, corefs)
    
def test_corenlp_naf():
    _check_corenlp()
    naf_bytes = corenlp.corenlp_naf("John shoots himself", annotators=corenlp.LEMMATIZER)
    print naf_bytes
    naf = KafNafParser(BytesIO(naf_bytes))

    terms = {t.get_id(): t.get_lemma() for t in naf.get_terms()}
    assert_equal(set(terms.values()), {"John", "shoot", "himself"})

    
if __name__ == '__main__':
    naf = test_corenlp_naf()
