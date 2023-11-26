"""
Prepare the ChestX-ray14 images.
1. Convert all PNG images in a folder to grayscale.
"""

# Imports
import argparse
import os
import tqdm
from PIL import Image

# Arguments
parser = argparse.ArgumentParser()
parser._action_groups.pop()
required = parser.add_argument_group('Required Arguments')
required.add_argument('--in_dir', required=True, type=str, help='Path to folder containing original PNGs.')
required.add_argument('--out_dir', required=True, type=str, help='Path to folder to put processed PNGs into.')
args = parser.parse_args()
in_dir = args.in_dir
out_dir = args.out_dir
if not os.path.exists(out_dir):
  os.mkdir(out_dir)

# Main code
for fname in tqdm.tqdm(os.listdir(in_dir)):
  image = Image.open(os.path.join(in_dir, fname))
  image = image.convert('L')
  image.save(os.path.join(out_dir, fname))
