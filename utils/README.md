# Docker

Build Docker container

```
docker build -t {CONTAINER_NAME} .
```

Run the docker container.

```
docker run -it {CONTAINER_NAME} /bin/bash
```

If you need access to files outside of the preprocessing folder, you can mount a directory.

```
docker run -it -v {DIR}:/workspace {CONTAINER_NAME} /bin/bash
```

# Preprocessing Images
## ChestX-ray14
Download dataset from [this url](https://nihcc.app.box.com/v/ChestXray-NIHCC/folder/37178474737).

Convert all images to one channel images (about 1,000 have four channels).
```
usage: prepare_chestxray14.py [-h] --in_dir IN_DIR --out_dir OUT_DIR

Required Arguments:
  --in_dir IN_DIR    Path to folder containing original PNGs.
  --out_dir OUT_DIR  Path to folder to put processed PNGs into.
```

## SLIVER07
Download dataset from [this url](https://sliver07.grand-challenge.org/).

Convert MHD files to NIfTI. Rescale to 0-255.
```
usage: prepare_sliver07.py [-h] --in_dir IN_DIR --out_dir OUT_DIR

Required Arguments:
  --in_dir IN_DIR    Path to folder containing original MHD files.
  --out_dir OUT_DIR  Path to folder to put processed NIfTIs into.
```

## MSD - Brain Tumors

Download dataset from [this url](drive.google.com/drive/folders/1HqEgzS8BV2c7xYNrZdEAnrHk7osJJ--2).

Convert images to 2D slices. Only keep slices with at least 15% of the pixels being non-zero. Rescale images slice-wise to be in the range [0,255]. Pad images with zeros to be of shape (256, 256). 
```
usage: prepare_MSDbt.py [-h] --in_dir IN_DIR --out_dir OUT_DIR

Required Arguments:
  --in_dir IN_DIR    Path to folder containing original 3D NIfTIs.
  --out_dir OUT_DIR  Path to folder to put processed 2D NIfTi slices into.
```

## ACDC

Download dataset from [this url](creatis.insa-lyon.fr/Challenge/acdc/databases.html).

Convert 4D to 2D NIfTI files. Pad each image so that it is square. Resize the image to be of shape (256, 256). Rescale the image to be in the range [0, 255].
```
usage: prepare_ACDC.py [-h] --in_dir IN_DIR --out_dir OUT_DIR

Required Arguments:
  --in_dir IN_DIR    Path to folder containing original 4D NIfTIs.
  --out_dir OUT_DIR  Path to folder to put processed 2D NIfTi slices into.
```

# Statistical Tests

Running the statistical tests in the paper requires a csv file with observations. 

```
usage: statistical_tests.py [-h] --test TEST [--csv CSV] [--num_col NUM_COL] [--split SPLIT] [--alternative ALTERNATIVE] [--segments [SEGMENTS ...]]

Required Arguments:
  --test TEST           Which test to use. Two-sample Kolmogorov-Smirnov test, paired t test, independent t test, or Pearson correlation. Options: {'KS','Pair', 'Ind_T', 'Pearson'}.
  --csv CSV             Path to the csv file containing the observations.
  --num_col NUM_COL     Name of column containing information to compare.
  --split SPLIT         Column to split the data on.

Optional Arguments:
  --alternative ALTERNATIVE
                        Defines null and alternate hypotheses. Options: {'two-sided','less','greater'}. Default: 'two-sided'
  --segments [SEGMENTS ...]
                        Space separated list of column names. Perform the test separately for unique values in each column.
```

For example, if I had a csv file named `frechet_distances.csv` with columns 'Dataset', 'Augmentation', 'Backbone', 'Distance', I could compute the Pearson correlation between the Fréchet distances calculated using various backbone architectures by:
```
python statistical_tests.py --test Pearson \
                            --csv frechet_distances.csv \
                            --num_col Distance \
                            --split Backbone
```

Furthermore, I could compute the correlation by dataset with
```
python statistical_tests.py --test Pearson \
                            --csv frechet_distances.csv \
                            --num_col Distance \
                            --split Backbone \
                            --segments Dataset
```

# Split dataset

We provide the functionality to randomly split a dataset in half so that the Fréchet distance between the two halfs may be calculated.
```
usage: split_datasets.py [-h] --in_dir IN_DIR --out_dir1 OUT_DIR1 --out_dir2 OUT_DIR2

Required Arguments:
  --in_dir IN_DIR      Path to folder containing dataset to split.
  --out_dir1 OUT_DIR1  Path to folder to put first half of the dataset into.
  --out_dir2 OUT_DIR2  Path to folder to put second half of the dataset into.
```
