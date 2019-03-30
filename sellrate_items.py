import helperfunction

cursor, conn = helperfunction.connect_to_database('localhost','vinbud','postgres','postgres')

#------------------------SETTINGS---------------------
current_hour = 9
current_minute = 0
max_hour = 18

time_steps = 60

s_items = """select sum(-1*i.quantity)
from receiptitems i, receipt r
where i.receiptno = r.receiptno
and i.itemno in ({})
and r.timasetning > '{}' and r.timasetning < '{}'
and to_char(r.dagsetning, 'day') like '{}%';"""

s_count_days = """select count(DISTINCT dagsetning)
from receipt
where to_char(dagsetning, 'day') like '{}%';"""


days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

timar = []
while current_hour < max_hour:
    timar.append( '{}:{}:00'.format(current_hour if current_hour >= 10 else '0' + str(current_hour), current_minute if current_minute >= 10 else '0' + str(current_minute)) )
    current_minute += time_steps
    while current_minute >= 60:
        current_hour += 1
        current_minute -= 60
timar.append( '{}:{}:00'.format(current_hour if current_hour >= 10 else '0' + str(current_hour), current_minute if current_minute >= 10 else '0' + str(current_minute)) )


#------------------------------------------------THE MAIN PART------------------------------------------
ipa_beers = "22988,24689,23968,23550,22827,24191,23717,21751,22901,23984,23916,01719,24376,23793,16671,24073,23839,21100,22681,24100,01466,24072,24377,21297,20318,24284,22026,24444,24349,23130,23129,21124,22307"


items = ','.join(["'{}'".format(s) for s in ipa_beers.split(',')])

sellcount = {}
for d in days:
    sellcount[d] = [0 for _ in timar]
    cursor.execute( s_count_days.format(d) )
    numberofdays = cursor.fetchall()

    for t in range(len(timar)-1):
        cursor.execute( s_items.format( items, timar[t], timar[t+1], d ) )
        result = cursor.fetchall()

        try:
            int(result[0][0])
            sellcount[d][t] = result[0][0]/numberofdays[0][0]
        except:
            pass


#-----------------------------------------SHOWING THE RESULTS----------------------------

print('Title: IPA Beers')
print('------------------------------')
for d in days:
    print(d)
    for t in timar:
        print(t[:-3],end='\t')
    print('')
    for t in range(len(timar)):
        print(int(sellcount[d][t]+0.5),end='\t')
    print('\n------------------------------')

cursor.close()
conn.close()
