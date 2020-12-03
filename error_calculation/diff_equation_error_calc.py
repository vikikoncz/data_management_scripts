#Python 2.7 script
#Keszitett: Koncz Viktoria
#Datum: 2017. december 1.
#Feladata: Sav-bazis tranziens szimulacioja soran kimentett profilok (+ ido- es terbeli derivaltak) visszahelyettesites az eredeti differencial-egyenletbe,
# ebbol valamilyen modon aggregalt hiba szamolas; 
#############################################################################################

import math 

print "PYTHON scripts are easy"

#####################################
#Parameters + constants
#####################################
D_h = 9.31e-9   # m2 / s
D_oh = 5.28e-9
D_k = 1.96e-9
D_cl = 2.04e-9
K_v = 1e-14  # mol2 / dm6
K_v = 1e-8  # mol2 / m6
k_v = 1.3e11  # dm3 / mol /s
k_v = 1.3e8 # m3 / mol / s

T = 298  # K 
K_fix = 1e-4
k_fix = 6e9
c0_fa = 4e-3   
R = 8.3145  # J / mol / K
F = 96485  # s * A / mol
epsilon = 8.8542e-12  # F / m   #vakuum
epsilon = 6.954e-10  # viz


###############################################
# EQUATION-s
###############################################

# ht = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh)
# oht = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh)
# kt = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx)
# clt = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx)
# -epsilon * phixx = F * (h-oh+k-cl-c_fa)

# res_h = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh) - ht
# res_oh = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh) - oht
# res_k = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx) - kt
# res_cl = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx) - clt
# res_poiss = F * (h-oh+k-cl-c_fa) + epsilon * phixx

# res_node = res_h^2 + res_oh^2 + res_k^2 + res_cl^2 + res_poiss^2
# res_domain = SUM(res_node)

FRT = F / R / T
K = k_v * K_v


#FILE_PROBA='proba.dat'
FILE_PROBA='DER_c_kcl_b_0.0c_kcl_a_0.0_U_10.0Vt_0.06_0.0_10.0Vt_150.0_Wed_Nov_29_17.43.49_CET_2017.dat'

FILE_RESULTS_NODE='error_NODE.dat'		#########*****KITOLTENI*****###########
FILE_RESULTS_CUMULATED='error_CUMULATED.dat'		#########*****KITOLTENI*****###########
FILE_RESULTS_PERCENT='error_NODE_PERCENT.dat'   ##############KITOLTENI#############

f_proba= open(FILE_PROBA, 'r')
f_results_node=open(FILE_RESULTS_NODE, 'w')
f_results_cumulated=open(FILE_RESULTS_CUMULATED, 'w')

row_proba=f_proba.readlines() #az adatfajl beolvasas; 
num_rows=len(row_proba) #adatfajl sorainak a hossza

#WRITE HEADER to the NODE file
f_results_node.write('%ERROR calculation NODE\n')
f_results_node.write('% res_h = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh) - ht \n')
f_results_node.write('% res_oh = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh) - oht \n')
f_results_node.write('% res_k = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx) - kt \n')
f_results_node.write('% res_cl = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx) - clt \n')
f_results_node.write('% res_poiss = F * (h-oh+k-cl-c_fa) + epsilon * phixx \n')
f_results_node.write('% res_node = res_h^2 + res_oh^2 + res_k^2 + res_cl^2 + res_poiss^2 \n')
f_results_node.write('% \n')
f_results_node.write('% \n')

f_results_node.write('% x res_h res_oh res_k res_cl res_poiss res_node \n')

f_results_node.write('% \n')
f_results_node.write('% \n')

#WRITE HEADER to the CUMULATED file
f_results_cumulated.write('%ERROR calculation NODE\n')
f_results_cumulated.write('% res_h = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh) - ht \n')
f_results_cumulated.write('% res_oh = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh) - oht \n')
f_results_cumulated.write('% res_k = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx) - kt \n')
f_results_cumulated.write('% res_cl = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx) - clt \n')
f_results_cumulated.write('% res_poiss = F * (h-oh+k-cl-c_fa) + epsilon * phixx \n')
f_results_cumulated.write('% res_node = res_h^2 + res_oh^2 + res_k^2 + res_cl^2 + res_poiss^2 \n')
f_results_cumulated.write('% res_cum =  \n')   ###KITOLTENI#####
f_results_cumulated.write('% \n')
f_results_cumulated.write('% \n')

