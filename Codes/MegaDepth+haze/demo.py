import torch
import sys
from torch.autograd import Variable
import numpy as np
from options.train_options import TrainOptions
opt = TrainOptions().parse()  # set CUDA_VISIBLE_DEVICES before import torch
from data.data_loader import CreateDataLoader
from models.models import create_model
from skimage import io
from skimage.transform import resize
import os
import re

model = create_model(opt)
input_dir = ""
output_dir = ""
A = 0.6    #0.6, 0.8
beta = 0.8   #0.8, 1.2

def test_simple(model):
    model.switch_to_eval()
    imgs = os.listdir(input_dir)
    for i in imgs:
        img = np.float32(io.imread(input_dir + i))/255.0
        # img = resize(img, (input_height, input_width), order = 1)
        input_img = torch.from_numpy( np.transpose(img, (2,0,1)) ).contiguous().float()
        input_img = input_img.unsqueeze(0)

        input_images = Variable(input_img.cuda())
        pred_log_depth = model.netG.forward(input_images)
        pred_log_depth = torch.squeeze(pred_log_depth)
        pred_depth = torch.exp(pred_log_depth)
        pred_depth = pred_depth.data.cpu().numpy()
        t = np.exp(-beta * pred_depth)
        t = t.reshape(400, 400, 1)
        t = np.tile(t, (1, 1, 3))
        res = np.multiply(img, t) + np.multiply(A, (1 - t))
        io.imsave(output_dir + i, res)# sh, dh

        # pred_inv_depth = 1/pred_depth
        # pred_inv_depth = pred_inv_depth.data.cpu().numpy()
        # # you might also use percentile for better visualization
        # pred_inv_depth = pred_inv_depth/np.amax(pred_inv_depth)
        #
        # io.imsave('demo.png', pred_inv_depth)
        # # print(pred_inv_depth.shape)
        # sys.exit()



test_simple(model)
print("We are done")
