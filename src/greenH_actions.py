import sqlite3
from gpiozero import LED
from gpiozero import Motor
from time import sleep

# Actuadores
vent = LED(27) # Ventilador
water = Motor(forward=5, backward=6) # Bomba de agua
ledProx = LED(25) # Led sensro HC-SR04
ledSL = LED(16) # Barra de LEDs

# Variables globales
statuss = ()
info = ()
db = 'greenHouse.db'

# Funciones
def encenderLedSL():
    ledSL.on()

def apagarLedSL():
    ledSL.off()

def encenderLedProx():
    ledProx.on()

def apagarLedProx():
    ledProx.off()

def encenderVentilador():
    vent.on()

def apagarVentilador():
    vent.off()

def encenderWaterBomb():
    water.forward()

def apagarWaterBomb():
    water.stop()

def getTemp_Hum():
    return info[0], info[1]

def getHumedadTierra():
    return info[2]

def getCrecimientoPlantas():
    return info[3]

def getHora():
    return info[4]

def getMotorStatus():
    return statuss[0]

def getWaterStatus():
    return statuss[1]

def getLedProxStatus():
    return statuss[2]

def getLedSlStatus():
    return statuss[3]

def setLedSlStatus(status):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("UPDATE sensorsStatus SET ledSLstatus = ?",[status])
    conn.commit()
    print("Estado luces actualizado")
    conn.close()

def setMotorStatus(status):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("UPDATE sensorsStatus SET motorStatus  = ?",[status])
    conn.commit()
    print("Estado ventilador actualizado")
    conn.close()

def setWaterStatus(status):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("UPDATE sensorsStatus SET waterStatus  = ?",[status])
    conn.commit()
    print("Estado bomba de agua actualizado")
    conn.close()

def regarTierra():
    encenderWaterBomb()
    sleep(3)
    apagarWaterBomb()

def actualizarStatus():
    global statuss, info
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql1 = '''SELECT * from sensorsStatus'''
    cur.execute(sql1)
    statuss = cur.fetchone()
    #sensorsStatus (motorStatus integer, waterStatus integer,ledProxStatus integer, ledSLstatus integer)

    print(statuss)

    sql2 = '''SELECT * from greenhouse'''
    cur.execute(sql2)
    info = cur.fetchone()
    #greenhouse (humedad real,temperatura real,humTierra real, crecimiento real,hora text)
    
    print(info)

    conn.close()