import helperfunction
import csv

def fixitemno(s):
    while len(s) < 5:
        s = '0' + s
    return s

cursor, conn = helperfunction.connect_to_database('localhost','vinbud','postgres','postgres')



f=open('hilla.csv',encoding='utf8')

dread=csv.DictReader(f,delimiter=',')

data = []
for x in dread:
    data.append(x)
f.close()

#testing = set()
#for d in data:
 #   testing.add( (d['itemno'], d['itemcode'], d['baseunitofmeasure'], d['millilitrar'],d['soluflokkur'],d['vinstyrkur'],d['unitprice'],d['description']) )

numberofrowstoinsert = 2000
hilluplass=1
counter = 0

insertstring = "insert into hilluplass(bud,itemno,magn) values"
values = []

for d in data:
    print(d.keys())
    #if d['itemno'] != '':
    values.append (('Hafnarfjordur',fixitemno(d['itemno']),d['magn']))
    counter+=1

    if counter == numberofrowstoinsert:
        #print(values)
        args_str = b','.join(cursor.mogrify("(%s,%s,%s)", x) for x in values)
        cursor.execute(insertstring + args_str.decode('utf-8'))
        values = []
        counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s,%s,%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0


conn.commit()
cursor.close()
conn.close()