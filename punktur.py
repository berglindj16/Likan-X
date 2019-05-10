import matplotlib.pyplot as plt 
import helperfunction

cursor, conn = helperfunction.connect_to_database('localhost','atvr','postgres','tobbi')

f = open('Solution05.sol')
solution = f.readlines()
f.close()

items = "select hilluplass.itemno from voruspjald,hilluplass where itemcode ='05'and hilluplass.itemno = voruspjald.itemno order by hilluplass.itemno"
cursor.execute(items)
result = cursor.fetchall()

print(len(result))

fout = open('insertstatements.sql','w')
fout1 = open('insertstatements1.sql','w')
fout2 = open('insertstatements2.sql','w')
fout3 = open('insertstatements3.sql','w')
fout4 = open('insertstatements4.sql','w')

sumafylling=0
for t in solution:
    t = t.strip()
    if t.startswith('A'):
        tmp = t.replace(',',' ').replace('(',' ').replace(')',' ').split()
        fout.write("insert into ErAfylling (itemno, timeslot, erAfylling) values ('{}',{},{});\n".format(result[int(tmp[1])-1][0],tmp[2],tmp[3]))
        #if tmp[2] != '0':
    		#print('Áfylling á korteri {}, = {}'.format(tmp[1],tmp[2]))
    		#print('----------------------------------------')
    		#sumafylling=int(tmp[2])+sumafylling
    if t.startswith('B'):
        tmp = t.replace(',',' ').replace('(',' ').replace(')',' ').split()
        fout1.write("insert into afylling(timeslot, afylling) values ('{}',{});\n".format(tmp[1],tmp[2]))
        #if tmp[2] != '0':
            #print('Áfylling á korteri {}, = {}'.format(tmp[1],tmp[2]))
            #print('----------------------------------------')
            #sumafylling=int(tmp[2])+sumafylling
    if t.startswith('x'):
        tmp = t.replace(',',' ').replace('(',' ').replace(')',' ').split()
        fout2.write("insert into slott (itemno, slott) values ('{}',{});\n".format(result[int(tmp[1])-1][0],tmp[2]))
        	#if tmp[2] != '0':
        	#print('Vörunúmer {}, - slott =, {}'.format(tmp[1],tmp[2]))
        	#print('----------------------------------------')
    if t.startswith('y'):
        tmp = t.replace(',',' ').replace('(',' ').replace(')',' ').split()
        fout3.write("insert into birgdastada (itemno, timeslot, inventory) values ('{}',{},{});\n".format(result[int(tmp[1])-1][0],tmp[2],int(round(float(tmp[3])))))
    	#print('Vörunúmer {}, Birgðastaða á korteri {} ,= {}'.format(tmp[1],tmp[2],tmp[3]))
    	#print('----------------------------------------')
    if t.startswith('z'):
        tmp = t.replace(',',' ').replace('(',' ').replace(')',' ').split()
        fout4.write("insert into afylltMagn (itemno, timeslot, afylltmagn) values ('{}',{},{});\n".format(result[int(tmp[1])-1][0],tmp[2],(int(round(float(tmp[3]))))))
        #if tmp[3] != '0':
        	#print('Vörunúmer {}, áfyllt magn á korteri {} ,= {}'.format(tmp[1],tmp[2],tmp[3]))
        	#print('----------------------------------------')

fout.close()
fout1.close()
fout2.close()
fout3.close()
fout4.close()

#print('Heildarfjöldi áfyllinga: {}'.format(sumafylling))
#print('----------------------------------------')

