"""
Assign articles from AmCAT sets for background processing in nlpipe
"""

import sys, argparse

from nlpipe import tasks
from nlpipe.pipeline import parse_background
from nlpipe.backend import get_input_ids
from nlpipe.celery import app

modules = {n.split(".")[-1]: t for (n,t) in app.tasks.iteritems() if n.startswith("nlpipe")}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('module', help='nlpipe module (task) name ({})'.format(", ".join(sorted(modules))),
                    choices=modules, metavar="module")
parser.add_argument('sets', type=int, nargs='+', help='Article set id(s)')
parser.add_argument('--max', type=int, help='maximum number of articles to assign')

args = parser.parse_args()

task = modules[args.module]

body = {u'filter': {'terms': {u'sets': args.sets}}}
print("Assigning {max} articles from set(s) {args.sets} for processing by {task.name}"
      .format(max=("up to {}".format(args.max) if args.max is not None else "all"), **locals()))
ids = list(get_input_ids(body))
parse_background(ids, task, max=args.max)
