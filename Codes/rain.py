import cv2
import os
import re
import numpy as np
import random
input_dir = ""
output_dir = ""
value = 5 # 2, 5
length = 15 # 10, 15
beta = 0.6 # 0.6, 0.8
imgs = os.listdir(input_dir)
for i in imgs:
	img = cv2.imread(input_dir + i)
	noise = np.random.uniform(0, 256, img.shape[0:2])
	noise[np.where(noise < (256 - value))] = 0
	k = np.array([[0, 0.1, 0], [0.1, 8, 0.1], [0, 0.1, 0]])
	noise = cv2.filter2D(noise, -1, k)
	angle = random.randint(145, 215)
	if angle <= 180:
		angle = angle - 10
	else:
		angle = angle + 10
	trans = cv2.getRotationMatrix2D((length / 2, length / 2), angle-45, 1-length/100.0)
	dig = np.diag(np.ones(length))
	k=cv2.warpAffine(dig, trans, (length, length))
	k = cv2.GaussianBlur(k, (3, 3), 0)
	blurred = cv2.filter2D(noise, -1, k)
	cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
	rain = np.array(blurred, dtype=np.uint8)
	rain = np.expand_dims(rain, 2)
	rain = np.repeat(rain, 3, 2)
	# # 加权合成新图
	# res = cv2.addWeighted(img, beta, rain, 1 - beta, 1)
	res = img.copy()
	res[:, :, 0] = res[:, :, 0] * (255.0 - rain[:, :, 0])/255.0 + beta * rain[:, :, 0]
	res[:, :, 1] = res[:, :, 1] * (255.0 - rain[:, :, 1])/255.0 + beta * rain[:, :, 1]
	res[:, :, 2] = res[:, :, 2] * (255.0 - rain[:, :, 2])/255.0 + beta * rain[:, :, 2]
	cv2.imwrite(output_dir + i, res) # lr, hr

