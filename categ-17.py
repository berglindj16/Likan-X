import helperfunction

cursor, conn = helperfunction.connect_to_database('localhost','atvr','postgres','Regn4121')

outfile = open('data.dat','w')

current_hour = 11
current_minute = 0
max_hour = 18
time_steps = 60
slot = []
counter_time_steps = 0

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

timar = []
dags="""select distinct (dagsetning) from receipt where dagsetning > '2018-11-30' and dagsetning < '2019-01-13' order by dagsetning asc"""
cursor.execute(dags)
dagsetn = cursor.fetchall()


while current_hour < max_hour:
	timar.append( '{}:{}:00'.format(current_hour if current_hour >= 10 else '0' + str(current_hour), current_minute if current_minute >= 10 else '0' + str(current_minute)) )
	current_minute += time_steps
	while current_minute >= 60:
		current_hour += 1
		current_minute -= 60
timar.append( '{}:{}:00'.format(current_hour if current_hour >= 10 else '0' + str(current_hour), current_minute if current_minute >= 10 else '0' + str(current_minute)) )


items = "select hilluplass.itemno from voruspjald,hilluplass where itemcode ='17' and hilluplass.itemno = voruspjald.itemno order by hilluplass.itemno"
cursor.execute(items)
result = cursor.fetchall()

heild1 = 0
heild2 = 0
heild_hilluplass = """select sum(magn) from hilluplass, voruspjald where itemcode = '17' and hilluplass.itemno = voruspjald.itemno and voruspjald.millilitrar = '{}';"""


listi_ml = """select distinct(voruspjald.millilitrar) from voruspjald, hilluplass where itemcode = '17' and hilluplass.itemno = voruspjald.itemno group by millilitrar order by voruspjald.millilitrar"""
cursor.execute(listi_ml)
listi = cursor.fetchall()


#flaska = []
litilflaska = []
storflaska = []
for i in range(len(listi)):
	if listi[i][0] <= 500: 
		litilflaska.append(listi[i][0])
	else:
		storflaska.append(listi[i][0])
#	else:
#		flaska.append(listi[i][0])

#cursor.execute(heild_hilluplass.format(flaska[0]))
#heild = cursor.fetchall()
#print(flaska)
print(litilflaska)
print(storflaska)


for i in range(len(litilflaska)):
	cursor.execute(heild_hilluplass.format(litilflaska[i]))
	hilla1 = cursor.fetchall()
	heild1 = heild1 + hilla1[0][0]
for i in range(len(storflaska)):
	cursor.execute(heild_hilluplass.format(storflaska[i]))
	hilla2 = cursor.fetchall()
	try:
		int(hilla2[0][0])
		heild2 = heild2 + hilla2[0][0]
	except:
		pass

print('success!')

sell_items ="""select sum(-1*i.quantity),r.dagsetning from receipt r, receiptitems i, voruspjald v where r.receiptno = i.receiptno and i.itemno = v.itemno and i.itemno = '{}' and r.timasetning > '{}' and r.timasetning < '{}' and r.dagsetning = '{}' and v.itemcode = '17' group by r.dagsetning, r.timasetning order by r.dagsetning, r.timasetning"""
litrar = """select millilitrar from voruspjald where itemno = '{}';"""


C = 100; 
MaxSlots = int(heild1/8)+int(heild2/7);
MinSlots = 1;
M = 10000; 
T = len(dagsetn)*(len(timar)-1); 
V = len(result) #Vorunumer


outfile.write("param MaxSlots := {};\n".format(MaxSlots))
outfile.write("param MinSlots := {};\n".format(MinSlots))
outfile.write("param M := {};\n".format(M))
outfile.write("param T := {};\n".format(T))
outfile.write("param V := {};\n".format(V))

outfile.write("\n")

outfile.write("param C :=\n")
for a in range(len(dagsetn)*(len(timar)-1)):
	if a%7==0:
		C = 100
	if a%7 >= 0.5:
		C += 20
	outfile.write('{} {} \n'.format(a+1,C))

outfile.write(";\n")

outfile.write("param MPS :=\n")
for a in range(len(result)):
	cursor.execute( litrar.format( result[a][0] ))
	millilitrar = cursor.fetchall()
	if millilitrar[0][0] <= 500:
		MPS = 8
		outfile.write('{} {} \n'.format(a+1, MPS))
	else:
		MPS = 7
		outfile.write('{} {} \n'.format(a+1, MPS))

outfile.write(";\n")

outfile.write("param S :=\n")
for i in range(len(result)):
	if i % 10 == 0:
		print('.',end='', flush=True)

	for d in range(len(dagsetn)):
		for j in range(len(timar)-1):
			cursor.execute( sell_items.format( result[i][0], timar[j], timar[j+1], dagsetn[d][0]) )
			sell = cursor.fetchall()

			try:
				sala = int(sell[0][0])
			except:
				sala = 0
			outfile.write('{} {} {} \n'.format(i+1, j+1 + d*(len(timar)-1) ,sala))

	
outfile.write(";\nend;")

outfile.close()
