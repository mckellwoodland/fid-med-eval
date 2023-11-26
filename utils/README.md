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

## MSD - Brain Tumor

Converts to 2D slices. Only keeps slices with at least 15% of the pixels being non-zero. Rescales images slice-wise to be in the range [0,255]. Pads images with zeros to be of shape (256, 256). 
```
python preprocessMSD.py --in_dir {RAW_DIR} --out_dir {PROCESSED_DIR}
```

## ACDC
