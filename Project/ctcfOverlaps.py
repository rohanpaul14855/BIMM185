import csv
import pandas as pd
import seaborn as sns
import pickle
import matplotlib.pyplot as plt


# tadsig, nontadsig = [], []
# with open('data/bedfiles/HeLa.left.bed') as f:
#     reader = csv.reader(f, delimiter='\t')
#     next(reader)
#     with open('data/peakFiles/HeLa/wgEncodeBroadHistoneHelas3CtcfStdPk.broadPeak') as p:
#         peaks = list(csv.reader(p, delimiter='\t'))
#
#     outfile = 'data/HeLa_ctcf.left.features'
#     out = []
#     for line in reader:
#         chrom = line[0]
#         start = int(line[1])
#         stop = int(line[2])
#         r1 = set(range(start, stop + 1))
#         signals = []
#
#         for peak in peaks:
#             signal = float(peak[6])
#             chrom2 = peak[0]
#             start2 = int(peak[1])
#             stop2 = int(peak[1])
#             r2 = set(range(start2, stop2 + 1))
#             if chrom == chrom2:
#                 overlap = len(r1.intersection(r2)) > 0
#                 if overlap:
#                     signals.append(signal)
#                     tadsig.append(signal)
#                 elif not overlap:
#                     nontadsig.append(signal)
#
#         out.append([chrom, start, stop, sum(signals)])
#
#
#     with open(outfile, 'w') as f:
#         csv.writer(f, delimiter='\t').writerows(out)
#
# data = pd.DataFrame([[i, j] for i, j in zip(tadsig, nontadsig)], columns=['TAD regions', 'non TAD regions'])
#
# with open('data/pickle/signals.pickle', 'wb') as f:
#     pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


with open('data/pickle/signals.pickle', 'rb') as f:
    data = pickle.load(f)

from scipy.stats import ttest_ind as ttest

significance = ttest(data['TAD regions'], data['non TAD regions'])
print(significance.pvalue)
sns.boxplot(data, showfliers=False)
plt.ylabel('CTCF Peak Strength')
plt.title('CTCF binding strength comparison for TAD boundary vs. non-boundary regions')

plt.show()
