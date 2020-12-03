#PYTHON 2.7 script
#Keszitette: Koncz Viktoria
#2015. oktober 14.
#Feladata: Megjavitja a 20 V-os adatokat. Egy oszlopot kihagy.
#Eredmenyt CSV tipusu fajlba menti ki, ami konnyen megnyithato, nezgetheto, Mondrian, Statistica stb. tipusu szoftverrel.
######################################################################################

import math 

print "PYTHON scripts are easy"

#konyvtarnev, ahova irni kell
DIR_w='/home/vikik/Documents/Mondrian_DATAS/20_V/c_kcl_base_0.06M_jav/'   #PHYNDI
#konyvtarnev, ahonnan hozzafuzni kell
DIR_add='/home/vikik/Documents/Mondrian_DATAS/20_V/c_kcl_base_0.06M/' #PHYNDI
#ugyanez filenevekre
FILE_RESULT='expressions_20V_t_25s.csv'  #ez az eredmenyfajl neve
FILE_ADD= 'expressions_20V_t_25s.csv'  #ezt a fajlt fogja hozzafuzni


f_result=open(DIR_w+FILE_RESULT, 'w')
f_add=open(DIR_add+FILE_ADD, 'r')

#f_result.write('UWH')

row_add=f_add.readlines() #a referencia fajl beolvasas
num_rows=len(row_add)

shit=0

for row_index in range(num_rows):

	current_row=row_add[row_index]
	values=current_row.split("\t") #visszaadott egy darab stringet szetbontja TAB-onkent
	index=len(values)
	values[index-1]=values[index-1].strip() #utolso tartalmaz egy ujsor jelet (\n), ezt ki kell szedni 
	new_row = range(index-1)	
	
	for i in range(len(values)):

		if i<4:
			new_row[i]=values[i]
		elif (i==4):
			shit=shit+1
		else:
			new_row[i-1]=values[i]


	for i in range(len(new_row)):
		f_result.write(str(new_row[i]))
		if i!=(len(new_row)-1):
			f_result.write('\t')
	f_result.write('\n')

print str(shit)+'\n'

#closing files
f_add.close()
f_result.close()			




