"""
All the statistical tests used in the paper.
"""

# Imports
import argparse
import pandas as pd
from scipy import stats

# Arguments
parser = argparse.ArgumentParser()
parser._action_groups.pop()
required = parser.add_argument_group('Required Arguments')
required.add_argument('--test', required=True, type=str, help="Which test to use. \
                                                              Two-sample Kolmogorov-Smirnov test, paired t test, independent t test, or Pearson correlation. \
                                                              Options: {'KS','Pair', 'Ind_T', 'Pearson'}.")
required.add_argument('--csv', type=str, help='Path to the csv file containing the observations.')
required.add_argument('--num_col', type=str, help='Name of column containing information to compare.')
required.add_argument('--split', type=str, help='Column to split the data on.')
optional = parser.add_argument_group('Optional Arguments')
optional.add_argument('--alternative', type=str, default='two-sided', help="Defines null and alternate hypotheses. \
                                                                             Options: {'two-sided','less','greater'}. \
                                                                             Default: 'two-sided'")
optional.add_argument('--segments', type=str, nargs='*', help='Space separated list of column names. \
                                                            Perform the test separately for unique values in each column.')
args = parser.parse_args()
test = args.test.lower()
alt = args.alternative
csv = args.csv
num_col = args.num_col
split = args.split
segs = args.segments
if segs is None:
    segs = []
if test not in ['ks', 'pair', 'pearson', 'ind_t']:
    raise ValueError(f"Please choose one of the following tests: {'KS', 'Pair', 'Ind_T','Pearson'}")
if alt not in ['two-sided','less','greater']:
    raise ValueError(f"Please choose one of the following alternatives: {'two-sided','less','greater'}")

# Functions
def calculate_statistic(df, split, num_col, segs, test, alt):
    if len(segs) == 0:
        labels = df[split].unique()
        for i in range(len(labels)):
            for j in range(i+1,len(labels)):
                print(f"Calculating for {labels[i]} and {labels[j]}")
                pop1 = df[df[split] == labels[i]][num_col]
                pop2 = df[df[split] == labels[j]][num_col]
                if test == 'ks':
                    print(stats.kstest(pop1, pop2, alternative=alt))
                elif test == 'pair':
                    print(stats.ttest_rel(pop1, pop2, alternative=alt))
                elif test == 'ind_t':
                    print(stats.ttest_ind(pop1, pop2, alternative=alt))
                elif test == 'pearson':
                    print(stats.pearsonr(pop1, pop2, alternative=alt))
    else:
        seg = segs[0]
        print(f'Segmenting data by col {seg}')
        values = df[seg].unique()
        for value in values:
            print(f"Looking at value {value}")
            calculate_statistic(df[df[seg]==value], split, num_col, segs[1:], test, alt)

# Main code
df = pd.read_csv(csv)
if not df[num_col].dtype == 'float64':
    df[num_col] = df[num_col].astype(float)
calculate_statistic(df, split, num_col, segs, test, alt)
