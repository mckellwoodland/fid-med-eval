# Feature Extraction for Generative Medical Imaging Evaluation: New Evidence Against an Evolving Trend - Official Repository

<p><img src="https://github.com/mckellwoodland/fid-med-eval/blob/main/figures/figure1.png"
</p>

**Feature Extraction for Generative Medical Imaging Evaluation: New Evidence Against an Evolving Trend**

M. Woodland, A. Castelo, M. Al Taie, J. Albuquerque Marques Silva, M. Eltaher, F. Mohn, A. Shieh, S. Kundu, J.P. Yung, A.B. Patel, & K.K. Brock

Abstract: *Fréchet Inception Distance (FID) is a widely used metric for assessing synthetic image quality. It relies on an ImageNet-based feature extractor, making its applicability to medical imaging unclear. A recent trend is to adapt FID to medical imaging through feature extractors trained on medical images. Our study challenges this practice by demonstrating that ImageNet-based extractors are more consistent and aligned with human judgment than their RadImageNet counterparts. We evaluated sixteen StyleGAN2 networks across four medical imaging modalities and four data augmentation techniques with Fréchet distances (FDs) computed using eleven ImageNet or RadImageNet-trained feature extractors. Comparison with human judgment via visual Turing tests revealed that ImageNet-based extractors produced rankings consistent with human judgment, with the FD derived from the ImageNet-trained SwAV extractor significantly correlating with expert evaluations. In contrast, RadImageNet-based rankings were volatile and inconsistent with human judgment. Our findings challenge prevailing assumptions, providing novel evidence that medical image-trained feature extractors do not inherently improve FDs and can even compromise their reliability.*

