#Python 2.7 script
#Keszitett: Koncz Viktoria
#Datum: 2019. augusztus
#Feladata: adott mappaban levo, kimentett derivative_profiles fajlokra hibat szamol. Tobbfele uzemmod lehet a hibaszamolasra, ezeket vlaahogyan abrazolni is probalja. Ehhez keszult Utils. 
#############################################################################################

import math
import constants as c 



def my_function():
	print("Hello from a function")

def calculateERRORs():
	#ez az ami majd osszefogja az egeszet
	f_out_base = generateOutputFileName(current_file)

def calculatErrorNode(current_file, mode, DIR, f_out_base):
	print(current_file)
	print (mode)
	print (c.T)
	
	#f_out_base = generateOutputFileName(current_file)
	FILE_RESULTS_NODE = DIR + f_out_base + "_mode_" + str(mode) + "_NODE.dat"	
	FILE_RESULTS_CUMULATED = DIR + f_out_base + "_mode_" + str(mode) + "_CUMULATED_node.dat"
	
	f_proba= open(current_file, 'r')
	f_results_node=open(FILE_RESULTS_NODE, 'w')
	f_results_cumulated=open(FILE_RESULTS_CUMULATED, 'w')

	N_mesh = numberOfMeshPoints(current_file)

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

	f_results_node.write('% x res_h res_h_szaz res_h_norm res_oh res_oh_szaz res_oh_norm res_k res_k_szaz res_k_norm res_cl res_cl_szaz res_cl_norm res_poiss res_poiss_szaz res_poiss_norm res_node res_node_szaz res_node_no_poisson res_node_no_poisson_szaz res_node_norm res_node_norm_with_poiss ht oht kt clt np_h_j np_oh_j np_k_j np_cl_j np_h_diff np_oh_diff np_k_diff np_cl_diff np_h_migr np_oh_migr np_k_migr np_cl_migr np_reak\n')


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

	f_results_cumulated.write('% t res_cum res_cum_no_poisson res_cum_szaz res_cum_no_poisson_szaz res_cum_norm res_cum_norm_with_poiss \n')

	f_results_cumulated.write('% \n')
	f_results_cumulated.write('% \n')

	res_cum = 0
	res_cum_no_poisson = 0;
	res_cum_szaz = 0;
	res_cum_no_poisson_szaz = 0;
	res_cum_norm = 0;
	res_cum_norm_with_poiss = 0;	

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
				res_cum_no_poisson = 0;
				res_cum_szaz = 0;
				res_cum_no_poisson_szaz = 0;
				res_cum_norm = 0;
				res_cum_norm_with_poiss = 0;

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
			
			
				res_h = c.D_h * hxx + c.D_h*c.FRT * (hx*phix + h*phixx) + c.K - c.k_v*h*oh - ht
				res_oh = c.D_oh * ohxx - c.D_oh*c.FRT * (ohx*phix + oh*phixx) + c.K - c.k_v*h*oh - oht
				res_k = c.D_k * kxx + c.D_k*c.FRT * (kx*phix + k*phixx) - kt
				res_cl = c.D_cl * clxx - c.D_cl*c.FRT * (clx*phix + cl*phixx) - clt
				res_poiss = c.F * (h-oh+k-cl-c_fa) + c.epsilon * phixx

				#melyik egyenlet melyik oldala: szazalekszamitas miatt fontos
				np_h_j = c.D_h * hxx + c.D_h*c.FRT * (hx*phix + h*phixx) + c.K - c.k_v*h*oh
				np_oh_j = c.D_oh * ohxx - c.D_oh*c.FRT * (ohx*phix + oh*phixx) + c.K - c.k_v*h*oh
				np_k_j = c.D_k * kxx + c.D_k*c.FRT * (kx*phix + k*phixx)
				np_cl_j = c.D_cl * clxx - c.D_cl*c.FRT * (clx*phix + cl*phixx)
				p_j = c.F * (h-oh+k-cl-c_fa)
				p_b = - c.epsilon * phixx  #Poisson-egyenlet bal oldala	

				#kulonbozo tagok az egyenletekben
				#diffuzios tagok
				np_h_diff = c.D_h * hxx
				np_oh_diff = c.D_oh * ohxx
				np_k_diff = c.D_k * kxx
				np_cl_diff = c.D_cl * clxx
								
				#ionmigracios tagok
				np_h_migr = c.D_h*c.FRT * (hx*phix + h*phixx)
				np_oh_migr = - c.D_oh*c.FRT * (ohx*phix + oh*phixx)
				np_k_migr = c.D_k*c.FRT * (kx*phix + k*phixx)
				np_cl_migr = - c.D_cl*c.FRT * (clx*phix + cl*phixx)
				

				#reakciotagok
				np_h_reak = c.K - c.k_v*h*oh
				np_oh_reak = c.K - c.k_v*h*oh
				np_k_reak = 0
				np_cl_reak = 0

				#diff. ionmigracios es reakciotagok negyzetei
				np_h_negyz = np_h_diff*np_h_diff + np_h_migr*np_h_migr + np_h_reak*np_h_reak + ht*ht
				np_oh_negyz = np_oh_diff*np_oh_diff + np_oh_migr*np_oh_migr + np_oh_reak*np_oh_reak + oht*oht
				np_k_negyz = np_k_diff*np_k_diff + np_k_migr*np_k_migr + np_k_reak*np_k_reak +kt*kt
				np_cl_negyz = np_cl_diff*np_cl_diff + np_cl_migr*np_cl_migr + np_cl_reak*np_cl_reak +clt*clt
 				
				
				#hiba: legyen az egyeb tagokkal normalva
				res_h_norm = res_h / math.sqrt(np_h_negyz)
				res_oh_norm = res_oh / math.sqrt(np_oh_negyz)
				res_k_norm = res_k /math.sqrt(np_k_negyz)
				res_cl_norm = res_cl / math.sqrt(np_cl_negyz)
				res_poiss_norm = res_poiss / math.sqrt(p_j*p_j + p_b*p_b)
				#res_poiss_norm = res_poiss / 1

				#
				res_h_absz_norm = res_h / (abs(np_h_diff) + abs(np_h_migr) + abs(np_h_reak) + abs(ht))
				res_oh_absz_norm = res_oh / (abs(np_oh_diff) + abs(np_oh_migr) + abs(np_oh_reak) + abs(oht))
				res_k_absz_norm = res_k / (abs(np_k_diff) + abs(np_k_migr) + abs(np_k_reak) + abs(kt))
				res_cl_absz_norm = res_cl / (abs(np_cl_diff) + abs(np_cl_migr) + abs(np_cl_reak) + abs(clt))
				res_poiss_absz_norm = res_poiss / (abs(p_j) + abs(p_b))				


				#szazalekos elteresek az egyenletekben: remelek ezek nem lesznek tul nagyok 1: ez a 100%
				res_h_szaz = res_h / np_h_j
				res_oh_szaz = res_oh / np_oh_j
				res_k_szaz = res_k / np_k_j
				res_cl_szaz = res_cl / np_cl_j
				res_poiss_szaz = res_poiss / p_j
				#res_poiss_szaz = 0				

				res_node = res_h**2 + res_oh**2 + res_k**2 + res_cl**2 + res_poiss**2
				res_node_no_poisson = res_h**2 + res_oh**2 + res_k**2 + res_cl**2 
				res_node_szaz = res_h_szaz**2 + res_oh_szaz**2 + res_k_szaz**2 + res_cl_szaz**2 + res_poiss_szaz**2
				res_node_no_poisson_szaz = res_h_szaz**2 + res_oh_szaz**2 + res_k_szaz**2 + res_cl_szaz**2

				res_node_norm = math.sqrt(res_h_norm**2 + res_oh_norm**2 + res_k_norm**2 + res_cl_norm**2)
				res_node_norm_with_poiss = math.sqrt(res_h_norm**2 + res_oh_norm**2 + res_k_norm**2 + res_cl_norm**2 + res_poiss_norm**2)


				# res_domain = SUM(res_node)
				res_cum = res_cum + res_node
				res_cum_no_poisson = res_cum_no_poisson + res_node_no_poisson
				res_cum_szaz = res_cum_szaz + res_node_szaz
				res_cum_no_poisson_szaz = res_cum_no_poisson_szaz + res_node_no_poisson_szaz
				res_cum_norm = res_cum_norm + res_node_norm 
				res_cum_norm_with_poiss = res_cum_norm_with_poiss + res_node_norm_with_poiss
			
				#WRITE NODE file
				f_results_node.write(str(x))  #0
				f_results_node.write('\t')
				f_results_node.write(str(res_h)) #1
				f_results_node.write('\t')
				f_results_node.write(str(res_h_szaz))  #2
				f_results_node.write('\t')
				f_results_node.write(str(res_h_norm))  #3
				f_results_node.write('\t')
				f_results_node.write(str(res_oh))  #4
				f_results_node.write('\t')
				f_results_node.write(str(res_oh_szaz))  #5
				f_results_node.write('\t')
				f_results_node.write(str(res_oh_norm))  #6
				f_results_node.write('\t')
				f_results_node.write(str(res_k))  #7
				f_results_node.write('\t')
				f_results_node.write(str(res_k_szaz))  #8
				f_results_node.write('\t')
				f_results_node.write(str(res_k_norm))  #9
				f_results_node.write('\t')	
				f_results_node.write(str(res_cl))  #10
				f_results_node.write('\t')
				f_results_node.write(str(res_cl_szaz))  #11
				f_results_node.write('\t')
				f_results_node.write(str(res_cl_norm))  #12
				f_results_node.write('\t')
				f_results_node.write(str(res_poiss))  #13
				f_results_node.write('\t')
				f_results_node.write(str(res_poiss_szaz))  #14
				f_results_node.write('\t')
				f_results_node.write(str(res_poiss_norm))  #15
				f_results_node.write('\t')
				f_results_node.write(str(res_node))  #16
				f_results_node.write('\t')
				f_results_node.write(str(res_node_szaz))  #17
				f_results_node.write('\t')
				f_results_node.write(str(res_node_no_poisson))  #18
				f_results_node.write('\t')
				f_results_node.write(str(res_node_no_poisson_szaz))  #19
				f_results_node.write('\t')
				f_results_node.write(str(res_node_norm))  #20
				f_results_node.write('\t')
				f_results_node.write(str(res_node_norm_with_poiss))  #21
				f_results_node.write('\t')
				f_results_node.write(str(ht))  #22
				f_results_node.write('\t')
				f_results_node.write(str(oht))  #23
				f_results_node.write('\t')
				f_results_node.write(str(kt))  #24
				f_results_node.write('\t')
				f_results_node.write(str(clt))  #25
				f_results_node.write('\t')
				f_results_node.write(str(np_h_j))  #26
				f_results_node.write('\t')
				f_results_node.write(str(np_oh_j))  #27
				f_results_node.write('\t')
				f_results_node.write(str(np_k_j)) #28
				f_results_node.write('\t')
				f_results_node.write(str(np_cl_j)) #29
				#TODO: irjuk ki a reakcio, a migracios es a diffuzios tagokat is
				f_results_node.write('\t')
				f_results_node.write(str(np_h_diff)) #30 
				f_results_node.write('\t')
				f_results_node.write(str(np_oh_diff)) #31	
				f_results_node.write('\t')
				f_results_node.write(str(np_k_diff)) #32	
				f_results_node.write('\t')
				f_results_node.write(str(np_cl_diff)) #33
				f_results_node.write('\t')
				f_results_node.write(str(np_h_migr)) #34
				f_results_node.write('\t')
				f_results_node.write(str(np_oh_migr)) #35
				f_results_node.write('\t')
				f_results_node.write(str(np_k_migr)) #36
				f_results_node.write('\t')
				f_results_node.write(str(np_cl_migr)) #	37
				f_results_node.write('\t')
				f_results_node.write(str(np_h_reak)) #38
				f_results_node.write('\t')
				f_results_node.write(str(res_h_absz_norm)) #39
				f_results_node.write('\t')
				f_results_node.write(str(res_oh_absz_norm)) #40
				f_results_node.write('\t')
				f_results_node.write(str(res_k_absz_norm))  #41
				f_results_node.write('\t')
				f_results_node.write(str(res_cl_absz_norm))  #42
				f_results_node.write('\t')
				f_results_node.write(str(res_poiss_absz_norm)) #43	
				f_results_node.write('\t')
				f_results_node.write(str(p_j)) #44 Poisson jobb oldala	
				f_results_node.write('\t')
				f_results_node.write(str(p_b)) #45	Poisson bal oldala
				
				f_results_node.write('\n')

				#WRITE CUMULATED file
			

		#praktikusan nulla, vagy 1 hosszu; ez '\n' ill szimpla '%' karakter lehet, ezeket csak at kell masolni
		else:
			f_results_node.write(current_row)

			if (i == 1):
				f_results_cumulated.write(str(res_cum / int(N_mesh)))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_no_poisson / int(N_mesh)))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_szaz / int(N_mesh)))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_no_poisson_szaz / int(N_mesh)))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_norm / int(N_mesh)))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_norm_with_poiss / int(N_mesh)))
				f_results_cumulated.write('\n')
				i = 0
			
			
	#closing files
	f_proba.close()
	f_results_node.close()
	f_results_cumulated.close()	

	return FILE_RESULTS_NODE
	

