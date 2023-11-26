"""
Preprocess MSD brain images.

Processing:
1. Separate the 4D image into 4 types (FLAIR, T1w, T1gd, T2w).
2. Converts to 2D slices. It only keeps the slices where at least 15% of the pixels are non-zero.
3. Rescales individual slices to the range [0, 255].
4. Pads images with 0 pixels so the slice is of shape (256, 256).
"""

# Imports
import argparse
import os
import tqdm
import SimpleITK as sitk
import numpy as np

# Arguments
parser = argparse.ArgumentParser()
parser._action_groups.pop()
required = parser.add_argument_group('Required Arguments')
required.add_argument('--in_dir', required=True, type=str, help='Path to folder containing 3D NIfTIs to convert')
required.add_argument('--out_dir', required=True, type=str, help='Path to folder to put consolidated and scaled 2D NIfTi slices into')
args = parser.parse_args()
in_dir = args.in_dir
out_dir = args.out_dir
if not os.path.exists(out_dir):
  os.mkdir(out_dir)

# Functions.
def pad_image(img, res):
  """
  Pad image so that it is a certain resolution.
  
  Inputs:
    img (nparray): img to be padded
    res (int): desired resolution
  """
  h, w = img.shape
  pad_h, pad_w = res - h, res - w
  if pad_w % 2 == 0:
    l_pad, r_pad = pad_w // 2, pad_w // 2
  else:
    l_pad, r_pad = pad_w // 2 - 1, pad_w // 2 + 1
  if pad_h % 2 == 0:
    t_pad, b_pad = pad_h // 2, pad_h // 2
  else:
    t_pad, b_pad = pad_h // 2 - 1, pad_h // 2 + 1
  data = np.pad(img, ((t_pad, b_pad),(l_pad, r_pad)))
  return data

# Main code.
for fname in tqdm.tqdm(os.listdir(in_dir)):
  prefix = fname[:-7]
  img4d = sitk.ReadImage(os.path.join(in_dir, fname))
  for img_type in range(4):
    img = img4d[:,:,:,img_type]
    img = sitk.RescaleIntensity(img)
    for i in range(img.GetSize()[2]):
      out_path = os.path.join(out_dir, prefix + f'_{img_type}_{i}.nii.gz')
      if not os.path.exists(out_path):
        img_slice = img[:,:,i]
        slice_data = sitk.GetArrayFromImage(img_slice)
        slice_data = pad_image(slice_data, 256)
        ratio = (slice_data > 0).sum() / (slice_data > -1).sum()
        if ratio > 0.15:
            sitk.WriteImage(sitk.GetImageFromArray(slice_data), out_path)
