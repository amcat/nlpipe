from .module import NLPipeModule

class TestModule(NLPipeModule):
    def process(self, text):
        return "<xml bla joh>"        
        
