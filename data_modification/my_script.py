import csv

print "PYTHON scripts are easy"

f_proba = open('proba.dat', 'r')
f_ref=open('proba_ref.dat','r')
f_results=open('error_calc.dat', 'w')

#write header
f_results.write('%Ez a proba!!! RSA safari\n')

#print f
row=f_proba.readlines()
current_row=row[12]
values=current_row.split("\t")
index=len(values)
print values[6]
values[index-1]=values[index-1].strip()
print values

for i in range(len(values)):
	values[i]=float(values[i])*3
print values
s=str(values)

for i in range(len(values)):
	f_results.write(str(values[i]))
	if i!=(len(values)-1):
		f_results.write('\t')
f_results.write('\n')


#proba='test string\n'
#print proba

#for line in f_proba:
#        print line,
	
		
#f_proba.read()

#closing files
f_proba.close()
f_ref.close()
f_results.close()
