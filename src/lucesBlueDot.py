import os
import psutil
from signal import pause, SIGKILL, SIGINT, SIGTERM
from bluedot import BlueDot
from time import sleep

# Canciones que se reproduciran dependiendo de la posición del boton que se presione 
songs = ('16bitGirl.mp3','FirstDrop.mp3','Caution_RadioEdit.mp3','QandA.mp3')
# Comando que inicia el show de luces
comando = 'sudo python3 /home/pi/lightshowpi/py/synchronized_lights.py --file=/home/pi/Music/' 
# Bandera que indica si se esta o no ejecutando el show de luces
status = False
# Bandera que indica la canción que se esta reproduciendo
sflag = 4

def controlLightShow(pos):
	"""
	Detecta la posición del botón de Blue Dot que se ha presionado y reproduce
	la comienza el show de luces con la asignación asignada a esa posición.

	Parameters:
		pos(bluedot): objeto de Blue Dot del cual se obtendrá la posición presionada.
	"""

	global status, sflag
	process = ''

	if status == True:
		# Verifica si no hay algún show de luces en curso
			stopLightShow(songs[sflag])
			#sleep(3)
	else:
		""" Sino hay un show de curso de luces en uso se inicia el correspondiente
		a esa posición"""
		if pos.top:
			process = comando + songs[0] + '&'
			os.system(process)
			sflag = 0
			print("Reproduciendo ",songs[0])
		elif pos.bottom:
			process = comando + songs[1] + '&'
			os.system(process)
			sflag = 1
			print("Reproduciendo ",songs[1])
		elif pos.left:
			process = comando + songs[2] + '&'
			os.system(process)
			sflag = 2
			print("Reproduciendo ",songs[2])
		elif pos.right:
			process = comando + songs[3] + '&'
			os.system(process)
			sflag = 3
			print("Reproduciendo ",songs[3])
		# Se actualiza la bandera indicando que hay un show de luces en curso
		status = True
		print("sflag:",sflag)

def stopLightShow(song):
	"""
	Detiene el show de luces en ejecución con la canción indicada.

	Parmeters:
		song(string): nombre del archivo mp3
	"""

	global status
	# Script de phyton que ejcuta el show de luces
	cmd = "/home/pi/lightshowpi/py/synchronized_lights.py"
	#cmd = Archivo mp3 con su ruta
	pcs = "--file=/home/pi/Music/" + song
	
	# Obtenemos todos los procesos que se encuentran ejecutando
	for process in psutil.process_iter():
		# Buscamos el proceso del show de luces
		if process.cmdline() == ["sudo","python3",cmd, pcs]:
			print("Deteniendo show de luces")
			print(process.pid)
			#Matamos a todos los procesos hijos
			for child in process.children(recursive=True):
				child.kill()
			process.kill() # Matamos al proceso padre
			status = False
	if status == True:
		print("Proceso no encontrado...")


blueD = BlueDot()
blueD.when_pressed = controlLightShow
pause()