def generateOutputFileName(current_file):

	f_source= open(current_file, 'r')

	rows=f_source.readlines() #az adatfajl beolvasas; 
	num_rows = len(rows)
	
	N_mesh = ''
	Function_type = ''

	#keressuk meg a header-t

	for row_index in range(num_rows):
		
		current_row = rows[row_index]	
		if (current_row == '%MESH SETTINGS\n'):
			print rows[row_index+1] #ebben van az n_mesh_real
			print rows[row_index+2] #ebben van a function_type
			N_mesh = rows[row_index+1]
			Function_type = rows[row_index+2]
			break
		

	#N_mesht es Function Type-ot atalakitani

	values = N_mesh.split("=")
	index=len(values)
	n=values[index-1].strip()
	print n

	values = Function_type.split("=")
	index=len(values)
	f=values[index-1].strip()
	print f

	FILE_new = 'Function_type_' + f + "_N_" + n + current_file
	#file_new = open(DIR + FILE_new, 'w')

	return FILE_new

def getFunctionType(current_file):
 
	f_source= open(current_file, 'r')

	rows=f_source.readlines() #az adatfajl beolvasas; 
	num_rows = len(rows)
	
	Function_type = ''
	
	for row_index in range(num_rows):
		current_row = rows[row_index]	
		if (current_row == '%MESH SETTINGS\n'):
			#print rows[row_index+1] #ebben van az n_mesh_real
			#print rows[row_index+2] #ebben van a function_type
			#N_mesh = rows[row_index+1]
			Function_type = rows[row_index+2]
			break

	values = Function_type.split("=")
	index=len(values)
	f=values[index-1].strip()
	#print('f=' + str(f))
	return f