The article was published in [MICCAI 2024](https://doi.org/10.1007/978-3-031-72390-2_9). The preprint is available at [arXiv](https://arxiv.org/abs/2311.13717).

# Training generative models

Preprocess all data using the files in `utils`.

Build the Docker container.
```
docker build --tag sg2ada:latest stylegan2-ada-pytorch/.
```

Train a StyleGAN2<sup>1</sup> model without augmentation.
```
stylegan2-ada-pytorch/docker_run.sh python stylegan2-ada-pytorch/train.py --outdir {OUT_DIR} \
                                                                          --gpus {GPUS} \
                                                                          --data {PROCESSED_DIR} \
                                                                          --cfg stylegan2 \
                                                                          --aug noaug \
                                                                          --gamma 8.2
```

Train a StyleGAN2 model with ADA<sup>2</sup>. For the MSD dataset, use `--augpipe bgcfn`.
```
stylegan2-ada-pytorch/docker_run.sh python stylegan2-ada-pytorch/train.py --outdir {OUT_DIR} \
                                                                          --gpus {GPUS} \
                                                                          --data {PROCESSED_DIR} \
                                                                          --cfg stylegan2 \
                                                                          --augpipe bgcfnc \
                                                                          --gamma 8.2
```

Train a StyleGAN2 model with APA<sup>3</sup>.
```
stylegan2-ada-pytorch/docker_run.sh python DeceiveD-main/train.py --outdir {OUT_DIR} \
                                                                  --gpus {GPUS} \
                                                                  --data {PROCESSED_DIR} \
                                                                  --cfg stylegan2 \
                                                                  --aug apa \
                                                                  --gamma 8.2
```

Train a StyleGAN2 model with DiffAugment<sup>4</sup>. For the MSD<sup>5</sup> dataset, use `--DiffAugment color,translation`.
```
stylegan2-ada-pytorch/docker_run.sh python data-efficient-gans-master/DiffAugment-stylegan2-pytorch/train.py --outdir {OUT_DIR} \
                                                                                                             --gpus {GPUS} \
                                                                                                             --data {PROCESSED_DIR} \
                                                                                                             --cfg stylegan2 \
                                                                                                             --aug noaug \
                                                                                                             --DiffAugment color,translation,cutout \
                                                                                                             --gamma 8.2
```

For training models on NIfTI or DICOM images, use the nifti branch of the forked repos.

# Evaluating generative models

Generate 50,000 images per model. Use the weights associated with 25k kimgs for the ChestX-ray14<sup>6</sup>, SLIVER07<sup>7</sup>, and ACDC<sup>8</sup> datasets (i.e. `network-snapshot-025000.pkl`) and 5k kimgs for the MSD dataset.
```
stylegan2-ada-pytorch/docker_run.sh python stylegan2-ada-pytorch/generate.py --network {MODEL_WEIGHTS} \
                                                                             --seeds 0-49999 \
                                                                             --outdir {OUT_DIR}
```

Calculate FDs with RadImageNet<sup>16</sup> models. You'll need to download the Tensorflow models [here](https://github.com/BMEII-AI/RadImageNet). Then you can extract the features. We extracted features for 50,000 generated images and the full datasets.
```
usage: extract_features.py [-h] -i IMG_DIR -f FEATURE_DIR [-a ARCHITECTURE] [-d DATASET]
                           [-m MODEL_DIR] [-g GPU_NODE] [-s IMG_SIZE] [-b BATCH_SIZE]

Required Arguments:
  -i IMG_DIR, --img_dir IMG_DIR
                        Specify the path to the folder that contains the images to be embedded within
                        a folder labeled class0.
  -f FEATURE_DIR, --feature_dir FEATURE_DIR
                        Specify the path to the folder where the features should be saved. This folder
                        will be further subdivided by feature extraction architecture and dataset
                        automatically.

Optional Arguments:
  -a ARCHITECTURE, --architecture ARCHITECTURE
                        Specify which feature extraction architecture to use. Options: "IRV2",
                        "ResNet50", "DenseNet121", "InceptionV3". Defaults to "InceptionV3".
  -d DATASET, --dataset DATASET
                        Specify which dataset the feature extractor should be trained on. Options:
                        "RadImageNet", "ImageNet". Defaults to "ImageNet".
  -m MODEL_DIR, --model_dir MODEL_DIR
                        Specify the path to the folder that contains the RadImageNet-pretrained models
                        in TensorFlow. Required if the dataset to be evaluated is RadImageNet.
  -g GPU_NODE, --gpu_node GPU_NODE
                        Specify the GPU node. Defaults to 0.
  -s IMG_SIZE, --img_size IMG_SIZE
                        Specify the height/width of the images. Defaults to 512.
  -b BATCH_SIZE, --batch_size BATCH_SIZE
                        Specify the batch size for inference.
```

Once the features are extracted, you can calculate the FD.
```
usage: fd.py [-h] -f1 FEAT_DIR1 -f2 FEAT_DIR2

Required Arguments:
  -f1 FEAT_DIR1, --feat_dir1 FEAT_DIR1
                        Specify the path to the folder that contains the first group of
                        embeddings.
  -f2 FEAT_DIR2, --feat_dir2 FEAT_DIR2
                        Specify the path to the folder that contains the second group of
                        embeddings.
```

Evaluate the ImageNet Fréchet distances, precision, and recall<sup>9</sup> with the StudioGAN<sup>10</sup> fork. Possible backbones: `InceptionV3_tf`, `InceptionV3_torch`<sup>11</sup>, `ResNet50_torch`<sup>12</sup>, `SwAV_torch`<sup>13</sup>, `DINO_torch`<sup>14</sup>, `Swin-T_torch`<sup>15</sup>.

The StudioGAN docker container can be pulled by:
```
docker pull alex4727/experiment:pytorch113_cuda116
```

Note that to use the ResNet50 backbone, you'll need to use our 'fid_med_eval' branch of the StudioGAN fork.
```
python PyTorch-StudioGAN-master/src/evaluate.py -metrics fid prdc \
                                                --dset1 {GEN_DIR} \
                                                --dset2 {REAL_DIR} \
                                                --post_resizer clean \
                                                --eval_backbone {BACKBONE} \
                                                --out_path {LOG_PATH}
```

To get the relative Fréchet distance, divide by the Fréchet distance calculated on a random split of the real data. You may use the same commands as above to do so, except switch the `GEN_DIR` and `REAL_DIR` for the two halves of the dataset. Code for splitting a dataset into two folders is available in `utils`.
```
python split_datasets.py --in_dir {FULL_DIR} \
                         --out_dir1 {HALF1_OUT_DIR} \
                         --out_dir2 {HALF2_OUT_DIR}
```

The functionality to run all statistical tests is also available in `utils`. Possible tests (not case-sensitive): Kolgomorov-Smirnov `KS`, paired *t* test `Pair`, indepdent *t* test `Ind_T`, and the Pearson correlation `Pearson`.
```
python statistical_tests.py --test {TEST} \
                            --csv {RESULT_CSV} \
                            --num_col {COL_TO_COMPARE} \
                            --split {LABEL_COL}
```

# Model Weights

The StyleGAN2 weights from our paper are available on [Zenodo](https://zenodo.org/records/13730919). Each model is named as follows `stylegan-{AUG}-{KIMG}-{FID}.pkl` where `AUG` is the augmentation technique, `KIMG` is the KIMG that the model was saved at, and `FID` is the FID of the model.

# Additional Results

Individual participant results for each visual Turing test are available in the `additional_results` directory. The directory further contains a depiction of randomly generated images from each model. Finally, the directory contains Improved Precision<sup>9</sup> and Improved Recall<sup>9</sup> metrics calculated with various backbone architectures.

# Citation

If you have found our work useful, we would appreciate a citation of our paper.
```
@InProceedings{10.1007/978-3-031-72390-2_9,
  author="Woodland, McKell
    and Castelo, Austin
    and Al Taie, Mais
    and Albuquerque Marques Silva, Jessica
    and Eltaher, Mohamed
    and Mohn, Frank
    and Shieh, Alexander
    and Kundu, Suprateek
    and Yung, Joshua P.
    and Patel, Ankit B.
    and Brock, Kristy K.",
  editor="Linguraru, Marius George
    and Dou, Qi
    and Feragen, Aasa
    and Giannarou, Stamatia
    and Glocker, Ben
    and Lekadir, Karim
    and Schnabel, Julia A.",
  title="Feature Extraction for Generative Medical Imaging Evaluation: New Evidence Against an Evolving Trend",
  booktitle="Medical Image Computing and Computer Assisted Intervention -- MICCAI 2024",
  year="2024",
  publisher="Springer Nature Switzerland",
  address="Cham",
  pages="87--97",
  abstract="Fr{\'e}chet Inception Distance (FID) is a widely used metric for assessing synthetic image quality. It relies on an ImageNet-based feature extractor, making its applicability to medical imaging unclear. A recent trend is to adapt FID to medical imaging through feature extractors trained on medical images. Our study challenges this practice by demonstrating that ImageNet-based extractors are more consistent and aligned with human judgment than their RadImageNet counterparts. We evaluated sixteen StyleGAN2 networks across four medical imaging modalities and four data augmentation techniques with Fr{\'e}chet distances (FDs) computed using eleven ImageNet or RadImageNet-trained feature extractors. Comparison with human judgment via visual Turing tests revealed that ImageNet-based extractors produced rankings consistent with human judgment, with the FD derived from the ImageNet-trained SwAV extractor significantly correlating with expert evaluations. In contrast, RadImageNet-based rankings were volatile and inconsistent with human judgment. Our findings challenge prevailing assumptions, providing novel evidence that medical image-trained feature extractors do not inherently improve FDs and can even compromise their reliability. Our code is available at https://github.com/mckellwoodland/fid-med-eval.",
  isbn="978-3-031-72390-2"
}
```
# Acknowledgments

Research reported in this publication was supported in part by resources of the Image Guided Cancer Therapy Research Program at The University of Texas MD Anderson Cancer Center, a generous gift from the Apache Corporation, the National Institutes of Health/NCI under award number P30CA016672, and the Tumor Measurement Initiative through the MD Anderson Strategic Initiative Development Program (STRIDE). We thank the NIH Clinical Center for the ChestX-ray14 dataset, the StudioGAN authors<sup>10</sup> for their FD implementations, and the RadImageNet creators for providing models for public use.

# References
1. Tero Karras *et al.* Analyzing and improving the image quality of StyleGAN. In CVPR, IEEE, pages 8110-8119, 2020.
2. Tero Karras *et al.* Training generative adversarial networks with limited data. In *et al.* (eds) Adv Neural Inf Syst Process, Curran Associates, Inc., 33:12104-12114, 2020.
3. Liming Jiang *et al.* Deceive D: Adaptive Pseudo Augmentation for GAN training with limited data. In M. Ranzato *et al.* (eds) Adv Neural Inf Syst Process, Curran Associates, Inc., 34:21655-21667, 2021.
4. Shengyu Zhao *et al.* Differentiable augmentation for data-efficient GAN training. In H. Larochelle *et al.* (eds) Adv Neural Inf Syst Process, Curran Associates, Inc., 33:7559-7570, 2020.
5. Michela Antonelli *et al.* The Medical Segmentation Decathlon. Nat Commun, 13:e4128, 2022.
6. Xiaosong Wang *et al.* ChestX-ray8: Hospital-scale chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases. In CVPR, IEEE, pages 2097-2106, 2017.
7. Tobias Heimann *et al.* Comparison and evaluation of methods for liver segmentation from CT datasets. IEEE Trans Med Imaging, 28(8):1251-1265, 2009.
8. Olivier Bernard *et al.* Deep learning techniques for automatic MRI cardiac multi-structures segmentation and diagnosis: Is the problem solved? IEEE Trans Med Imaging, 37(11):2514-2525, 2018.
9. Tuomas Kynkäänniemi *et al.* Improved precision and recall metric for assessing generative models. In H. Wallach *et al.* (eds) Adv Neural Inf Process Syst, Curran Associates, Inc., 32:3927-3936,2019.
10. Minguk Kang *et al.* StudioGAN: A taxonomy and benchmark of GANs for image synthesis. TPAMI, 45(12):15725-15742.
11. Christian Szegedy *et al.* Going deeper with convolutions. In CVPR, IEEE, pages 1-9, 2015.
12. Kaiming He *et al.* Deep residual learning for image recognition. In CVPR, IEEE, pages 770-778, 2016.
13. Mathilde Caron *et al.* Unsupervised learning of visual features by contrasting cluster assignments. In H. Larochelle *et al.* (eds) Adv Neural Inf Process Syst, Curran Associates, Inc., 33:9912-9924, 2020.
14. Mathilde Caron *et al.* Emerging properties in self-supervised vision transformers. In CVPR, IEEE, pages 9650-9660.
15. Ze Liu *et al.* Swin transformer: Hierarchical vision transformer using shifted windows. In CVPR, IEEE, pages 10012-10022, 2021.
16. X. Mei *et al.* RadImageNet: An open radiologic deep learning research dataset for effective transfer learning. Radiol. Artif. Intell., vol. 4, no. 5, pp. e210315, Jul. 2022, doi: 10.1148/ryai.210315.
