from __future__ import absolute_import

import datetime

from .celery import app
from .document import get_document, get_input, store_result

class NLPipeModule(app.Task):
    """
    Preprocessing module
    """
    abstract = True
    version = "0.0"
    input_doc_type = None # defaults to text (raw) input
    output_doc_type = None # defaults to name
    doc =False # if true, pass document rather than just input

    def __init__(self, *args, **kwargs):
        super(NLPipeModule, self).__init__(*args, **kwargs)
        self.process = self.run
        self.run = self.run_wrapper


    def run_wrapper(self, id):
        if self.input_doc_type is None:
            # task is based on raw input
            doc = get_input(id)
        else:
            doc = get_document(id, self.input_doc_type)
        begin_time = datetime.datetime.now()
        result = self.process(doc if self.doc else doc.input)
        end_time = datetime.datetime.now()

        provenance  = dict(module=self.name, version=self.version,
                           input_type=doc.input_type, input_fields=doc.input_fields,
                           begin_time=begin_time, end_time=end_time)
        
        doc_type = self.output_doc_type or self.name.split(".")[-1]
        
        store_result(doc_type, id, doc.pipeline + [provenance], result)
