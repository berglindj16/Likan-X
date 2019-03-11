import helperfunction
import csv

cursor, conn = helperfunction.connect_to_database('localhost','vinbud','postgres','postgres')


f=open('afi.csv')

dread=csv.DictReader(f,delimiter=',')

data = []
for x in dread:
    data.append(x)

f.close()

baskets = set()
for d in data:
    baskets.add( (d['receiptno'], d['posterminalno'], d['timasetning'], d['date']) )



numberofrowstoinsert = 2000
counter = 0


insertstring = "insert into receipt(receiptno, posterminalno, timasetning, dagsetning) values"
receipt = 1
values = []

for i in baskets:
    values.append ((i[0],i[1],i[2],i[3]))
    counter+=1

    if counter == numberofrowstoinsert:
        #print(i.keys())
        #print(values)
        args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s)", x) for x in values)
        cursor.execute(insertstring + args_str.decode('utf-8'))
        values = []
        counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0


conn.commit()
cursor.close()
conn.close()