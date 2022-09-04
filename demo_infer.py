

import re
import hai_client
import cv2
import numpy as np

ip = 'localhost'
port = 9999
hai = hai_client.HAIClient(ip=ip, port=port)

modules = hai.hub.list()  # 列出所有模型
print(f'Modules: \n{modules}')
model_name = 'UNet'

weights = hai.hub.list_weights(name=model_name)  # 列出所有模型权重，
print(f'Weights: \n{weights} {type(weights)}')

docs = hai.hub.docs(model_name)

model = hai.hub.load(model_name,   # 根据模型名称加载云模型
    weights=f'hai/unet/unet_v1.0.pth',  # 指定模型权重文件
    )
print('Model:', model)

config = model.config  # 获取模型配置
# config.weights = "runs/unet_exp/weights/checkpoint_epoch5.pth"  # 第二种指定模型权重文件的方法
print('Config:', config)

img = cv2.imread('data/car.jpg')
# img = cv2.resize(img, (256, 256))
ret = model(img)  # 本地的图像，调用远程接口返回结果
if model_name == 'UNet':  # UNet返回类型ndarray，但grpc不支持，需要额外转换
    ret = np.array(ret)
print('Result:', type(ret), ret.shape)
# 保存结果：结果是(2, h, w)的ndarray，2个维度分别是第0类和第1类的概率
ret = np.array(ret*255, dtype=np.uint8)
cv2.imwrite('data/car_out_class0.jpg', ret[0])
cv2.imwrite('data/car_out_class1.jpg', ret[1])
