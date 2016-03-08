"""
Test the Frog tagger/lemmatizer functions and task.
"""

import logging
from unittest import SkipTest
import os.path
import socket;
from cStringIO import StringIO

from nose.tools import assert_equal, assert_in

from nlpipe.modules.frog import call_frog
from nlpipe.tasks import frog

from KafNafParserPy import KafNafParser

def _check_frog(host="localhost", port=9887):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if not result == 0:
        raise SkipTest("No frog server found at {host}:{port}"
                       .format(**locals()))

def test_frog():
    _check_frog()
    tokens = list(call_frog("Mark Rutte werkte gisteren nog bij de  Vrije Universiteit in Amsterdam"))
    #print "\n".join(map(str, tokens)), "\n", "\n".join(map(str, entities))
    assert_equal(len(tokens), 10)
    assert_equal(tokens[0].lemma, 'Mark_Rutte')
    assert_equal(tokens[0].pos, 'R')
    assert_equal(tokens[1].pos, 'V')
    assert_equal(tokens[-1].word, 'Amsterdam')
    
    #assert_equal(len(entities), 3)
    #assert_in({'tokens': [6,7], 'type': 'ORG'}, entities)

def test_frog_saf():
    _check_frog()
    naf_str = frog._process("Mark Rutte werkte gisteren nog bij de  Vrije Universiteit in Amsterdam")

    naf = KafNafParser(StringIO(naf_str))
    lemmata = {t.get_lemma() for t in naf.get_terms()}
    assert_equal(lemmata, {"Mark_Rutte", "werken", "gisteren", "nog", "bij",
                           "de", "vrij", "universiteit", "in", "Amsterdam"})

    
