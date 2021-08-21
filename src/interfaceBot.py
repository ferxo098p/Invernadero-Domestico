#import sys
import telebot
import os
import greenH_actions

API_TOKEN = <ApiToken>

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, """\
Hola, soy Volleirei_bot. Estoy aquí para ayudarte, estos son los comandos de los que puedes hacer uso:\
\n\nstart -> Actualiza la información del invernadero, ejecute este comando cada 3 mins\
\n\ntemperatura->Obtiene la temperatura y humedad del invernadero.\
\n\ngrow -> Muestra cuanto han crecido las plantas. \
\n\nlight -> Muestra el estado de las luces del invernadero. \
\n\nfresh -> Enciende el ventilador en caso de estar apagado. \
\n\nnofresh -> Apaga el ventilador en caso de estar encendido. \
\n\nwet -> Enciende la bomba de agua en caso estar apagada durante tres segundos. \
\n\nearth -> Devuelve el estado de la tierra. \
\n\nlightup -> Enciende las luces en caso de estar apagadas. \
\n\nlightdown -> Apaga las luces en caso de estar encendidas.
""")

@bot.message_handler(commands=['start'])
def actualizar_Info(message):
    greenH_actions.actualizarStatus()
    bot.reply_to(message,"Información actualizada!!!")

@bot.message_handler(commands=['temperatura'])
def medir_Temp(message):
    humedad, temperatura = greenH_actions.getTemp_Hum()
    bot.reply_to(message,"""Temperatura = {0:0.1f} °C \
    \nHumedad = {1:0.1f}%""".format(humedad,temperatura))

@bot.message_handler(commands=['grow'])
def enviar_Crecimiento(message):
    crecimiento = greenH_actions.getCrecimientoPlantas()
    bot.reply_to(message, "Las plantas han crecido {0:0.1f} cm".format(crecimiento))

@bot.message_handler(commands=['light'])
def enviarEdoLuces(message):
    hora = greenH_actions.getHora()
    lightStaus = greenH_actions.getLedSlStatus()

    if lightStaus == 0:
        bot.reply_to(message,"""Son las {0} hrs, las luces se\
        encuentran apagadas""".format(hora))
    elif lightStaus == 1:
        bot.reply_to(message,"""Son las {0} hrs, y algo esta obstruyendo\
        la luz. Estas se encendieron""".format(hora))
    else:
        bot.reply_to(message,"Es de noche o madrugada, las luces permanecen apagadas")

@bot.message_handler(commands=['wet'])
def enviarEdoTierra(message):
    humT = greenH_actions.getWaterStatus()
    if humT == 0:
        bot.reply_to(message, "Regando las plantas")
        greenH_actions.setWaterStatus(1)
        greenH_actions.regarTierra()
        greenH_actions.setWaterStatus(0)
    else:
        bot.reply_to(message, "La bomba de agua ya esta encendida")
        

@bot.message_handler(commands=['fresh'])
def refrescar(message):
    statusFan = greenH_actions.getMotorStatus()
    if statusFan == 0:
        greenH_actions.encenderVentilador()
        greenH_actions.setMotorStatus(1)
        bot.reply_to(message, "Ventilador encendido")
    else:
        bot.reply_to(message, "El ventilador ya se encuentra encendido")

@bot.message_handler(commands=['nofresh'])
def apagarFan(message):
    statusFan = greenH_actions.getMotorStatus()
    if statusFan == 1:
        greenH_actions.apagarVentilador()
        greenH_actions.setMotorStatus(0)
        bot.reply_to(message, "Ventilador apagado")
    else:
        bot.reply_to(message, "El ventilador ya se encuentra apagado")

@bot.message_handler(commands=['earth'])
def regar(message):
    wetStatus = greenH_actions.getHumedadTierra()
    if wetStatus == 0:
        bot.reply_to(message, "La tierra esta humeda")
    else:
        bot.reply_to(message, "La tierra esta seca")

@bot.message_handler(commands=['lightup'])
def lightOn(message):
    lightSt = greenH_actions.getLedSlStatus()
    if lightSt == 0:
        greenH_actions.encenderLedSL()
        greenH_actions.setLedSlStatus(1)
        bot.reply_to(message, "Luces encendidas")
    else:
        bot.reply_to(message, "Las luces ya estan encendidas")

@bot.message_handler(commands=['lightdown'])
def lightOff(message):
    lightSt = greenH_actions.getLedSlStatus()
    if lightSt == 1:
        greenH_actions.apagarLedSL()
        greenH_actions.setLedSlStatus(0)
        bot.reply_to(message, "Luces apagadas")
    else:
        bot.reply_to(message, "Las luces ya estan apagadas")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling()
