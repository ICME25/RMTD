import os
from PIL import Image
import os.path
import time
import torch
import torchvision.datasets as dset
import torchvision.transforms as trn
import torch.utils.data as data
import numpy as np
from PIL import Image
# /////////////// Distortion Helpers ///////////////
import skimage as sk
from skimage.filters import gaussian
from io import BytesIO
from wand.image import Image as WandImage
from wand.api import library as wandlibrary
import wand.color as WandColor
import ctypes
from PIL import Image as PILImage
import cv2
from scipy.ndimage import zoom as scizoom
from scipy.ndimage.interpolation import map_coordinates
import warnings
class MotionImage(WandImage):
    def motion_blur(self, radius=0.0, sigma=0.0, angle=0.0):
        wandlibrary.MagickMotionBlurImage(self.wand, radius, sigma, angle)


def gaussian_blur(x, severity=1):
    c = [.4, .6, 0.7, .8, 1][severity - 1]

    x = gaussian(np.array(x) / 255., sigma=c, multichannel=True)
    return np.clip(x, 0, 1) * 255


def motion_blur(x, severity=1):
    c = [(6,1), (6,1.5), (6,2), (8,2), (9,2.5)][severity - 1]

    output = BytesIO()
    x.save(output, format='PNG')
    x = MotionImage(blob=output.getvalue())

    x.motion_blur(radius=c[0], sigma=c[1], angle=np.random.uniform(-45, 45))

    x = cv2.imdecode(np.fromstring(x.make_blob(), np.uint8),
                     cv2.IMREAD_UNCHANGED)

    # if x.shape != (32, 32):
    return np.clip(x[..., [2, 1, 0]], 0, 255)  # BGR to RGB
    # else:  # greyscale to RGB
    #     return np.clip(np.array([x, x, x]).transpose((1, 2, 0)), 0, 255)
convert_img = trn.Compose([trn.ToTensor(), trn.ToPILImage()])
input_dir = ""
output_dir = ""
imgs = os.listdir(input_dir)
for i in imgs:
    img = convert_img(cv2.imread(input_img))
    res = gaussian_blur(img, 3)
    #res = motion_blur(img, 3)
    cv2.imwrite(output_dir + i, res) # mb, gb