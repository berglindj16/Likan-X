import helperfunction

cursor, conn = helperfunction.connect_to_database('localhost','atvr_h2','postgres','postgres')
#cursor, conn = helperfunction.connect_to_database('localhost','vinbud','postgres','postgres')

#------------------------SETTINGS---------------------
current_hour = 8
current_minute = 0
max_hour = 17

time_steps = 60

#------------------------SETTINGS---------------------

s_code = """select sum(-1*i.quantity)
from receiptitems i, receipt r, voruspjald v, itemcategorycode c
where i.receiptno = r.receiptno
and i.itemno = v.itemno
and v.itemcode = c.itemcode
and c.itemcode = '{}'
and r.timasetning >= '{}' and r.timasetning <= '{}'
and to_char(r.dagsetning, 'day') like '{}%';"""

s_count_days = """select count(DISTINCT dagsetning)
from receipt
where to_char(dagsetning, 'day') like '{}%';"""

s_get_codes = """select c.itemcode, c.description, sum(-1*i.quantity)
from receiptitems i, voruspjald v, itemcategorycode c
where i.itemno = v.itemno
and v.itemcode = c.itemcode
group by c.itemcode, c.description
having sum(-1*i.quantity) >= 0
order by sum(-1*i.quantity) desc;"""


timar = []
while current_hour < max_hour:
    timar.append( '{}:{}:00'.format(current_hour if current_hour >= 10 else '0' + str(current_hour), current_minute if current_minute >= 10 else '0' + str(current_minute)) )
    current_minute += time_steps
    while current_minute >= 60:
        current_hour += 1
        current_minute -= 60
timar.append( '{}:{}:00'.format(current_hour if current_hour >= 10 else '0' + str(current_hour), current_minute if current_minute >= 10 else '0' + str(current_minute)) )

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

cursor.execute(s_get_codes)
the_codes = cursor.fetchall()


sellcount = {}

for c in the_codes:
    sellcount[c] = {}
    for d in days:
        sellcount[c][d] = [0 for _ in timar]
        cursor.execute( s_count_days.format(d) )

        numberofdays = cursor.fetchall()

        print('.',end='')
        for t in range(len(timar)-1):
            cursor.execute( s_code.format( c[0], timar[t], timar[t+1], d ) )
            result = cursor.fetchall()

            try:
                int(result[0][0])
                sellcount[c][d][t] = result[0][0]/numberofdays[0][0]
            except:
                pass
print('')

#--------------------------------USE THE SELLCOUNT DICT TO DO SOMETHING CLEVER!
for c,v in sellcount.items():
    print('Category: {} ({})'.format(c[0],c[1]))
    print('------------------------------')
    for d in days:
        print(d)
        for t in timar:
            print(t[:-3],end='\t')
        print('')
        for t in range(len(timar)):
            print(int(v[d][t]+0.5),end='\t')
        print('\n------------------------------')
    print('')

cursor.close()
conn.close()
