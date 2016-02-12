#!/usr/bin/env python

from distutils.core import setup

setup(
    name="nlpip",
    description="Simple NLP Pipelinining using Elastic and Celery",
    author="Wouter van Atteveldt",
    author_email="wouter@vanatteveldt.com",
    packages=["nlpipe"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing",
    ],
    install_requires=[
        "celery>=3.0.0",
        "elasticsearch",
    ],
)
