
import os
import numpy as np
from collections import defaultdict

def load_data_from_file(dataset, dddataset, folder):
    targets = []
    intlist = []
    ddlist = []
    ttlist = []
    inputdataset = folder + dataset + '_admat_dgc.txt'
    input_dd_dataset = folder + dddataset + '_simmat_dc.txt'
    input_tt_dataset = folder + dataset + '_simmat_dg.txt'
    data = open(inputdataset, "r").readlines()
    dd_data = open(input_dd_dataset, "r").readlines()
    tt_data = open(input_tt_dataset, "r").readlines()
    drugs = data[0].strip().split('\t')
    for line in data:
        targets.append(line.split('\t')[0])
        intlist.append(line.split('\t')[1:])
    targets.pop(0)
    intlist.pop(0)
    for line in dd_data:
        ddlist.append(line.split('\t')[1:])
    for line in tt_data:
        ttlist.append(line.split('\t')[1:])
    ddlist.pop(0)
    ttlist.pop(0)
    intMat = np.array(intlist, dtype=np.float64).T    # drug-target interaction matrix
    drugMat = np.array(ddlist, dtype=np.float64)      # drug similarity matrix
    targetMat = np.array(ttlist, dtype=np.float64)    # target similarity matrix
    return intMat, drugMat, targetMat, drugs, targets


def load_data_for_comparison_withoutdd(dataset, folder):
    targets = []
    intlist = []
    ttlist = []
    inputdataset = folder + dataset + '_admat_dgc.txt'
    input_tt_dataset = folder + dataset + '_simmat_dg.txt'
    data = open(inputdataset, "r").readlines()
    tt_data = open(input_tt_dataset, "r").readlines()
    drugs = data[0].strip().split('\t')
    for line in data:
        targets.append(line.split('\t')[0])
        intlist.append(line.split('\t')[1:])
    targets.pop(0)
    intlist.pop(0)
    for line in tt_data:
        ttlist.append(line.split('\t')[1:])
    ttlist.pop(0)
    intMat = np.array(intlist, dtype=np.float64).T    # drug-target interaction matrix
    targetMat = np.array(ttlist, dtype=np.float64)    # target similarity matrix
    return intMat, targetMat, drugs, targets

def load_data_for_comparison_onlydd(dddataset, folder):
    ddlist = []
    input_dd_dataset = folder + dddataset
    dd_data = open(input_dd_dataset, "r").readlines()
    for line in dd_data:
        ddlist.append(line.split('\t')[1:])
    ddlist.pop(0)
    drugMat = np.array(ddlist, dtype=np.float64)      # drug similarity matrix
    return drugMat

def cross_validation(intMat, seeds, num=10):
    cv_data = defaultdict(list)
    for seed in seeds:
        num_drugs, num_targets = intMat.shape
        prng = np.random.RandomState(seed)
        index = prng.permutation(intMat.size)
        step = index.size//num
        for i in range(num):
            if i < num-1:
                ii = index[i*step:(i+1)*step]
            else:
                ii = index[i*step:]
            test_data = np.array([[k/num_targets, k % num_targets] for k in ii], dtype=np.int32)
            x, y = test_data[:, 0], test_data[:, 1]
            test_label = intMat[x, y]
            W = np.ones(intMat.shape)
            W[x, y] = 0
            cv_data[seed].append((W, test_data, test_label))
    return cv_data


def train(model, cv_data, intMat, drugMat, targetMat):
    aupr, auc = [], []
    for seed in list(cv_data.keys()):
        for W, test_data, test_label in cv_data[seed]:
            model.fix_model(W, intMat, drugMat, targetMat, seed)
            aupr_val, auc_val = model.evaluation(test_data, test_label)
            aupr.append(aupr_val)
            auc.append(auc_val)
    return np.array(aupr, dtype=np.float64), np.array(auc, dtype=np.float64)


def svd_init(M, num_factors):
    from scipy.linalg import svd
    U, s, V = svd(M, full_matrices=False)
    ii = np.argsort(s)[::-1][:num_factors]
    s1 = np.sqrt(np.diag(s[ii]))
    U0, V0 = U[:, ii].dot(s1), s1.dot(V[ii, :])
    return U0, V0.T


def mean_confidence_interval(data, confidence=0.95):
    import scipy as sp
    import scipy.stats
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, h


def write_metric_vector_to_file(auc_vec, file_name):
    np.savetxt(file_name, auc_vec, fmt='%.6f')


def load_metric_vector(file_name):
    return np.loadtxt(file_name, dtype=np.float64)
