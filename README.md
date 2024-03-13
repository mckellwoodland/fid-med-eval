# Feature Extraction for Generative Medical Imaging Evaluation: New Evidence Against an Evolving Trend - Official Repository

<p><img src="https://github.com/mckellwoodland/fid-med-eval/blob/main/figures/graphical_abstract.png"
</p>

**Feature Extraction for Generative Medical Imaging Evaluation: New Evidence Against an Evolving Trend**

M. Woodland, A. Castelo, M. Al Taie, J. Albuquerque Marques Silva, M. Eltaher, F. Mohn, A. Shieh, S. Kundu, J.P. Yung, A.B. Patel, & K.K. Brock

Abstract: *Fréchet Inception Distance (FID) is a widely used metric for assessing synthetic image quality. It relies on an ImageNet-based feature extractor, making its applicability to medical imaging unclear. A recent trend is to adapt FID to medical imaging through feature extractors trained on medical images. Our study challenges this practice by demonstrating that ImageNet-based extractors are more consistent and aligned with human judgment than their RadImageNet counterparts. We evaluated sixteen StyleGAN2 networks across four medical imaging modalities and four data augmentation techniques with Fréchet distances (FDs) computed using eleven ImageNet or RadImageNet-trained feature extractors. Comparison with human judgment via visual Turing tests revealed that ImageNet-based extractors produced rankings consistent with human judgment, with the FD derived from the ImageNet-trained SwAV extractor significantly correlating with expert evaluations. In contrast, RadImageNet-based rankings were volatile and inconsistent with human judgment. Our findings challenge prevailing assumptions, providing novel evidence that medical image-trained feature extractors do not inherently improve FDs and can even compromise their reliability.*

