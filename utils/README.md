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
