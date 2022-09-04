import os, sys
from pathlib import Path
import damei as dm
import copy
pydir = Path(os.path.abspath(__file__)).parent

try:
    import hai
except ImportError:
    hai_root = f'{pydir.parent.parent.parent}/hai'
    sys.path.insert(0, hai_root)
    import hai
    sys.path.pop(0)

logger = dm.getLogger('remote_hai_model')

class RemoteHAIModel(object):
    def __init__(self, name, parent):
        self.name = name  # 模型名
        self.parent = parent  # 父类，一般是HAIHub
        self.haic = parent.haic  # hai client

        self._config = None  # 模型配置
        self._config_dict = None  # 模型配置内部的字典，存储本地未修改前的配置，用于比较以知晓是否需要同步到服务器

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"

    def __call__(self, x, *args, **kwargs):
        return self.forward(x)

    @property
    def cfg(self):
        return self.config
    
    @property
    def config(self):
        if self._config is None:
            s, data = self.haic.call('model_config', name=self.name)
            self._config = hai.Config.from_dict(data)
            self._config_dict = copy.copy(self._config.__dict__)
        return self._config  # 一直本地

    def set_config(self):
        """自动判断是否需要同步，本地配置同步到服务器"""
        cfg = self._config
        cfg_dict = cfg.__dict__  # 当前的配置
        is_dirty = cfg_dict != self._config_dict  # 是否有修改
        if is_dirty:
            # print('Sync config to server')
            s, data = self.haic.call('set_config', name=self.name, cfg=self.config.to_dict())
            assert s == 1, f'Failed to set config: {data}'
            self._config_dict = copy.copy(cfg_dict)
    
    def forward(self, x):
        self.set_config()  # 本地配置同步到服务器
        logger.info(f'Forward, waiting for results...')
        s, data = self.haic.call('forward', data=x)  # 调用
        return data
    