def numberOfMeshPoints(current_file):
	
	f_source= open(current_file, 'r')

	rows=f_source.readlines() #az adatfajl beolvasas; 
	num_rows = len(rows)
	
	N_mesh = ''

	for row_index in range(num_rows):
		
		current_row = rows[row_index]	
		if (current_row == '%MESH SETTINGS\n'):
			#print rows[row_index+1] #ebben van az n_mesh_real			
			N_mesh = rows[row_index+1]
			break

	values = N_mesh.split("=")
	index=len(values)
	n=values[index-1].strip()

	return n 


def calculateErrorEdge(FILE_NODE, f_out_base, mode, DIR):

	FILE_RESULTS_CUMULATED = DIR + f_out_base + "_mode_" + str(mode) + "_CUMULATED_edge.dat"
	FILE_RESULTS_EDGE = DIR + f_out_base + "_mode_" + str(mode) + "_EDGE.dat"

	print(FILE_RESULTS_EDGE)
	

	f_results_cumulated=open(FILE_RESULTS_CUMULATED, 'w')	
	f_results_node=open(FILE_NODE, 'r')
	f_results_edge=open(FILE_RESULTS_EDGE, 'w')		

	#WRITE HEADER to the EDGE file
	f_results_edge.write('%ERROR calculation EDGE\n')
	f_results_edge.write('% res_h = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh) - ht \n')
	f_results_edge.write('% res_oh = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh) - oht \n')
	f_results_edge.write('% res_k = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx) - kt \n')
	f_results_edge.write('% res_cl = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx) - clt \n')
	f_results_edge.write('% res_poiss = F * (h-oh+k-cl-c_fa) + epsilon * phixx \n')
	f_results_edge.write('% res_node = res_h^2 + res_oh^2 + res_k^2 + res_cl^2 + res_poiss^2 \n')
	f_results_edge.write('% \n')
	f_results_edge.write('% \n')

	f_results_edge.write('% deltax res_h res_h_szaz res_h_norm res_oh res_oh_szaz res_oh_norm res_k res_k_szaz res_k_norm res_cl res_cl_szaz res_cl_norm res_poiss res_poiss_szaz res_poiss_norm res_node res_node_szaz res_node_no_poisson_edg res_node_no_poisson_szaz_edg res_node_norm_edg res_node_norm_with_poiss_edg\n')

	f_results_edge.write('% \n')
	f_results_edge.write('% \n')


	#WRITE HEADER to the CUMULATED file
	f_results_cumulated.write('%ERROR calculation EDGE\n')
	f_results_cumulated.write('% res_h = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh) - ht \n')
	f_results_cumulated.write('% res_oh = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh) - oht \n')
	f_results_cumulated.write('% res_k = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx) - kt \n')
	f_results_cumulated.write('% res_cl = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx) - clt \n')
	f_results_cumulated.write('% res_poiss = F * (h-oh+k-cl-c_fa) + epsilon * phixx \n')
	f_results_cumulated.write('% res_node = res_h^2 + res_oh^2 + res_k^2 + res_cl^2 + res_poiss^2 \n')
	f_results_cumulated.write('% res_cum =  \n')   ###KITOLTENI#####
	f_results_cumulated.write('% \n')
	f_results_cumulated.write('% \n')

	f_results_cumulated.write('% t res_cum_edg res_cum_no_poisson_edg res_cum_szaz_edg res_cum_no_poisson_szaz_edg res_cum_norm_edg res_cum_norm_with_poiss_edg  \n')

	f_results_cumulated.write('% \n')
	f_results_cumulated.write('% \n')


	row_proba=f_results_node.readlines() #az adatfajl beolvasas; 
	num_rows=len(row_proba) #adatfajl sorainak a hossza

	x_old = 0			
	res_h_old = 0
	res_h_szaz_old = 0
	res_h_norm_old = 0
	res_oh_old = 0
	res_oh_szaz_old = 0
	res_oh_norm_old = 0
	res_k_old = 0
	res_k_szaz_old = 0
	res_k_norm_old = 0
	res_cl_old = 0
	res_cl_szaz_old = 0
	res_cl_norm_old = 0
	res_poiss_old = 0
	res_poiss_szaz_old = 0
	res_poiss_norm_old = 0
	res_node_old = 0
	res_node_szaz_old = 0
	res_node_no_poisson_old = 0
	res_node_no_poisson_szaz_old = 0
	res_node_norm_old = 0
	res_node_norm_with_poiss_old = 0	

	x = 0			
	res_h = 0
	res_h_szaz = 0
	res_h_norm = 0
	res_oh = 0
	res_oh_szaz = 0
	res_oh_norm = 0
	res_k = 0
	res_k_szaz = 0
	res_k_norm = 0
	res_cl = 0
	res_cl_szaz = 0
	res_cl_norm = 0
	res_poiss = 0
	res_poiss_szaz = 0
	res_poiss_norm = 0
	res_node = 0
	res_node_szaz = 0
	res_node_no_poisson = 0
	res_node_no_poisson_szaz = 0
	res_node_norm = 0
	res_node_norm_with_poiss = 0


	res_cum_edg = 0; #szamlalo nullazasa	
	res_cum_no_poisson_edg = 0;
	res_cum_szaz_edg = 0;
	res_cum_no_poisson_szaz_edg = 0;
	res_cum_norm_edg = 0;
	res_cum_norm_with_poiss_edg = 0

	i=100
	first = 0
	
	for row_index in range(num_rows):

		current_row=row_proba[row_index]
		row_length = len(current_row)
	
	
		if (row_length > 2):
			#Header-t esetleg masoljuk at az eredmeny fajlba
			if (current_row[0]=="%") & ((current_row[1]!="t") | (current_row[2]!="=")):
				#WRITE EDGE file
				f_results_edge.write(current_row)

				#WRITE CUMULATED file
				f_results_cumulated.write(current_row)
	
			#t ido kiszedes
			elif (current_row[0]=="%") & (current_row[1]=="t") & (current_row[2]=="="):
												
				t = current_row
			
				t = t.replace("%t=","")
				t.strip()  #utolso \n jel kiszedese
				t=float(t)
			
				f_results_edge.write(current_row)
			
				f_results_cumulated.write(str(t))
				f_results_cumulated.write('\t')	
				res_cum_edg = 0; #szamlalo nullazasa	
				res_cum_no_poisson_edg = 0;
				res_cum_szaz_edg = 0;
				res_cum_no_poisson_szaz_edg = 0;
				res_cum_norm_edg = 0;
				res_cum_norm_with_poiss_edg = 0;

				i = 1
				first = 1


			else: 
				values = current_row.split("\t")
				index=len(values)
				values[index-1]=values[index-1].strip()

				x_old = x			
				res_h_old = res_h
				res_h_szaz_old = res_h_szaz
				res_h_norm_old = res_h_norm
				res_oh_old = res_oh
				res_oh_szaz_old = res_oh_szaz
				res_oh_norm_old = res_oh_norm
				res_k_old = res_k
				res_k_szaz_old = res_k_szaz
				res_k_norm_old = res_k_norm
				res_cl_old = res_cl
				res_cl_szaz_old = res_cl_szaz
				res_cl_norm_old = res_cl_norm
				res_poiss_old = res_poiss
				res_poiss_szaz_old = res_poiss_szaz
				res_poiss_norm_old = res_poiss_norm
				res_node_old = res_node
				res_node_szaz_old = res_node_szaz
				res_node_no_poisson_old = res_node_no_poisson
				res_node_no_poisson_szaz_old = res_node_no_poisson_szaz
				res_node_norm_old = res_node_norm
				res_node_norm_with_poiss_old = res_node_norm_with_poiss
				 

				x = float(values[0])			
				res_h = float(values[1])
				res_h_szaz = float(values[2])
				res_h_norm = float(values[3])
				res_oh = float(values[4])
				res_oh_szaz = float(values[5])
				res_oh_norm = float(values[6])
				res_k = float(values[7])
				res_k_szaz = float(values[8])
				res_k_norm = float(values[9])
				res_cl = float(values[10])
				res_cl_szaz = float(values[11])
				res_cl_norm = float(values[12])
				res_poiss = float(values[13])
				res_poiss_szaz = float(values[14])
				res_poiss_norm = float(values[15])
				res_node = float(values[16])
				res_node_szaz = float(values[17])
				res_node_no_poisson = float(values[18])
				res_node_no_poisson_szaz = float(values[19])
				res_node_norm = float(values[20])
				res_node_norm_with_poiss = float(values[21])

				if first==0:

					deltax = x - x_old			
					res_h_edg = (res_h + res_h_old) / 2
					res_h_szaz_edg = (res_h_szaz + res_h_szaz_old) / 2
					res_h_norm_edg = (res_h_norm + res_h_norm_old) / 2
					res_oh_edg = (res_oh + res_oh_old) / 2
					res_oh_szaz_edg = (res_oh_szaz + res_oh_szaz_old) / 2
					res_oh_norm_edg = (res_oh_norm + res_oh_norm_old) / 2
					res_k_edg = (res_k + res_k_old) / 2
					res_k_szaz_edg = (res_k_szaz + res_k_szaz_old) / 2
					res_k_norm_edg = (res_k_norm + res_k_norm_old) / 2
					res_cl_edg = (res_cl + res_cl_old) / 2
					res_cl_szaz_edg = (res_cl_szaz + res_cl_szaz_old) / 2
					res_cl_norm_edg = (res_cl_norm + res_cl_norm_old) / 2
					res_poiss_edg = (res_poiss + res_poiss_old) / 2
					res_poiss_szaz_edg = (res_poiss_szaz + res_poiss_szaz_old) / 2
					res_poiss_norm_edg = (res_poiss_norm + res_poiss_norm_old) / 2
					res_node_edg = (res_node + res_node_old) / 2
					res_node_szaz_edg = (res_node_szaz + res_node_szaz_old) / 2
					res_node_no_poisson_edg = (res_node_no_poisson + res_node_no_poisson_old) / 2
					res_node_no_poisson_szaz_edg = (res_node_no_poisson_szaz + res_node_no_poisson_szaz_old) / 2
					res_node_norm_edg = (res_node_norm + res_node_norm_old) / 2
					res_node_norm_with_poiss_edg = (res_node_norm_with_poiss + res_node_norm_with_poiss_old) / 2	

					#WRITE EDGE file
					f_results_edge.write(str(x + deltax))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_h_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_h_szaz_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_h_norm_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_oh_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_oh_szaz_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_oh_norm_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_k_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_k_szaz_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_k_norm_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_cl_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_cl_szaz_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_cl_norm_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_poiss_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_poiss_szaz_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_poiss_norm_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_node_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_node_szaz_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_node_no_poisson_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_node_no_poisson_szaz_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_node_norm_edg))
					f_results_edge.write('\t')
					f_results_edge.write(str(res_node_norm_with_poiss_edg))
					f_results_edge.write('\n')
				
					# res_domain = SUM(res_node)
					res_cum_edg = res_cum_edg + res_node_edg * deltax
					res_cum_no_poisson_edg = res_cum_no_poisson_edg + res_node_no_poisson_edg * deltax
					res_cum_szaz_edg = res_cum_szaz_edg + res_node_szaz_edg * deltax
					res_cum_no_poisson_szaz_edg = res_cum_no_poisson_szaz_edg + res_node_no_poisson_szaz_edg * deltax
					res_cum_norm_edg = res_cum_norm_edg + res_node_norm_edg * deltax
					res_cum_norm_with_poiss_edg = res_cum_norm_with_poiss_edg + res_node_norm_with_poiss_edg * deltax


				#legvegen i=0
				first=0

		else:	
			f_results_edge.write(current_row)	

			if (i==1):
				f_results_cumulated.write(str(res_cum_edg))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_no_poisson_edg))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_szaz_edg))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_no_poisson_szaz_edg))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_norm_edg))
				f_results_cumulated.write('\t')	
				f_results_cumulated.write(str(res_cum_norm_with_poiss_edg))
				f_results_cumulated.write('\n')
				i = 0
	
	
	f_results_edge.close()
	f_results_node.close()
	f_results_cumulated.close()			


