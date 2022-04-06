
import os
import time
import cv_eval
from functions import *
from nrlmf import NRLMF
from netlaprls import NetLapRLS
from blm import BLMNII
from wnngip import WNNGIP

method = input('Enter method (wnngip,nrlmf,netlaprls,blmnii): ')
dataset = input('Enter dataset (nr,ic,e,gpcr): ')
dd_data = input('Enter drug-drug similarity data name (ex: nr, ic, e, gpcr, Cosine_e, Tanimoto_gpcr, Dice_nr, allones_ic, 95e, ...): ')
data_dir = input('Enter data directory (ex: F:/PythonCodes/DTI/datasets):  ')
output_dir = input('Enter output directory (ex: F:/PythonCodes/DTI/outputs/):  ')
sp_arg = int(input('Enter specify-arg (0 for optimal arguments, 1 for default arguments): '))
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

seeds = [7771, 8367, 22, 1812, 4659]
# seeds = np.random.choice(10000, 5, replace=False)

# default parameters for each methods
if method == 'nrlmf':
    args = {'c': 5, 'K1': 5, 'K2': 5, 'r': 50, 'lambda_d': 0.125, 'lambda_t': 0.125, 'alpha': 0.25, 'beta': 0.125, 'theta': 0.5, 'max_iter': 100}
if method == 'netlaprls':
    args = {'gamma_d': 10, 'gamma_t': 10, 'beta_d': 1e-5, 'beta_t': 1e-5}
if method == 'blmnii':
    args = {'alpha': 0.7, 'gamma': 1.0, 'sigma': 1.0, 'avg': False}
if method == 'wnngip':
    args = {'T': 0.8, 'sigma': 1.0, 'alpha': 0.8}

intMat, drugMat, targetMat, drug_names, target_names = load_data_from_file(dataset, dd_data, data_dir)
X, D, T = intMat, drugMat, targetMat
cv_data = cross_validation(X, seeds)
if sp_arg == 0:
    if method == 'nrlmf':
        cv_eval.nrlmf_cv_eval(method, dataset, cv_data, X, D, T, args)
    if method == 'netlaprls':
        cv_eval.netlaprls_cv_eval(method, dataset, cv_data, X, D, T, args)
    if method == 'blmnii':
        cv_eval.blmnii_cv_eval(method, dataset, cv_data, X, D, T, args)
    if method == 'wnngip':
        cv_eval.wnngip_cv_eval(method, dataset, cv_data, X, D, T, args)
elif sp_arg == 1:
    tic = time.process_time()
    if method == 'nrlmf':
        model = NRLMF(cfix=args['c'], K1=args['K1'], K2=args['K2'], num_factors=args['r'], lambda_d=args['lambda_d'], lambda_t=args['lambda_t'], alpha=args['alpha'], beta=args['beta'], theta=args['theta'], max_iter=args['max_iter'])
    if method == 'netlaprls':
        model = NetLapRLS(gamma_d=args['gamma_d'], gamma_t=args['gamma_t'], beta_d=args['beta_t'], beta_t=args['beta_t'])
    if method == 'blmnii':
        model = BLMNII(alpha=args['alpha'], gamma=args['gamma'], sigma=args['sigma'], avg=args['avg'])
    if method == 'wnngip':
        model = WNNGIP(T=args['T'], sigma=args['sigma'], alpha=args['alpha'])
    cmd = str(model)
    print("Dataset:"+dataset+"\n"+cmd)
    aupr_vec, auc_vec = train(model, cv_data, X, D, T)
    aupr_avg, aupr_conf = mean_confidence_interval(aupr_vec)
    auc_avg, auc_conf = mean_confidence_interval(auc_vec)
    print("auc:%.6f, aupr: %.6f, auc_conf:%.6f, aupr_conf:%.6f, Time:%.6f" % (auc_avg, aupr_avg, auc_conf, aupr_conf, time.process_time()-tic))
    write_metric_vector_to_file(auc_vec, os.path.join(output_dir, method+"_auc_cvs"+"_"+dataset+".txt"))
    write_metric_vector_to_file(aupr_vec, os.path.join(output_dir, method+"_aupr_cvs"+"_"+dataset+".txt"))
else:
    print('sp_arg is not valid!')
