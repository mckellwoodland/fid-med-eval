"""
Splits a dataset into two. Used to determine the Fréchet distance between two splits of the real distribution.
"""

# Imports
import argparse
import os
import random
import shutil
from tqdm import tqdm

# Arguments
parser = argparse.ArgumentParser()
parser._action_groups.pop()
required = parser.add_argument_group('Required Arguments')
required.add_argument('--in_dir', required=True, type=str, help='Path to folder containing dataset to split.')
required.add_argument('--out_dir1', required=True, type=str,
                      help='Path to folder to put first half of the dataset into.')
required.add_argument('--out_dir2', required=True, type=str,
                      help='Path to folder to put second half of the dataset into.')
args = parser.parse_args()
in_dir = args.in_dir
out_dir1 = args.out_dir1
out_dir2 = args.out_dir2
if not os.path.exists(out_dir1):
    os.mkdir(out_dir1)
if not os.path.exists(out_dir2):
    os.mkdir(out_dir2)

# Main code.
files = os.listdir(in_dir)
num_files = len(files)
# Randomly sample indices for the first half
indices1 = random.sample(range(num_files), num_files//2)
for i, file in tqdm(enumerate(files)):
    # If the file belongs to the first set of indices, copy it to out_dir1, else out_dir2.
    if i in indices1:
        shutil.copy(os.path.join(in_dir, file), os.path.join(out_dir1, file))
    else:
        shutil.copy(os.path.join(in_dir, file), os.path.join(out_dir2, file))


