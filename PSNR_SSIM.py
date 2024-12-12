import argparse
from skimage import data, util,io
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import os
parser = argparse.ArgumentParser(description='PSNR_SSIM')
parser.add_argument('--res_dir', default='', type=str, help='Directory of validation images')
parser.add_argument('--ori_dir', default='', type=str, help='Directory for clean images')
args = parser.parse_args()
imgs = os.listdir(args.res_dir)
ssim_list = []
psnr_list = []
for i in imgs:
	img_res = io.imread(args.res_dir + i)
	img_ori = io.imread(args.ori_dir + i.replace('degraded', 'GT'))
	ssim = structural_similarity(img_res, img_ori, multichannel = True)
	ssim_list.append(ssim)
	psnr = peak_signal_noise_ratio(img_res, img_ori)
	psnr_list.append(psnr)
	#with open(os.path.join(args.res_dir.split(args.res_dir.split('/')[-2])[0], args.res_dir.split('/')[-2] +
	#                       'psnr_ssim.txt'),'a') as f:
	#	f.write(i+'---->'+"PSNR: %.4f, SSIM: %.4f] "% (psnr, ssim)+'\n')
print('psnr:', sum(psnr_list)/len(psnr_list))
print('ssim:', sum(ssim_list)/len(ssim_list))