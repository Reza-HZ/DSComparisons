import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

auc = []
aupr = []
dataset_name = input('Enter dataset name: ')
method_name = input('Enter method name: ')
datasetfilename = method_name + '-' + dataset_name + '.txt'
data = open(datasetfilename, "r").readlines()
for line in data:
    templist = line.split('\t')
    auc.append(templist[1])
    aupr.append(templist[2])
auc = np.array(auc).astype(np.float32)
aupr = np.array(aupr).astype(np.float32)
aucvalues = np.zeros(8)
auprvalues = np.zeros(8)
tempauc = auc[1:101]
tempaupr = aupr[1:101]
aucvalues[0] = auc[0]
aucvalues[4:8] = auc[101:105]
aucvalues[1] = np.mean(tempauc)
aucvalues[2] = max(tempauc)
aucvalues[3] = min(tempauc)
auprvalues[0] = aupr[0]
auprvalues[4:8] = aupr[101:105]
auprvalues[1] = np.mean(tempaupr)
auprvalues[2] = max(tempaupr)
auprvalues[3] = min(tempaupr)

if dataset_name == 'e':
    real_dataname = 'Enzyme'
elif dataset_name == 'nr':
    real_dataname = 'Nuclear Receptors'
elif dataset_name == 'gpcr':
    real_dataname = 'GPCR'
else:
    real_dataname = 'Ion Channels'

if method_name == 'nrlmf':
    real_methodname = 'NRLMF'
elif method_name == 'blm':
    real_methodname = 'BLM-NII'
elif method_name == 'netlaprls':
    real_methodname = 'NetLapRLS'
else:
    real_methodname = 'WNN-GIP'


labels = ['All-onesSim', 'MeanRandoms', 'BestRandom', 'WorstRandom', 'CosinePF', 'DicePF', 'TanimotoPF', 'Simcomp']
x = np.arange(len(labels))  # the label locations
width = 0.38  # the width of the bars

auccolor = ['blue' if i == max(aucvalues) else 'skyblue' for i in aucvalues]
auprcolor = ['red' if i == max(auprvalues) else 'orange' for i in auprvalues]

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, aucvalues, width, color = auccolor)
rects2 = ax.bar(x + width/2, auprvalues, width, color = auprcolor)

red_patch = mpatches.Patch(color='red', label='AUPR_Max')
orange_patch = mpatches.Patch(color='orange', label='AUPR')
blue_patch = mpatches.Patch(color='blue', label='AUC_Max')
skyblue_patch = mpatches.Patch(color='skyblue', label='AUC')

plt.legend(handles=[red_patch, orange_patch, blue_patch, skyblue_patch], ncol = 4, fontsize=6.5)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Similarity Matrices')
ax.set_title(real_methodname + ' method and ' + real_dataname + ' dataset', fontsize= 9)
ylim_min = 0 if min(min(auprvalues),min(aucvalues))-0.12<0 else min(min(auprvalues),min(aucvalues))-0.12
ax.set_ylim(ylim_min,1.14)
ax.set_xticks(x, labels, fontsize= 6)

ax.bar_label(rects1, padding=0.02, fontsize= 6, rotation = 'vertical', fontname='Bemio')
ax.bar_label(rects2, padding=0.02, fontsize= 6, rotation = 'vertical', fontname='Bemio')
fig.tight_layout()
plt.show()