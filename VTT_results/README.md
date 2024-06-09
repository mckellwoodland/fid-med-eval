| Participant	| Aug	    | FPR [%] ↑	| FNR [%] ↑	| *t* test | Diff ↓	| KS test |
| ----------- | ---     | --------- | --------- | ------   | ------ | ------- |
| 1	          | None    | 70	      | 30	      | p>.999   | 0.2	  | p=.994  |
|             |	ADA	    | 40	      | 10	      | p=.018   | 0.0	  | p>.999  |
|             |	APA     | 30        |	20        |	p=.024   | 0.5    |	p=.168  |
|             |	DiffAug | 80	      | 20        |	p>.999   | 0.1    |	p>.999  |
2	None	60	30	p=.660	0.3	p=.994
	ADA	30	20	p=.024	0.6	p=.787
	APA	30	50	p=.039	0.2	p=.994
	DiffAug	40	40	p=.398	0.0	p<.001
3	None	30	70	p>.999	0.1	p=.994
	ADA	20	60	p=.355	0.4	p=.994
	APA	50	60	p=.673	0.2	p=.994
	DiffAug	20	100	p=.151	-0.5	p>.999
4	None	40	70	p=.660	0.2	p=.994
	ADA	40	60	p>.999	0.4	p=.787
	APA	30	70	p>.999	0.2	p=.994
	DiffAug	80	60	p=.074	-0.4	p=0.012
5	None	40	90	p=.134	-0.2	p=.994
	ADA	30	80	p=.628	0.0	p>.999
	APA	30	80	p=.628	0.1	p>.999
	DiffAug	20	70	p=.628	0.0	p=.994
Table S1: Visual Turing test results for individual participants for the ChestXray-14 dataset. Precision (Pre), recall (Rec), accuracy (Acc), false positive rate (FPR), and false negative rate (FNR) are shown. FPRs near 50% indicate random guessing on generated images. The p values generated from the t test, representing the likelihood that a participant will guess ‘real’ whether or not the image was real, are also presented. The difference between mean Likert scores for real and generated images (Diff) is also shown; Diff represents the perceived difference in image realism between real and generated images (where a negative value signifies perceiving generated images as more realistic than real images). Finally, the p values generated from the Kolmogorov-Smirnov (KS) tests, representing the likelihood that Likert scores for real and generated images are drawn from the same distribution, are presented. 
↑ and ↓ signify whether a higher or lower value is better. 
Boldface denotes the best performance per dataset.
Gray boxes demonstrate instances in which we fail to reject the null hypothesis, suggesting random guessing. 
Red denotes decreased performance from that augmentation method (Aug) compared with no augmentation (None): adaptive discriminator augmentation (ADA), adaptive pseudo augmentation (APA), or differentiable augmentation (DiffAug).

<table>
  <tr>
    <td rowspan="2">This cell spans 2 rows</td>
    <td>This is row 1, column 2</td>
  </tr>
  <tr>
    <td>This is row 2, column 2</td>
  </tr>
</table>
