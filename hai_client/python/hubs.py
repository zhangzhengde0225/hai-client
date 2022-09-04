from .remote_hai_model import RemoteHAIModel

class HAIHub(object):

    def __init__(self, haic):
        self.haic = haic

    def __call__(self, func, **kwargs):
        status, data = self.haic.call(func, **kwargs)
        return data
        
    def list(self):
        """列出所有模型"""
        return self('hub.list')

    def list_weights(self, name=None, *args, **kwargs):
        return self('hub.list_weights', name=name, *args, **kwargs)

    def docs(self, name):
        """获取模型的文档"""
        return self('hub.docs', name=name)

    def load(self, name, **kwargs):
        """加载模型"""
        model_name = self('hub.load', name=name, **kwargs)
        return RemoteHAIModel(name=model_name, parent=self)




