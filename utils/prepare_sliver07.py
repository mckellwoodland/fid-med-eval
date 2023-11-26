"""
Prepare the SLIVER07 images.
1. Convert MHD files to 2D NIfTI images.
2. Rescale images to 0-255.
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
required.add_argument('--in_dir', required=True, type=str, help='Path to folder containing original MHD files.')
required.add_argument('--out_dir', required=True, type=str, help='Path to folder to put processed NIfTIs into.')
args = parser.parse_args()
in_dir = args.in_dir
out_dir = args.out_dir
if not os.path.exists(out_dir):
  os.mkdir(out_dir)

# Functions
def convert_range(image, min_old, max_old, min_new, max_new):
    return (image - min_old) * (max_new - min_new) / (max_old - min_old) + min_new

# Main code.
for fname in tqdm.tqdm([f for f in os.listdir(in_dir) if f.endswith('.mhd')]):
  prefix = fname[:-4]
  img = sitk.ReadImage(os.path.join(in_dir, fname), imageIO="MetaImageIO")
  min_max_filter = sitk.MinimumMaximumImageFilter()
  min_max_filter.Execute(img)
  img_min, img_max = min_max_filter.GetMinimum(), min_max_filter.GetMaximum()
  for i in range(img.GetSize()[2]):
    img_slice = img[:,:,i]
    slice_np = sitk.GetArrayFromImage(img_slice)
    # Change slice to range [0, 255]
    slice_rescale = convert_range(slice_np, slice_np.min(), slice_np.max(), 0., 255.)
    slice_out = sitk.GetImageFromArray(slice_rescale)
    slice_out.CopyInformation(img_slice)
    slice_out.SetSpacing((img.GetSpacing()[0], img.GetSpacing()[1]))
    sitk.WriteImage(slice_out, os.path.join(out_dir, prefix + f'_{i}.nii.gz'))
