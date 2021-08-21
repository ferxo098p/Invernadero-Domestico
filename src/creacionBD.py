import sqlite3

con = sqlite3.connect('greenHouse.db')

cursorObj = con.cursor()

sql1 = '''CREATE TABLE greenhouse (humedad real, temperatura real, \
humTierra real, crecimiento real, hora text)'''

cursorObj.execute(sql1)

sql2 = '''CREATE TABLE sensorsStatus (motorStatus integer, waterStatus integer,\
ledProxStatus integer, ledSLstatus integer)'''

cursorObj.execute(sql2)

con.close()

print("Base de datos creada exitosamente")