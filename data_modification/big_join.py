#PYTHON 2.7 script
#Keszitette: Koncz Viktoria
#2015. oktober. 5.
#Feladata: TXT adatfajlok egyesitese. Osszejoinol-ja a MESH experimentnel keletkezo tablakat. Egy MESH beallitast kulon kezel.
#Eredmenyt CSV tipusu fajlba menti ki, ami konnyen megnyithato, nezgetheto, Mondrian, Statistica stb. tipusu szoftverrel. Egyes mesh setting-ek
######################################################################################

import math 

print "PYTHON scripts are easy"

#konyvtarnev, ahova irni kell (eredmeny)
DIR_result='/home/vikik/Documents/statistica_python/'   #PHYNDI
#konyvtarnev, ahonnan olvasni kell
DIR_solution='/home/vikik/Documents/statistica_python/' #PHYNDI
DIR_diff='/home/vikik/Documents/statistica_python/' 
DIR_error='/home/vikik/Documents/statistica_python/'
DIR_expr='/home/vikik/Documents/statistica_python/'
#ugyanez filenevekre
FILE_RESULT='mesh_exp.dat'  #ide lesz osszejoin-olva
FILE_SOLUTION= 'sol.dat'  #ez az eredmenyfajl
FILE_DIFF='diff.dat'	#ez a szamitott differencia fajl	
FILE_ERROR='error.dat'	#ez a szamitott hibafajl
FILE_EXPR='expr.dat'	#ez a 'deszkriptorok' fajlja

f_result=open(DIR_result+FILE_RESULT, 'w')
f_solution=open(DIR_solution+FILE_SOLUTION, 'r')
f_diff=open(DIR_diff+FILE_DIFF, 'r')
f_error=open(DIR_error+FILE_ERROR, 'r')
f_expr=open(DIR_expr+FILE_EXPR, 'r')

row_solution=f_solution.readlines() #a solution fajl beolvasas
row_diff=f_diff.readlines() #a differencia fajl beolvasas
row_error=f_error.readlines() #az error fajl beolvasas
row_expr=f_expr.readlines() #az expression fajl beolvasas

num_solution=len(row_solution)
num_diff=len(row_diff)
num_error=len(row_error)
num_expr=len(row_expr)

# hasonlitsuk ossze
if ((num_solution!=num_diff) | (num_solution!=num_error)) | (num_solution!=num_expr):
	print "ERROR happaned. Check the headers of the comparable files. Something is missing maybe."
	print str(num_solution)+'\n'
	print str(num_diff)+'\n'
	print str(num_error)+'\n'
	print str(num_expr)+'\n'
	exit()

#WRITE HEADER of the file


t=-1  #Time

for row_index in range(num_solution):
	
	current_solution=row_solution[row_index]
	current_diff=row_diff[row_index]
	current_error=row_error[row_index]
	current_expr=row_expr[row_index]

	if (current_solution[0]=="%"):	# 't' must be figured out, ???FINITO???
		if (current_solution[1]!="F"):
			if (current_solution[1]!="c"):
				row=current_solution.split("\t")
				time=row[0].split("=")
				t=time[1]

	elif (current_solution[0]=="\n"):
		print "BARCELONA???"
	else:
		values_solution=current_solution.split("\t") #visszaadott egy darab stringet szetbontja TAB-onkent
		values_diff=current_diff.split("\t")
		values_error=current_error.split("\t")
		values_expr=current_expr.split("\t")		

		index_solution=len(values_solution)
		#utolso tartalmaz egy ujsor jelet(\n), ezt ki kell szedni
		values_solution[index_solution-1]=values_solution[index_solution-1].strip()  
		index_diff=len(values_diff)	
		values_diff[index_diff-1]=values_diff[index_diff-1].strip()
		index_error=len(values_error)
		values_error[index_error-1]=values_error[index_error-1].strip()
		index_expr=len(values_expr)
		values_expr[index_expr-1]=values_expr[index_expr-1].strip()

		big_length=index_solution+index_diff+index_error+index_expr
		big_row=range(big_length)  #itt majd pontosan ki kell szamolni, h hanyra van szukseg

		for i in range(index_solution):
			values_solution[i]=float(values_solution[i])
			big_row[i]=values_solution[i] #ertek at van masolva

		for i in range(index_diff):
			values_diff[i]=float(values_diff[i])
			big_row[i+index_solution]=values_diff[i]

		for i in range(index_error):
			values_error[i]=float(values_error[i])
			big_row[i+index_diff]=values_error[i]
		
		for i in range(index_expr):
			values_expr[i]=float(values_expr[i])
			big_row[i+index_error]=values_expr[i]

		big_row[big_length-1]=t

		for i in range(len(big_row)):
			f_result.write(str(big_row[i]))
			if i!=(len(big_row)-1):
				f_result.write('\t')
		f_result.write('\n')


#closing files
f_result.close()
f_solution.close()
f_diff.close()
f_error.close()
f_expr.close()
