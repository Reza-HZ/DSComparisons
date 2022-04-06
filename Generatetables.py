import numpy as np


dataset_names =['nr', 'e', 'gpcr','ic']
method_names = ['nrlmf', 'blm', 'netlaprls', 'wnngip']
labels = ['All-onesSim', 'MeanRandoms', 'BestRandom', 'WorstRandom', 'CosinePF', 'DicePF', 'TanimotoPF', 'Simcomp']
for dataset_name in dataset_names:
    if dataset_name == 'e':
        real_dataname = 'Enzyme'
    elif dataset_name == 'nr':
        real_dataname = 'Nuclear Receptors'
    elif dataset_name == 'gpcr':
        real_dataname = 'GPCR'
    else:
        real_dataname = 'Ion Channels'
    fn = open('ResultsTable-' + real_dataname + '.txt', "w")
    fn.write('\t')
    str_data = '\t'.join(i for i in labels)
    fn.write(str_data)
    fn.write('\n')
    for method_name in method_names:
        auc = []
        aupr = []
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

        tempaucmat=np.around(aucvalues,decimals=6)
        fn.write(method_name + 'AUC\t')
        str_data = '\t'.join(str(i) for i in tempaucmat)
        fn.write(str_data)
        fn.write('\n')
        tempauprmat=np.around(auprvalues,decimals=6)
        fn.write(method_name + 'AUPR\t')
        str_data = '\t'.join(str(i) for i in tempauprmat)
        fn.write(str_data)
        fn.write('\n')
    fn.close()