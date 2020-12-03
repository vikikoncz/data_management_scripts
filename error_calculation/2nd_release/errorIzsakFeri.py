#Python 2.7 script
#Keszitett: Koncz Viktoria
#Datum: 2020. januar
#Feladata: Augusztusban gyartott errorUtils mintajara, IzsakFeri altal javasolt hibametrikat szamol.  
#############################################################################################

import math
import constants as c 
import errorUtils
import numpy as np


#ezek legyenek teljesen kulon modulban
def calculateErrorIZS(current_file, DIR, f_out_base, FILE_RESULTS):
    print("Let's go to play hockey")

    N_mesh = errorUtils.numberOfMeshPoints(current_file)
    function_type = errorUtils.getFunctionType(current_file)	
		
    f_proba= open(current_file, 'r')

    row_proba=f_proba.readlines() #az adatfajl beolvasas; 
    num_rows=len(row_proba) #adatfajl sorainak a hossza

    print "Num_rows = "	
    print(num_rows)
    i = 0

    #decalre numpy arrays to TV calculation
    list_h = []
    list_oh = []
    list_k = []
    list_cl = []
	
    #array: calculated TV - t
    list_t_TV_h = []
    list_t_TV_oh = []
    list_t_TV_k = []
    list_t_TV_cl = []
	
    list_x_resh = []
    list_x_resoh = []
    list_x_resk = []
    list_x_rescl = []
	
    list_res_t_h = []
    list_res_t_oh = []
    list_res_t_k = []
    list_res_t_cl = []
	

    for row_index in range(num_rows):

        current_row=row_proba[row_index]
        row_length = len(current_row)
	
	
        if (row_length > 2):
            #Header-t esetleg masoljuk at az eredmeny fajlba
            if (current_row[0]=="%") & ((current_row[1]!="t") | (current_row[2]!="=")):
                viki = 0	
                #print "notebook" 	
                #WRITE NODE file
                #f_results_node.write(current_row)
                #WRITE CUMULATED file
                #f_results_cumulated.write(current_row)
	
	    #t ido kiszedes
            elif (current_row[0]=="%") & (current_row[1]=="t") & (current_row[2]=="="):
                t = current_row
                t = t.replace("%t=","")
                t.strip()  #utolso \n jel kiszedese
                t=float(t)
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
                h = float(values[17])	#
                oh = float(values[18])	#
                k = float(values[19])	#
                cl = float(values[20])	#
                c_fa = float(values[21])		
                phi = float(values[22])	
			
			
                res_h = c.D_h * hxx + c.D_h*c.FRT * (hx*phix + h*phixx) + c.K - c.k_v*h*oh - ht
                res_oh = c.D_oh * ohxx - c.D_oh*c.FRT * (ohx*phix + oh*phixx) + c.K - c.k_v*h*oh - oht
                res_k = c.D_k * kxx + c.D_k*c.FRT * (kx*phix + k*phixx) - kt
                res_cl_new = c.D_cl * clxx - c.D_cl*c.FRT * (clx*phix + cl*phixx) - clt
                res_poiss = c.F * (h-oh+k-cl-c_fa) + c.epsilon * phixx
				
                res_h_abs = abs(res_h)
                res_oh_abs = abs(res_oh)
                res_k_abs = abs(res_k)
                res_cl_abs = abs(res_cl_new)	
				
                list_x_resh.append([x, res_h_abs])
                list_x_resoh.append([x, res_oh_abs])
                list_x_resk.append([x, res_k_abs])
                list_x_rescl.append([x, res_cl_abs])


                #add h, oh, k, cl to lists
                list_h.append(h)
                list_oh.append(oh)
                list_k.append(k)
                list_cl.append(cl)
					
