"""
Prepare the ACDC images.
1. Convert 4D to 2D NIfTIs.
2. Pad image so that it is square.
3. Resize image to shape (256, 256).
4. Rescale image to range [0, 255].
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
required.add_argument('--in_dir', required=True, type=str, help='Path to folder containing original 4D NIfTIs.')
required.add_argument('--out_dir', required=True, type=str, help='Path to folder to put processed 2D NIfTi slices into.')
args = parser.parse_args()
in_dir = args.in_dir
out_dir = args.out_dir
if not os.path.exists(out_dir):
  os.mkdir(out_dir)

# Functions.
def pad_image(img):
  """
  Pad image so that it is square. Uses SimpleITK code from Bing Chat AI.
  """
  data = sitk.GetArrayFromImage(img)
  h, w = data.shape
  res = max([h,w])
  pad_h, pad_w = res - h, res - w
  if pad_w % 2 == 0:
    l_pad, r_pad = pad_w // 2, pad_w // 2
  else:
    l_pad, r_pad = pad_w // 2 - 1, pad_w // 2 + 1
  if pad_h % 2 == 0:
    t_pad, b_pad = pad_h // 2, pad_h // 2
  else:
    t_pad, b_pad = pad_h // 2 - 1, pad_h // 2 + 1
  
  min_pixel_value = data.min()
  pad_filter = sitk.ConstantPadImageFilter()
  pad_filter.SetPadLowerBound([l_pad, b_pad, 0])
  pad_filter.SetPadUpperBound([r_pad, t_pad, 0])
  pad_filter.SetConstant(float(min_pixel_value))
  padded_image = pad_filter.Execute(img)
  return padded_image

def resize_image(img, new_size):
  """
  Function from Bing Chat AI
  """
  size = img.GetSize()
  spacing = img.GetSpacing()
  new_spacing = [osz*osp/nsp for osz, osp, nsp in zip(size, spacing, new_size)]

  resampler = sitk.ResampleImageFilter()
  resampler.SetSize(new_size)
  resampler.SetOutputSpacing(new_spacing)
  resampler.SetOutputDirection(img.GetDirection())
  resampler.SetOutputOrigin(img.GetOrigin())
  resampler.SetTransform(sitk.Transform())
  resampler.SetDefaultPixelValue(img.GetPixelIDValue())
  resampler.SetInterpolator(sitk.sitkBSpline)

  return resampler.Execute(img)
# Main code.
for folder in tqdm.tqdm(os.listdir(in_dir)):
  if 'patient' in folder:
    for fname in os.listdir(os.path.join(in_dir, folder)):
      prefix = fname[:-7]
      if '4d' in prefix:
        img4d = sitk.ReadImage(os.path.join(in_dir, folder, fname))
        size = img4d.GetSize()
        for i in range(1):
          img3d = img4d[:,:,:,i]
          for j in range(size[2]):
            out_path = os.path.join(out_dir, prefix + f'_{i}_{j}.nii.gz')
            if not os.path.exists(out_path):
              img2d = img3d[:,:,j]
              img2d_fl = sitk.Cast(img2d, sitk.sitkFloat32)
              # Pad image so it is square
              img2d_square = pad_image(img2d_fl)
              # resize image here
              img2d_256 = resize_image(img2d_square, [256, 256])
              # Rescale to [0,255]
              img2d_0_255 = sitk.RescaleIntensity(img2d_256, 0., 255.)
              sitk.WriteImage(img2d_0_255, out_path)
