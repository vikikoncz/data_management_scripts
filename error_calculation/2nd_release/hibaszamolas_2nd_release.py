#Python 2.7 script
#Keszitett: Koncz Viktoria
#Datum: 2019. augusztus
#Feladata: adott mappaban levo, kimentett derivative_profiles fajlokra hibat szamol. Tobbfele uzemmod lehet a hibaszamolasra, ezeket vlaahogyan abrazolni is probalja.  
#############################################################################################

import math
import os 
import array as arr
#import PyGnuplot as gp  ezt nem sikerult installalni
import numpy as np
import subprocess
import errorUtils
import errorIzsakFeri

#import matplotlib.pyplot as plt ezt sem szereti

print "PYTHON scripts are easy: 2019. SUMMER - ERROR calculation"


#subprocess.call(['./characteristic.gnuplot'])

#megint csinaljunk egy probat...
#Phyndi trial
DIR_SOURCE = "/home/vikik/adaptive_mesh_new_release/hibaszamolas_python/hibaszamolas2nd_release/"
DIR = "/home/vikik/adaptive_mesh_new_release/hibaszamolas_python/hibaszamolas2nd_release/error_results/proba/"  #ide kell majd a vegeredmenyeket irni

FILE_RESULTS = DIR + "errorIZS.dat"

fileok=[]


for file in os.listdir(DIR_SOURCE):
    if file.endswith(".dat"):
        #print(os.path.join("/mydir", file))
	#fileok.append(file)
	#print file
	fileok.append(file)

print fileok

num_files=len(fileok)

f_results=open(FILE_RESULTS, 'w')
f_results.write('%N_mesh Function_type res_h res_oh res_k res_cl tvt_h tvt_oh tvt_k tvt_cl error_h error_oh error_k error_cl')
f_results.write('\n') 

f_results.close()


for file_index in range(num_files):

	current_file = fileok[file_index]
	mode = 1	

	#call function with current_file
	#errorUtils.calculatError(current_file, mode, DIR)
	f_out_base = errorUtils.generateOutputFileName(current_file)  #filenev alap szamolas	
	f_node = errorUtils.calculatErrorNode(current_file, mode, DIR, f_out_base)  #error_node
	#errorUtils.calculateErrorEdge(f_node, f_out_base, mode, DIR)   #error_edge
	#errorIzsakFeri.calculateErrorIZS(current_file, DIR, f_out_base, FILE_RESULTS)	#errorIZSF	







