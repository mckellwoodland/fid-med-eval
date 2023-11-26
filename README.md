# Importance of Feature Extraction in the Calculation of Fréchet Distance Calculation for Medical Imaging - Official Repository

<p><img src="https://github.com/mckellwoodland/fid-med-eval/blob/main/figures/graphical_abstract.png"
</p>

**Importance of Feature Extraction in the Calculation of Fréchet Distance Calculation for Medical Imaging**
M. Woodland, M. Al Taie, J. Albuquerque Marques Silva, M. Eltaher, F. Mohn, A. Shieh, A. Castelo, S. Kundu, J.P. Yung, A.B. Patel, & K.K. Brock

Abstract: *Fréchet Inception Distance is a widely used metric for evaluating synthetic image quality that utilizes an ImageNet-trained InceptionV3 network as a feature extractor. However, its application in medical imaging lacks a standard feature extractor, leading to biased and inconsistent comparisons. This study aimed to compare state-of-the-art feature extractors for computing Fréchet Distances (FDs) in medical imaging. A StyleGAN2 network was trained with data augmentation techniques tailored for limited data domains on datasets comprising three medical imaging modalities and four anatomical locations. Human evaluation of generative quality (via a visual Turing test) was compared to FDs calculated using ImageNet-trained InceptionV3, ResNet50, SwAV, DINO, and Swin Transformer architectures, in addition to an InceptionV3 network trained on a large medical dataset, RadImageNet. All ImageNet-based extractors were consistent with each other, but only SwAV was significantly correlated with medical expert judgment. The RadImageNet-based FD showed volatility and lacked correlation with human judgment. Caution is advised when using medical image-trained extraction networks in the FD calculation. These networks should be rigorously evaluated on the imaging modality under consideration and publicly released. ImageNet-based extractors, while imperfect, are consistent and widely understood. Training extraction networks with SwAV is a promising approach for synthetic medical image evaluation.*

Article available on arXiv.