Article available on [arXiv](https://arxiv.org/abs/2311.13717).

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

Evaluate the RadFID.
```
python radfid-main/calc_radfid.py --image_size {IMG_SIZE} \
                                  --img_dir_gen {GEN_DIR} \
                                  --img_dir_real {REAL_DIR} \
                                  --batch_size {BATCH_SIZE} \
                                  --metric radfid \
                                  --out_path {LOG_PATH}
```

Evaluate the ImageNet Fréchet distances, precision, and recall<sup>9</sup> with the StudioGAN<sup>10</sup> fork. Possible backbones: `InceptionV3_tf`, `InceptionV3_torch`<sup>11</sup>, `ResNet50_torch`<sup>12</sup>, `SwAV_torch`<sup>13</sup>, `DINO_torch`<sup>14</sup>, `Swin-T_torch`<sup>15</sup>.

The StudioGAN docker container can be pulled by:
```
docker pull alex4727/experiment:pytorch113_cuda116
```

Note, to use the ResNet50 backbone, you'll need to use our 'fid_med_eval' branch of the StudioGAN fork.
```
python PyTorch-StudioGAN-master/src/evaluate.py --metrics fid prdc \
                                                --dset1 {GEN_DIR} \
                                                --dset2 {REAL_DIR} \
                                                --post_resizer clean \
                                                --eval_backbone {BACKBONE} \
                                                --out_path {LOG_PATH}
```

To get the relative Fréchet distance, divide by the Fréchet distance calculated on a random split of the real data. You may use the same commands as above to do so, except switch the `GEN_DIR` and `REAL_DIR` for the two halfs of the dataset. Code for splitting a datset into two folders in available in `utils`.
```
python split_datasets.py --in_dir {FULL_DIR} \
                         --out_dir1 {HALF1_OUT_DIR} \
                         --out_dir2 {HALF2_OUT_DIR}
```

Functionality to run all statistical tests is also available in `utils`. Possible tests (not case-sensitive): Kolgomorov-Smirnov `KS`, paired *t* test `Pair`, indepdent *t* test `Ind_T`, and the Pearson correlation `Pearson`.
```
python statistical_tests.py --test {TEST} \
                            --csv {RESULT_CSV} \
                            --num_col {COL_TO_COMPARE} \
                            --split {LABEL_COL}
```

# Citation

If you have found our work useful, we would appreciate a citation of our arXiv submission.
```
@misc{woodland2024_fid_med,
      title={Feature Extraction for Generative Medical Imaging Evaluation: New Evidence Against an Evolving Trend}, 
      author={McKell Woodland and Austin Castelo and Mais Al Taie and Jessica Albuquerque Marques Silva and Mohamed Eltaher and Frank Mohn and Alexander Shieh and Suprateek Kundu and Joshua P. Yung and Ankit B. Patel and Kristy K. Brock},
      year={2024},
      eprint={2311.13717},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

# Acknowledgments

Research reported in this publication was supported in part by resources of the Image Guided Cancer Therapy Research Program at The University of Texas MD Anderson Cancer Center, a generous gift from the Apache Corporation, the National Institutes of Health/NCI under award number P30CA016672, and the Tumor Measurement Initiative through the MD Anderson Strategic Initiative Development Program (STRIDE). We thank the NIH Clinical Center for the ChestX-ray14 dataset, and the StudioGAN authors\sup{10} for their FD implementations.

# Referenc
1. Tero Karras et al. Analyzing and improving the image quality of StyleGAN. In CVPR, IEEE, pages 8110-8119, 2020.
2. Tero Karras et al. Training generative adversarial networks with limited data. In H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin (eds) Adv Neural Inf Syst Process, Curran Associates, Inc., 33:12104-12114, 2020.
3. Liming Jiang, Bo Dai, Wayne Wu, and Chen Loy. Deceive D: Adaptive Pseudo Augmentation for GAN training with limited data. In M. Ranzato, A. Beygelzimer, Y. Dauphin, P. Liang, and J. Vaughan (eds) Adv Neural Inf Syst Process, Curran Associates, Inc., 34:21655-21667, 2021.
4. Shengyu Zhao, Zhijian Liu, Ji Lin, Jun-Yan Zhu, and Song Han. Differentiable augmentation for data-efficient GAN training. In H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin (eds) Adv Neural Inf Syst Process, Curran Associates, Inc., 33:7559-7570, 2020.
5. Michela Antonelli et al. The Medical Segmentation Decathlon. Nat Commun, 13:e4128, 2022.
6. Xiaosong Wang et al. ChestX-ray8: Hospital-scale chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases. In CVPR, IEEE, pages 2097-2106, 2017.
7. Tobias Heimann et al. Comparison and evaluation of methods for liver segmentation from CT datasets. IEEE Trans Med Imaging, 28(8):1251-1265, 2009.
8. Olivier Bernard et al. Deep learning techniques for automatic MRI cardiac multi-structures segmentation and diagnosis: Is the problem solved? IEEE Trans Med Imaging, 37(11):2514-2525, 2018.
9. Tuomas Kynkäänniemi, Tero Karras, Samuli Laine, Jaakko Lehtinen, and Timo Aila. Improved precision and recall metric for assessing generative models. In H. Wallach et al. (eds) Adv Neural Inf Process Syst, Curran Associates, Inc., 32:3927-3936,2019.
10. Minguk Kang, Joonghyuk Shin, and Jaesik Park. StudioGAN: A taxonomy and benchmark of GANs for image synthesis. TPAMI, 45(12):15725-15742.
11. Christian Szegedy et al. Going deeper with convolutions. In CVPR, IEEE, pages 1-9, 2015.
12. Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In CVPR, IEEE, pages 770-778, 2016.
13. Mathilde Caron et al. Unsupervised learning of visual features by contrasting cluster assignments. In H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin (eds) Adv Neural Inf Process Syst, Curran Associates, Inc., 33:9912-9924, 2020.
14. Mathilde Caron et al. Emerging properties in self-supervised vision transformers. In CVPR, IEEE, pages 9650-9660.
15. Ze Liu et al. Swin transformer: Hierarchical vision transformer using shifted windows. In CVPR, IEEE, pages 10012-10022, 2021.

