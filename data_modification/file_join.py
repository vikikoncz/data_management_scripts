#PYTHON 2.7 script
#Keszitette: Koncz Viktoria
#2015. szeptember. 30.
#Feladata: TXT adatfajlok egyesitese. Praktikusan append-el, egyesitett adatfajlba plusz oszlopot is szur be. Adott szimulacio beallitasait ez tartalmazza majd. 
#Eredmenyt CSV tipusu fajlba menti ki, ami konnyen megnyithato, nezgetheto, Mondrian, Statistica stb. tipusu szoftverrel.
######################################################################################

import math 

print "PYTHON scripts are easy"

#konyvtarnev, ahova irni kell
DIR_w='/home/vikik/Documents/statistica_python/'   #PHYNDI
#konyvtarnev, ahonnan hozzafuzni kell
DIR_add='/home/vikik/Documents/Mondrian_DATAS/20_V/c_kcl_base_0.06M_jav/' #PHYNDI
#ugyanez filenevekre
FILE_RESULT='results_jav.dat'  #ez az eredmenyfajl neve
FILE_ADD= 'expressions_20V_t_150s.csv'  #ezt a fajlt fogja hozzafuzni


##############################################
#EGYEB OSZLOPOK BERAKASA, EHHEZ VALTOZOK DEFINIALASA
description='c_kcl_t_base_0.06M__n_alap_1000__n_refined_5000'
U=20 #Volt-ban kifejezve
t=150 #sec-ban
reaction_zone=0  #diszkret ertekeket vehet fel; 0 ha NEM reakciozona, 1 ha IGEN 
x_old=0  #ez csak segitseg a reakciozona eldontesehez


f_result=open(DIR_w+FILE_RESULT, 'a')
f_add=open(DIR_add+FILE_ADD, 'r')

#f_result.write('UWH')

row_add=f_add.readlines() #a referencia fajl beolvasas
num_rows=len(row_add)

for row_index in range(num_rows):

	current_row=row_add[row_index]
	#itt meg kell nezni, h mi az elso karakter, a header
	if (current_row[0]=="x") | (current_row[0]=="\n"):
		#ilyenkor kihagyjuk az egeszet, header-t nem kell atmasolni
		print "BARCELONA???"
	else:
		values=current_row.split("\t") #visszaadott egy darab stringet szetbontja TAB-onkent
		index=len(values)
		values[index-1]=values[index-1].strip() #utolso tartalmaz egy ujsor jelet (\n), ezt ki kell szedni 

		new_row = range(index+4) # define an error list
		new_row[index]=description    #itt kell majd megadni a plusz ertekeket
		new_row[index+1]=U
		new_row[index+2]=t	

		for i in range(len(values)):
			values[i]=float(values[i])
			new_row[i]=values[i] #ertek at van masolva
		#el kell donteni, h ez most suru mesh-es zona-e vagy nem
		if x_old==0:		
			reaction_zone=0
		else:
			distance=values[0]-x_old
			if distance<0.0005:
				reaction_zone=1			
			else:
				reaction_zone=0
		
		x_old=values[0]		
		new_row[index+3]=reaction_zone

		for i in range(len(new_row)):
			f_result.write(str(new_row[i]))
			if i!=(len(new_row)-1):
				f_result.write('\t')
		f_result.write('\n')


#closing files
f_add.close()
f_result.close()


