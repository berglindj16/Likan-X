import helperfunction

cursor, conn = helperfunction.connect_to_database('localhost','vinbud','postgres','postgres')

#numer = input('itemno: ')

s="""select description, quantity, timasetning, dagsetning 
from manuhvit
where itemno = %s
and timasetning < %s and timasetning > %s
order by dagsetning, timasetning ;"""

vorunumer = ('20410')

timar = ['12:00:00','13:00:00']
#'14:00:00','15:00:00','16:00:00']
result = [0 for _ in timar]

for t in range(len(timar)-1):
	values=[vorunumer,timar[t], timar[t+1]]

	query=cursor.mogrify(s,values)

	#print('The query is: "{}"'.format(query))

	cursor.execute(query)

	records=cursor.fetchall()

	for i in records:
		print(i[0],i[1],i[2],i[3])
		result[t] += int(i[1])

for r in result:
	print(r)

conn.commit()
cursor.close()
conn.close()

#,'20410','10408'