import sys
#import os
import Adafruit_DHT
import greenH_actions
import sqlite3
from gpiozero import InputDevice
from gpiozero import LightSensor
from gpiozero import DistanceSensor
from time import sleep, strftime

# Sensores y asignación de pines
SENSOR_DHT = Adafruit_DHT.DHT11 # Sensor de temperatura y humedad
PIN_DHT = 17 #Pin asignado
senLuz= LightSensor(18) #Sensor de luz (fotorresistencia)
# Sensor ultrasonico (HC-SR04)
sensor = DistanceSensor(23, 24) #Pin 23 --> Echo, Pin 24 --> Trigger
# Sensor de humedad terrestre
hum = InputDevice(26)

# Variables globales a usar
ventStatus = 0 # Status del ventilador
wbStatus = 0 # Status de la bomba de agua
lpStatus = 0 # Status del sensor HC-SR04 
lslStatus = 0 # Status luces controladas por el sensor de luz
humedad,temperatura = -1.0,-1.0 # Humedad y temperatura del sensor DHT11
humTierra = 0 # Humedad sensor de humedad de tierra
primerMuestra = False
disInit = 0
crecimiento = 0.0
hr = "" # Hora de encendido/apagado luces
hora = int(strftime("%H"))
db = 'greenHouse.db'
regFlag = False

# Funciones
def medirHumedadTierra():
    global humTierra, wbStatus
    if hum.value == 0:
        humTierra = 0
        wbStatus = 0
    else:
        humTierra = 1
        wbStatus = 1
        greenH_actions.encenderWaterBomb()
        sleep(3)
        greenH_actions.apagarWaterBomb()
        wbStatus = 0

def leerTemperatura():
    global humedad, temperatura
    humedad, temperatura = Adafruit_DHT.read_retry(SENSOR_DHT, PIN_DHT)
    if humedad is None and temperatura is None:
        humedad, temperatura = 0, 0
        
def activarVentilador():
    global ventStatus
    if temperatura is not None and temperatura > 25.0:
        greenH_actions.encenderVentilador()
        ventStatus = 1
    elif temperatura is not None and temperatura <= 25.0:
        greenH_actions.apagarVentilador()
        ventStatus = 0
    else:
        ventStatus = 0

def monitorearLuz():
    global msgLuz, hora, hr
    hr = strftime("%H:%M")

    if hora in range(8,16) and senLuz.light_detected:
        greenH_actions.apagarLedSL()
        lslStatus = 0
    elif hora in range(8,16) and not senLuz.light_detected:
        greenH_actions.encenderLedSL()
        lslStatus = 1
    else:
        greenH_actions.apagarLedSL()
        lslStatus = 2

def obtenerPrimeraMuestra():
    global disInit, primerMuestra

    if primerMuestra == False:
        disInit = sensor.distance * 100
        primerMuestra = True

def sensarCrecimiento():
    global disInit, crecimiento
    distancia = sensor.distance * 100
    crecimiento = disInit - distancia
    greenH_actions.encenderLedProx()
    disInit = distancia
    greenH_actions.apagarLedProx()
    
    if distancia < 0.0:
        crecimiento = 0.0
    

def insertarRegistros():
    global regFlag
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS greenhouse")
    cur.execute("DROP TABLE IF EXISTS sensorsStatus")

    sql1 = '''CREATE TABLE greenhouse (humedad real, temperatura real, \
    humTierra real, crecimiento real, hora text)'''
    cur.execute(sql1)
    
    sql2 = '''CREATE TABLE sensorsStatus (motorStatus integer, waterStatus integer,\
    ledProxStatus integer, ledSLstatus integer)'''
    cur.execute(sql2)

    cur.execute("INSERT INTO greenhouse VALUES (?,?,?,?,?)",[humedad,temperatura,humTierra,crecimiento,hr])
    cur.execute("INSERT INTO sensorsStatus VALUES (?,?,?,?)",[ventStatus,wbStatus,lpStatus,lslStatus])
    conn.commit()
    conn.close()
    regFlag = False

def sincronizarRegistros():
    global ventStatus, wbStatus, lpStatus, lslStatus, regFlag
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql1 = '''SELECT * FROM sensorsStatus'''
    cur.execute(sql1)
    registros = cur.fetchone()
    ventStatus = registros[0]
    wbStatus = registros[1]
    lpStatus = registros[2]
    lslStatus = registros[3]
    conn.close()
    regFlag = True

def monitorearGH():
    while True:
        obtenerPrimeraMuestra()
        leerTemperatura()
        activarVentilador()
        medirHumedadTierra()
        monitorearLuz()
        sensarCrecimiento()
        insertarRegistros()

        if regFlag == False:
            sincronizarRegistros()
            print("Registros actualizados")

        sleep(120)

if __name__ == "__main__":
    monitorearGH()