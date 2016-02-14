from subprocess import Popen, PIPE

from .module import NLPipeModule
from .celery import app

@app.task(base=NLPipeModule)
def morphosyntactic(text):
    cmd = "$NEWSREADER_HOME/run_parser.sh"
    p2 = Popen(cmd, stdin=PIPE, stdout=PIPE, shell=True)
    (out, err) = p2.communicate(text.encode("utf-8"))
    if p2.returncode != 0:
        raise Exception("Error on calling shell command: {cmd} (see logs)".format(**locals()))
    return out
