import helperfunction
import csv

def fixitemno(s):
    while len(s) < 5:
        s = '0' + s
    return s

cursor, conn = helperfunction.connect_to_database('localhost','vinbud','postgres','postgres')


f=open('ayflling.csv')

dread=csv.DictReader(f,delimiter=',')

data = []
for x in dread:
    data.append(x)
f.close()


numberofrowstoinsert = 2000
receiptitems=1
counter = 0


insertstring = "insert into receiptitems(receiptno,itemno,quantity,price,netprice,netamount,vatamount) values"
values = []

for i in data:

    if i['itemno'] != '':  
        values.append ((i['receiptno'],fixitemno(i['itemno']),i['quantity'],i['price'],i['netprice'],i['netamount'],i['vatamount']))
        counter+=1

    if counter == numberofrowstoinsert:
        #print(values)

        args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in values)
        cursor.execute(insertstring + args_str.decode('utf-8'))
        values = []
        counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0


conn.commit()
cursor.close()
conn.close()