#egy darab idopillanathoz tartozo eredmenytomb vege
#praktikusan nulla, vagy 1 hosszu; ez '\n' ill szimpla '%' karakter lehet, ezeket csak at kell masolni
        else:
            viki = 1
            #print "LYON"
            if (i == 1):	
                TV_h = calcualteTV(list_h)
                TV_oh = calcualteTV(list_oh)
                TV_k = calcualteTV(list_k)
                TV_cl = calcualteTV(list_cl)
				
                intx_h = integralList(list_x_resh)
                intx_oh = integralList(list_x_resoh) 				
                intx_k = integralList(list_x_resk)
                intx_cl = integralList(list_x_rescl)
				
                list_x_resh = []
                list_x_resoh = []
                list_x_resk = []
                list_x_rescl = []
				
                list_h = []
                list_oh = []
                list_k = []
                list_cl = []
				
                list_res_t_h.append([t, intx_h])
                list_res_t_oh.append([t, intx_oh])
                list_res_t_k.append([t, intx_k])
                list_res_t_cl.append([t, intx_cl])
				
                list_t_TV_h.append([t, TV_h])
                list_t_TV_oh.append([t, TV_oh])
                list_t_TV_k.append([t, TV_k])
                list_t_TV_cl.append([t, TV_cl])	
				
                i = 0
			
	
		
    #closing files
    f_proba.close()
    l = len(list_t_TV_h)
    print "list_t_TV_h"
    print l
    print list_t_TV_h
    print list_t_TV_h[3][1]

	
    TV_max_h = maxTV(list_t_TV_h)
    TV_max_oh = maxTV(list_t_TV_oh)
    TV_max_k = maxTV(list_t_TV_k)
    TV_max_cl = maxTV(list_t_TV_cl)

    #integral the list: integralList
    TV_t_integral_h = integralList(list_t_TV_h)
    TV_t_integral_oh = integralList(list_t_TV_oh)
    TV_t_integral_k = integralList(list_t_TV_k)
    TV_t_integral_cl = integralList(list_t_TV_cl)

    #integral t residuals
    Res_t_integral_h = integralList(list_res_t_h)
    Res_t_integral_oh = integralList(list_res_t_oh)
    Res_t_integral_k = integralList(list_res_t_k)
    Res_t_integral_cl = integralList(list_res_t_cl)	

    print("TV_max_h=" + str(TV_max_h))	
    print("TV_max_oh=" + str(TV_max_oh))
    print("TV_max_k=" + str(TV_max_k))	
    print("TV_max_cl=" + str(TV_max_cl))


    print("TV_t_integral_h=" + str(TV_t_integral_h))	
    print("TV_t_integral_oh=" + str(TV_t_integral_oh))
    print("TV_t_integral_k=" + str(TV_t_integral_k))	
    print("TV_t_integral_cl=" + str(TV_t_integral_cl))

    print("Res_t_integral_h=" + str(Res_t_integral_h))
    print("Res_t_integral_oh=" + str(Res_t_integral_oh))
    print("Res_t_integral_k=" + str(Res_t_integral_k))
    print("Res_t_integral_cl=" + str(Res_t_integral_cl))			


    f_results=open(FILE_RESULTS, 'a') 
    #TODO : ebbol kellene majd teljes hibat szamolni
    	
    
    tvt_h = math.sqrt(TV_max_h * TV_t_integral_h * c.D_h)
    tvt_oh = math.sqrt(TV_max_oh * TV_t_integral_oh * c.D_oh)
    tvt_k = math.sqrt(TV_max_k * TV_t_integral_k * c.D_k)
    tvt_cl = math.sqrt(TV_max_cl * TV_t_integral_cl * c.D_cl)
    
    error_h = Res_t_integral_h + tvt_h
    error_oh = Res_t_integral_oh + tvt_oh
    error_k = Res_t_integral_k + tvt_k
    error_cl = Res_t_integral_cl + tvt_cl

    f_results.write(str(N_mesh))
    f_results.write('\t')
    f_results.write(str(function_type))
    f_results.write('\t')	
   	
    
    f_results.write(str(Res_t_integral_h))
    f_results.write('\t')
    f_results.write(str(Res_t_integral_oh))
    f_results.write('\t')	
    f_results.write(str(Res_t_integral_k))
    f_results.write('\t')	
    f_results.write(str(Res_t_integral_cl))
    f_results.write('\t')	
    
    f_results.write(str(tvt_h))
    f_results.write('\t')	
    f_results.write(str(tvt_oh))
    f_results.write('\t')
    f_results.write(str(tvt_k))
    f_results.write('\t')	
    f_results.write(str(tvt_cl))
    f_results.write('\t')

    f_results.write(str(error_h))
    f_results.write('\t')	
    f_results.write(str(error_oh))
    f_results.write('\t')
    f_results.write(str(error_k))
    f_results.write('\t')	
    f_results.write(str(error_cl))
    f_results.write('\n')			  		

    f_results.close()	

def calcualteTV(list):
	#print("Viki")
	#vegig gyalogolok a listan: 
	
	sum = 0
	l = len(list) - 1
	for i in range(l):
	    sum = sum + abs(list[i+1] - list[i])
		
	return sum
	
	
def maxTV(list):

	l = len(list)
	max = list[0][1]
	for i in range(l):
		if list[i][1] > max:
			max = list[i][1]	

	return max   


def integralList(list):
	
	sum = 0
	l = len(list) - 1
	for i in range(l):
		diff_x = (list[i+1][0] + list[i][0]) / 2
		diff_y = (list[i+1][1] + list[i][1]) / 2
		sum = sum + diff_x * diff_y

	return sum






