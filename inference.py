import cv2
import torch
import torch.nn as nn
from torch.utils.serialization import load_lua
import numpy as np
import os
import unet as un
from utils import *
from config import *
from convert_my_data import reshape_nyu_rgb, reshape_sun_depth


data_path = "data2"
output_path = "result"

<<<<<<< HEAD


def get_network(model_path):
    if model_path == (SUN_RGB_SCENENET_PRETRAIN or NYU_RGB_SCENENET_PRETRAIN):
        unet = un.UNet(14)

    if model_path == (SUN_RGBD_SCENENET_PRETRAIN or NYU_RGBD_SCENENET_PRETRAIN):
        unet = un.UNetRGBD(14)

    unet.load_state_dict(torch.load(model_path + '.pth'))

    if on_gpu:
        unet.cuda()

=======

def get_network(model_path, depth=False):
    unet = un.UNetRGBD(14) if depth else un.UNet(14)
    unet.load_state_dict(torch.load(model_path + '.pth', map_location='cpu'))
    if on_gpu: 
        unet.cuda()
    if not depth:
        unet.eval()
>>>>>>> 4a4b2797e227cb14e0fd138d3de260cf0c4ec43e
    return unet


def inference_batch(model_path, data_path=data_path, output_path=output_path, depth=False):
    print('Model folder:{}'.format(model_path))
    print('Data folder:{}'.format(data_path))

    os.makedirs(output_path, exist_ok=True)

    unet = get_network(model_path, depth)
        
    img_ids = list()
    for i in os.listdir(data_path):
        if i.endswith('.npy'):
            img_ids.append(i.split('.')[0].split('_')[0])
    img_ids = list(set(img_ids))

    for img_id in img_ids:
        try:
            #scaled_rgb = cv2.imread(data_path + '/{}_RGB.jpg'.format(img_id))
            scaled_rgb = np.load(data_path + '/{}_RGB.npy'.format(img_id))
            scaled_depth = np.load(data_path + '/{}_DEPTH.npy'.format(img_id))
        except Exception as e:
            print(e)
            continue
        scaled_rgb = np.expand_dims(scaled_rgb,0)
        scaled_depth = np.expand_dims(scaled_depth,0)
        torch_rgb = torch.tensor(scaled_rgb,dtype=torch.float32)
        torch_depth = torch.tensor(scaled_depth,dtype=torch.float32)
        if on_gpu:
            if depth:
                pred = unet.forward((torch_rgb.cuda(),torch_depth.cuda()))
            else:
                pred = unet.forward(torch_rgb.cuda())
            pred_numpy = pred.cpu().detach().numpy()
        else:
            if depth:
                pred = unet.forward((torch_rgb,torch_depth))
            else:
                pred = unet.forward(torch_rgb)
            pred_numpy = pred.detach().numpy()

        new_pred = np.argmax(pred_numpy[0],axis=0)

        model_name = model_path.split('/')[1]
        np.save(output_path + "/" + img_id + "_" + model_name, new_pred)


if __name__ == "__main__":
    os.makedirs(output_path, exist_ok=True)

    #inference_batch(NYU_RGB_NO_PRETRAIN, data_path, depth=False)
    #inference_batch(NYU_RGB_IMAGENET_PRETRAIN, data_path,depth=False)
    inference_batch(NYU_RGB_SCENENET_PRETRAIN, data_path, depth=False)
    #inference_batch(NYU_RGBD_NO_PRETRAIN, data_path,depth=True)
    inference_batch(NYU_RGBD_SCENENET_PRETRAIN, data_path,depth=True)

    #inference_batch(SUN_RGB_NO_PRETRAIN,data_path, depth=False)
    #inference_batch(SUN_RGB_IMAGENET_PRETRAIN, data_path, depth=False)
    inference_batch(SUN_RGB_SCENENET_PRETRAIN, data_path, depth=False)
    #inference_batch(SUN_RGBD_NO_PRETRAIN, data_path, depth=True)
    inference_batch(SUN_RGBD_SCENENET_PRETRAIN, data_path, depth=True)
