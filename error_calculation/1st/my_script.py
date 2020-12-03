#PYTHON 2.7 script
#Keszitette: Koncz Viktoria
#2015. julius. 14.
#Feladata: Ket COMSOL profile fajl (amit az en JAVA COMSOL programom keszit) osszehasonlitasa, abbol ERROR szamitas. Valtozonkent es majd skalazva, kumulalva.
#Eredmenyt GNUPLOT-tal konnyen feldolgozhato fajlba menti ki.
######################################################################################

import math 

print "PYTHON scripts are easy"

DIR='/home/viki/acidbase_transient_data/ugras/profiles_MESH_experiments/'  #MY_UBUNTU  #########*****KITOLTENI*****###########
#DIR='/home/viki/Dokumentumok/python/'	#home library in UBUNTU where developed
DIR_results='/home/viki/acidbase_transient_data/ugras/error/reference_n_alap_500000_n_refined_0/'
FILE_PROBA='c_kcl_b_0.0c_kcl_a_0.0_U_10.0Vt_0.06_0.0_10.0Vt_400.0_n_alap_1000_n_refined_5000_Thu_Jul_09_23.43.02_CEST_2015.dat'		#########*****KITOLTENI*****###########
FILE_REF='c_kcl_b_0.0c_kcl_a_0.0_U_10.0Vt_0.06_0.0_10.0Vt_400.0_MESH_ekvi_500000_Thu_Aug_13_05.29.13_CEST_2015.dat'		#########*****KITOLTENI*****###########
FILE_RESULTS='error_not_scaled_reference_%%%_n_alap_500000_n_refined_0_simulation_n_alap_1000_n_refined_5000.dat'		#########*****KITOLTENI*****###########

f_proba= open(DIR+FILE_PROBA, 'r')  #majd ebbol kell kivenni az eredmeny fajl header-jet!!!
f_ref=open(DIR+FILE_REF,'r')
f_results=open(DIR_results+FILE_RESULTS, 'w')

scale_H=1
scale_OH=1
scale_K=1
scale_Cl=1
scale_C_FA=1
scale_PHI=1

scale = [0, scale_H, scale_OH, scale_K, scale_Cl, scale_C_FA, scale_PHI]

#write header
f_results.write('%ERROR calculation\n')
f_results.write('%Reference file MESH: n_alap=500000; n_refined=0 points\n') #########*****KITOLTENI*****###########
f_results.write('%SCALE settings\n')
f_results.write('%\tscale_H='+str(scale_H)+'\n')
f_results.write('%\tscale_OH='+str(scale_OH)+'\n')
f_results.write('%\tscale_K='+str(scale_K)+'\n')
f_results.write('%\tscale_Cl='+str(scale_Cl)+'\n')
f_results.write('%\tscale_C_FA='+str(scale_C_FA)+'\n')
f_results.write('%\tscale_PHI='+str(scale_PHI)+'\n')
f_results.write('%Cumulative ERROR calculation method:  error[index]+=pow(error[i],2)*scale[i]\n')  #########*****KITOLTENI*****###########
f_results.write('%Last column means CUMULATIVE ERROR\n')

#print f
row_proba=f_proba.readlines() #az adatfajl beolvasas; a ket adatfajl, melybol az ERROR szamitodik, ugyanolyan felepitesunek kell lenni;  
num_rows=len(row_proba) #adatfajl sorainak a hossza
row_ref=f_ref.readlines() #a referencia fajl beolvasas
num_ref=len(row_ref)	#a referencia fajl sorainak a szama

# hasonlitsuk ossze
if num_rows!=num_ref:
	print "ERROR happaned. Check the headers of the two comparable files. Something is missing maybe."
	print str(num_rows)+'\n'
	print str(num_ref)+'\n'
	exit()

print num_rows

for row_index in range(num_rows):

	current_row=row_proba[row_index]
	current_ref=row_ref[row_index]
	
	if (current_row[0]=="%") | (current_row[0]=="\n"):
		f_results.write(current_row)
		
	else:
		values=current_row.split("\t") #visszaadott egy darab stringet szetbontja TAB-onkent
		ref=current_ref.split("\t")
		index=len(values)
		values[index-1]=values[index-1].strip() #utolso tartalmaz egy ujsor jelet (\n), ezt ki kell szedni 
		ref[index-1]=ref[index-1].strip()		
		
		error = range(index+1) # define an error list
		error[index]=0
		for i in range(len(values)):
			values[i]=float(values[i])
			ref[i]=float(ref[i])
			if i==0:	#az 'x' erteket csak at kell masolni
				error[i]=values[i]
			else:
				#error[i]=values[i]-ref[i]  #ez csak az elteres, skalazatlanul!!!
				if ref[i]==0:
					error[i]=0
				else:
					error[i]=(values[i]-ref[i])/(ref[i])*100 #ez az adott valtozo szazalekos hibajat szamolja ki (%)
				error[index]+=pow(error[i],2)*scale[i]	# szamolja a kumulalt hibat 

		for i in range(len(error)):
			f_results.write(str(error[i]))
			if i!=(len(error)-1):
				f_results.write('\t')
		f_results.write('\n')

#closing files
f_proba.close()
f_ref.close()
f_results.close()