f_results_cumulated.write('% t res_cum \n')

f_results_cumulated.write('% \n')
f_results_cumulated.write('% \n')

res_cum = 0

i = 0

for row_index in range(num_rows):

	current_row=row_proba[row_index]
	row_length = len(current_row)
	
	
	if (row_length > 2):
		#Header-t esetleg masoljuk at az eredmeny fajlba
		if (current_row[0]=="%") & ((current_row[1]!="t") | (current_row[2]!="=")):
			#WRITE NODE file
			f_results_node.write(current_row)
			#WRITE CUMULATED file
			f_results_cumulated.write(current_row)
	
		#t ido kiszedes
		elif (current_row[0]=="%") & (current_row[1]=="t") & (current_row[2]=="="):
			
			t = current_row
			
			t = t.replace("%t=","")
			t.strip()  #utolso \n jel kiszedese
			t=float(t)
			
			f_results_node.write(current_row)
			
			f_results_cumulated.write(str(t))
			f_results_cumulated.write('\t')	
			res_cum = 0; #szamlalo nullazasa	

			i = 1
	
		else: 
			values = current_row.split("\t")
			index=len(values)
			values[index-1]=values[index-1].strip()
			
			
			x = float(values[0]) # mm
			hoh = float(values[1])  # mol 2 / m6
			hx = float(values[2])
			ohx = float(values[3])	
			kx = float(values[4])	
			clx = float(values[5])	
			phix = float(values[6])	
			phixx = float(values[7])	
			hxx = float(values[8])	
			ohxx = float(values[9])	
			kxx = float(values[10])	
			clxx = float(values[11])	
			ht = float(values[12])	
			oht = float(values[13])	
			kt = float(values[14])	
			clt = float(values[15])	
			phit = float(values[16])	
			h = float(values[17])	
			oh = float(values[18])	
			k = float(values[19])	
			cl = float(values[20])	
			c_fa = float(values[21])		
			phi = float(values[22])	
			
			
			res_h = D_h * hxx + D_h*FRT * (hx*phix + h*phixx) + K - k_v*h*oh - ht
			res_oh = D_oh * ohxx - D_oh*FRT * (ohx*phix + oh*phixx) + K - k_v*h*oh - oht
			res_k = D_k * kxx + D_k*FRT * (kx*phix + k*phixx) - kt
			res_cl = D_cl * clxx - D_cl*FRT * (clx*phix + cl*phixx) - clt
			res_poiss = F * (h-oh+k-cl-c_fa) + epsilon * phixx

			res_node = res_h**2 + res_oh**2 + res_k**2 + res_cl**2 + res_poiss**2

			# res_domain = SUM(res_node)
			res_cum = res_cum + res_node
			
			#WRITE NODE file
			f_results_node.write(str(x))
			f_results_node.write('\t')
			f_results_node.write(str(res_h))
			f_results_node.write('\t')
			f_results_node.write(str(res_oh))
			f_results_node.write('\t')
			f_results_node.write(str(res_k))
			f_results_node.write('\t')
			f_results_node.write(str(res_cl))
			f_results_node.write('\t')
			f_results_node.write(str(res_poiss))
			f_results_node.write('\t')
			f_results_node.write(str(res_node))
			f_results_node.write('\n')

			#WRITE CUMULATED file
			

	#praktikusan nulla, vagy 1 hosszu; ez '\n' ill szimpla '%' karakter lehet, ezeket csak at kell masolni
	else:
			f_results_node.write(current_row)

			if (i==1):
				f_results_cumulated.write(str(res_cum))
				f_results_cumulated.write('\n')
				i = 0
			
			
#closing files
f_proba.close()
f_results_node.close()
f_results_cumulated.close()
