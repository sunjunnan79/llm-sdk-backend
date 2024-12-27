import pkg.llm

models = {}


def initModels(config):
    global models
    models = pkg.llm.initModels(config)


class Service:
    def __init__(self):
        # 初始化models
        self.models = models

    def invoke(self):
        return
