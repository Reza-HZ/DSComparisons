# PyDTI-simplified -- a Python3 library for predicting drug-target interactions, and comparing different drug-drug similarities.  

Apr 06 2022

This package has been updated by Reza Hassanzadeh and Soheila Shabani-Mashcool. 
For any questions, please feel free to contact the authors:
r.hassanzadeh@uma.ac.ir
soheila.shabani@ut.ac.ir


The initial version of this package was implemented by Yong Liu in Pyhton2.
The specifications of the owner of the original version are as follows:
Yong Liu
Email: liuy0054@e.ntu.edu.sg
School of Computer Engineering, Nanyang Technological University, Singapore
Joint NTU-UBC Research Centre of Excellence in Active Living for Elderly (LILY), Nanyang Technological University, Singapore
https://github.com/stephenliu0423/PyDTI
-----------------------------------------------------------------------------------
Datasets:
Datasets are available at https://drive.google.com/file/d/1OfXU2QZhjb_TP8GdxZT3otDjGQQA0JZr/view?usp=sharing.
The dataset folder contains all the information about the four gold standard datasets:
nr (Nuclear Receptors), e(Enzymes), gpcr(G-Protein Coupled Receptors) and ic(Ion Channels). 
For example, the interaction matrices of e and nr datasets are stored as e_admat_dgc.txt and 
nr_admat_dgc.txt respectively. The target-target similarity matrices of gpcr and ic datasets 
are stored as gpcr_simmat_dg.txt and ic_simmat_dg.txt respectively.

For each dataset, in addition to the default drug-drug similarity matrix obtained by SIMCOMP (for 
example, gpcr_simmat_dc.txt is the default drug-drug similarity matrix obtained by SIMCOMP), there 
are 104 other matrices including:
	-One hundred random drug-drug similarity matrices marked with numbers from 1 to 100. For 
	example, the 78th random drug-drug similarity matrix for the gpcr dataset is denoted by 78gpcr_simmat_dc.txt. 
	-One drug-drug similarity matrix where every element is equal to one. For example, allones_e_simmat_dc.txt is 
	the all-one drug-drug similarity matrix for enzyme dataset.  
	-Three matrices calculated from PubChem fingerprint using Tanimoto coefficient, Dice coefficient and Cosine 
	similarity. For example, Dice_nr_simmat_dc.txt is the drug-drug similarity matrix obtained by Dice coefficient 
	for Nuclear Receptors dataset.
---------------------------------------------------------------------------------------
Running:

To get the results of different methods, please run PyDTI_simplified.py.
After running the PyDTI_simplified.py:
	-The method must be selected from the algorithms wnngip, nrlmf, netlaprls or blmnii.
	-The dataset must be selected from the nr, ic, e or gpcr.
	-To enter any drug-drug similarity matrix, simply delete the section "_simmat_dc.txt" from 
	the filename and write whatever remains.
	-specify-arg is to control the parameters of a algorithm (0 for optimal arguments, 1 for default arguments)

You can see an example of running the PyDTI_simplified.py below. In this example, for Nuclear Receptors dataset, 
the wnngip method and the 65th random drug-drug similarity matrix are considered:

Enter method (wnngip,nrlmf,netlaprls,blmnii): wnngip
Enter dataset (nr,ic,e,gpcr): nr
Enter drug-drug similarity data name (ex: nr, ic, e, gpcr, Cosine_e, Tanimoto_gpcr, Dice_nr, allones_ic, 95e, ...): 65nr
Enter data directory (ex: F:/PythonCodes/DTI/datasets):  F:/PythonCodes/DSComparisons/datasets/
Enter output directory (ex: F:/PythonCodes/DTI/outputs/):  F:/PythonCodes/DSComparisons/outputs/  
Enter specify-arg (0 for optimal arguments, 1 for default arguments): 0
---------------------------------------------------------------------------------------------
The results of all the experiments and comparisons we have done are in folder "ComparisonResults".
---------------------------------------------------------------------------------------------
You can run "compare_sims.py" for the comparision between different drug-drug similarities on all datasets.
----------------------------------------------------------------------------------------------
To plot the comparison results, you can run "plot_compare_sims.py" for the output files obtained by "compare_sims.py".
-----------------------------------------------------------------------------------------------
The results tables are calculated by "Generatetables.py" using output files obtained by "compare_sims.py".
----------------------------------------------------------------------------------------------
