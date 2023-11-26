# Importance of Feature Extraction in the Calculation of Fréchet Distance Calculation for Medical Imaging - Official Repository

<p><img src="https://github.com/mckellwoodland/fid-med-eval/blob/main/figures/graphical_abstract.png"
</p>

**Importance of Feature Extraction in the Calculation of Fréchet Distance Calculation for Medical Imaging**
M. Woodland, M. Al Taie, J. Albuquerque Marques Silva, M. Eltaher, F. Mohn, A. Shieh, A. Castelo, S. Kundu, J.P. Yung, A.B. Patel, & K.K. Brock

Abstract: *Fréchet Inception Distance is a widely used metric for evaluating synthetic image quality that utilizes an ImageNet-trained InceptionV3 network as a feature extractor. However, its application in medical imaging lacks a standard feature extractor, leading to biased and inconsistent comparisons. This study aimed to compare state-of-the-art feature extractors for computing Fréchet Distances (FDs) in medical imaging. A StyleGAN2 network was trained with data augmentation techniques tailored for limited data domains on datasets comprising three medical imaging modalities and four anatomical locations. Human evaluation of generative quality (via a visual Turing test) was compared to FDs calculated using ImageNet-trained InceptionV3, ResNet50, SwAV, DINO, and Swin Transformer architectures, in addition to an InceptionV3 network trained on a large medical dataset, RadImageNet. All ImageNet-based extractors were consistent with each other, but only SwAV was significantly correlated with medical expert judgment. The RadImageNet-based FD showed volatility and lacked correlation with human judgment. Caution is advised when using medical image-trained extraction networks in the FD calculation. These networks should be rigorously evaluated on the imaging modality under consideration and publicly released. ImageNet-based extractors, while imperfect, are consistent and widely understood. Training extraction networks with SwAV is a promising approach for synthetic medical image evaluation.*

Article available on arXiv.

# Training generative models

Preprocess all data using the files in `utils`.

Train a StyleGAN2 model without augmentation.
```
python stylegan2-ada-pytorch/train.py --outdir {OUT_DIR} \
                                      --gpus {GPUS} \
                                      --data {PROCESSED_DIR} \
                                      --cfg stylegan2 \
                                      --aug noaug \
                                      --gamma 8.2
```

Train a StyleGAN2 model with ADA. For the MSD dataset, use `--augpipe bgcfn`.
```
python stylegan2-ada-pytorch/train.py --outdir {OUT_DIR} \
                                      --gpus {GPUS} \
                                      --data {PROCESSED_DIR} \
                                      --cfg stylegan2 \
                                      --augpipe bgcfnc \
                                      --gamma 8.2
```

Train a StyleGAN2 model with APA.
```
python DeceiveD-main/train.py --outdir {OUT_DIR} \
                              --gpus {GPUS} \
                              --data {PROCESSED_DIR} \
                              --cfg stylegan2 \
                              --aug apa \
                              --gamma 8.2
```

Train a StyleGAN2 model with DiffAugment. For the MSD dataset, use `--DiffAugment color,translation`.
```
python data-efficient-gans-master/DiffAugment-stylegan2-pytorch/train.py --outdir {OUT_DIR} \
                                                                         --gpus {GPUS} \
                                                                         --data {PROCESSED_DIR} \
                                                                         --cfg stylegan2 \
                                                                         --aug noaug \
                                                                         --DiffAugment color,translation,cutout \
                                                                         --gamma 8.2
```

# Evaluating generative models

Generate 50,000 images per model. Use the weights associated with 25k kimgs for the ChestX-ray14, SLIVER07, and ACDC datasets (i.e. `network-snapshot-025000.pkl`) and 5k kimgs for the MSD dataset.
```
python stylegan2-ada-pytorch/generate.py --network {MODEL_WEIGHTS} \
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

Evaluate the ImageNet Fréchet distances, precision, and recall with the StudioGAN fork. Possible backbones: `InceptionV3_tf`, `InceptionV3_torch`, `ResNet50_torch`, `SwAV_torch`, `DINO_torch`, `Swin-T_torch`.
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
