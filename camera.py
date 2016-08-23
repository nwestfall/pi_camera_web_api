from flask import Flask, request
import datetime as dt
import picamera
import os
import threading
import shutil

#Setup Flask App Server
app = Flask(__name__)

#Setup PiCamera
camera = picamera.PiCamera(resolution=(1280, 720), framerate=24)
camera.annotate_background = picamera.Color('black')
currentlyRecording = False

#Setup other settings
defaultLoc = "/var/www/vids/"

@app.route('/record', methods=['POST'])
def start_recording():
	#RECORD CAMERA
	global currentlyRecording
	if currentlyRecording == True:
		return "Already recording..."
	currentlyRecording = True
	record_thread = threading.Thread(target=record_in_background)
	record_thread.start()
	return "Recording..."

def record_in_background():
	cleanUp()
	while currentlyRecording:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:$M:%S')
                camera.start_recording(getFileName(), format='h264', quality = 20)
                start = dt.datetime.now()
                while ((dt.datetime.now() - start).days * 24 * 60) < 5 and currentlyRecording:
                        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        camera.wait_recording(0.5)
                camera.stop_recording()

@app.route('/home', methods=['POST'])
def stop_recording():
	global currentlyRecording
	currentlyRecording = False
	return "Stop recording..."

def getFileName():
	dir = defaultLoc + dt.datetime.now().strftime('%Y%m%d')
	if not os.path.exists(dir):
		os.makedirs(dir)
	return dir + '/' + dt.datetime.now().strftime('%Y%m%d%H%M%S') + '.h264'

def cleanUp():
	past = dt.datetime.now() - timedelta(days=-2)
	dir = defaultLoc + past.strftime('%Y%m%d')
	if os.path.exists(dir):
		shutil.rmtree(dir, ignore_errors=True)
	return

if __name__ == '__main__':
	app.run(host='10.1.1.27', port=9000)
