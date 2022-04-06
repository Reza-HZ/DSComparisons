import numpy as np

dataname = input('Enter Dataset Name:')
num_of_mats = int(input('Enter Number of Matrices:'))
dataset_int_mat_file = dataname + '_admat_dgc.txt'
data = open(dataset_int_mat_file, "r").readlines()
drugs = data[0].strip().split('\t')
drugsl = len(drugs)
for i in range(num_of_mats+1):
    output_fnmae = str(i) + dataname + '_simmat_dc.txt'
    fn = open(output_fnmae, "w")
    fn.write('\t')
    str_data = '\t'.join(dr for dr in drugs)
    fn.write(str_data)
    fn.write('\n')
    if (i==0):
        tempmat = np.ones((drugsl,drugsl))
    else:
        tempmat = np.random.rand(drugsl,drugsl)
        tempmat=np.around(tempmat,decimals=6)
        tempmat = (tempmat + tempmat.T)/2
        tempmat[np.diag_indices_from(tempmat)] = 1
    for j in range(drugsl):
        fn.write(drugs[j] + '\t')
        str_data = '\t'.join(str(entryf) for entryf in tempmat[j])
        fn.write(str_data)
        fn.write('\n')
    fn.close()
