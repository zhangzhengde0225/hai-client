"""通过继承类的方式实现远程模型的推理"""


import os, sys
from pathlib import Path

import hai_client
import cv2
import numpy as np


hai = hai_client.HAIClient(ip='localhost', port=9999)

class UNet(hai.nn.UNet):
    pass



    


