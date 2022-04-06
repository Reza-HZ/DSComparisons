from functions import *
from nrlmf import NRLMF
from netlaprls import NetLapRLS
from blm import BLMNII
from wnngip import WNNGIP


data_dir = 'F:/PythonCodes/PyDTI-master/datasets/'
output_dir = 'F:/PythonCodes/PyDTI-master/ComparisonResults/'
method = input('Enter method name (nrlmf, netlaprls, blm, wnngip):')
datasetname = input('Enter dataset name (nr, e, gpce, ic):')
intMat, targetMat, drug_names, target_names = load_data_for_comparison_withoutdd(datasetname, data_dir)
seeds = [7771, 8367, 22, 1812, 4659]
X, T = intMat, targetMat
cv_data = cross_validation(X, seeds)

if method == 'nrlmf':
    args = {'c': 5, 'K1': 5, 'K2': 5, 'r': 50, 'lambda_d': 0.125, 'lambda_t': 0.125, 'alpha': 0.25, 'beta': 0.125, 'theta': 0.5, 'max_iter': 100}
if method == 'netlaprls':
    args = {'gamma_d': 10, 'gamma_t': 10, 'beta_d': 1e-5, 'beta_t': 1e-5}
if method == 'blm':
    args = {'alpha': 0.7, 'gamma': 1.0, 'sigma': 1.0, 'avg': False}
if method == 'wnngip':
    args = {'T': 0.8, 'sigma': 1.0, 'alpha': 0.8}
if method == 'kbmf':
    args = {'R': 50}
if method == 'cmf':
    args = {'K': 50, 'lambda_l': 0.5, 'lambda_d': 0.125, 'lambda_t': 0.125, 'max_iter': 30}

output_fname = output_dir + method + '-' + datasetname + '.txt'
fn = open(output_fname, "w")
for i in range(105):
    if (i==101):
        dddataset = 'Cosine_' + datasetname + '_simmat_dc.txt'
    elif (i==102):
        dddataset = 'Dice_' + datasetname + '_simmat_dc.txt'
    elif (i==103):
        dddataset = 'Tanimoto_' + datasetname + '_simmat_dc.txt'
    elif (i==104):
        dddataset = datasetname + '_simmat_dc.txt'
    else:
        dddataset = str(i) + datasetname + '_simmat_dc.txt'
    drugMat = load_data_for_comparison_onlydd(dddataset, data_dir)
    D = drugMat

    if method == 'nrlmf':
        model = NRLMF(cfix=args['c'], K1=args['K1'], K2=args['K2'], num_factors=args['r'], lambda_d=args['lambda_d'], lambda_t=args['lambda_t'], alpha=args['alpha'], beta=args['beta'], theta=args['theta'], max_iter=args['max_iter'])
    if method == 'netlaprls':
        model = NetLapRLS(gamma_d=args['gamma_d'], gamma_t=args['gamma_t'], beta_d=args['beta_t'], beta_t=args['beta_t'])
    if method == 'blm':
        model = BLMNII(alpha=args['alpha'], gamma=args['gamma'], sigma=args['sigma'], avg=args['avg'])
    if method == 'wnngip':
        model = WNNGIP(T=args['T'], sigma=args['sigma'], alpha=args['alpha'])

    aupr_vec, auc_vec = train(model, cv_data, X, D, T)
    aupr_avg, aupr_conf = mean_confidence_interval(aupr_vec)
    auc_avg, auc_conf = mean_confidence_interval(auc_vec)
    fn.write(str(i)+ '\t' +str(auc_avg)+ '\t' + str(aupr_avg) + '\n')
    print(i)
fn.close()
