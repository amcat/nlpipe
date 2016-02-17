[![Build Status](https://travis-ci.org/amcat/nlpipe.svg?branch=master)](https://travis-ci.org/amcat/nlpipe)

# Simple NLP Pipelining based on elastic + celery

NLPipe is a very simple caching NLP pipelining system built on elasticsearch (backend) and celery (job management)

To use it, define one or more tasks based on module.NLPipeModule. 
A task should convert input (raw text or the result of earlier processing) to output.
Input documents should be in the elasticsearch store, and output will be placed there.

A calling application can then ask for the results of one or more documents. 
If the documents are already processed (cached), the result is immediately returned.
Otherwise, a processing task is placed on the celery queue. 

Inspired by [xtas](http://xtas.net)

# Installation

Install directly from github:

```{sh}
pip install git+git://github.com/amcat/nlpipe
```

To run NLPipe, you need elasticsearch and rabbitmq, both of which can be installed directly using apt:

```{sh}
sudo apt-get install elasticsearch rabbitmq-server
```

# Configuration

Configuration is contained in the `nlpipe/esconfig.py` and `nlpipe/celeryconfig.py` modules.
System (site) settings can be set using environment variables, in particular:


 - `NLPIPE_ES_HOST` - elasticsearch host (default:localhost) 
 - `NLPIPE_ES_PORT` - elasticsearch port (default:9200)
 - `NLPIPE_BROKER_HOST` - rabbitmq host (default: 127.0.0.1)
 - `NLPIPE_BROKER_PORT` - rabbitmq port (default: 5672)


