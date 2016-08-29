from flask import Flask, request
from config import Config
import datetime as dt
import picamera
import os
import threading
import shutil
import json
import decimal as d

#load in config file
cfg = Config(file('config.cfg'))

#Setup Flask App Server
app = Flask(__name__)

#Setup PiCamera
camera = picamera.PiCamera(resolution = (cfg.camera[0]["resolutionWidth"], cfg.camera[0]["resolutionHeight"]), framerate = cfg.camera[0]["framerate"])
camera.led = cfg.camera[0]["cameraLedDefaultOn"]
camera.annotate_background = picamera.Color('black')
currentlyRecording = False
lastRecordingDuration = 0

"""
When a post method is sent to /record, the system will start recording if it's not already
"""
@app.route('/record', methods = ['POST'])
def start_recording():
	global currentlyRecording
	if currentlyRecording:
		return buildJSON(msg = "Already Recording", error = True)
	currentlyRecording = True
	lastRecordingStart = dt.datetime.now()
	record_thread = threading.Thread(target = record_in_background)
	record_thread.start()
	return buildJSON(msg = "Started Recording")

"""
When a post method is sent to /home, the system wlll stop recording if it's not already
"""
@app.route('/home', methods = ['POST'])
def stop_recording():
	global currentlyRecording
	if currentlyRecording:
		currentlyRecording = False
		return buildJSON(msg = "Stopping recording")
	else:
		return buildJSON(msg = "System was not recording", error = True)

"""
Get the current status of the system
"""
@app.route('/status', methods = ['GET'])
def current_status():
	if currentlyRecording:
		return buildJSON(msg = "System is currently recording")
	else:
		return buildJSON(msg = "System is not recording")

"""
Get the last duraction of a recording
"""
@app.route('/lastduration', methods = ['GET'])
def last_recording_duration():
	if lastRecordingDuration == 0:
		return buildJSON(msg = "No recording has start yet", error = True)
	
	d.getcontext().prec = 2
	minute = 0
	second = 0
	if lastRecordingDuration < 0:
		second = int(lastRecordingDuration * 60)
	else:
		minute = int(lastRecordingDuration)
		second = int((lastRecordingDuration - minute) * 60)

	return buildJSON(msg = "Last recording was " + str(minute) + " minute(s) and " + str(second) + " second(s) long")

"""
function to run on a background thread to keep the recording and server running
"""
def record_in_background():
	global lastRecordingDuration
	cleanUp()
	actualstart = dt.datetime.now()
	while currentlyRecording:
		start = dt.datetime.now()
		camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		camera.start_recording(getFileName(), format = cfg.camera[0]["format"], quality = cfg.camera[0]["quality"])
		camera.led = False
		ledCount = 0
		while (d.Decimal((dt.datetime.now() - start).seconds) / d.Decimal(60)) < d.Decimal(cfg.file[0]["daysToKeep"]) and currentlyRecording:
			ledCount = ledCount + 1
			camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			camera.wait_recording(0.5)
			if ledCount % 3 == 0:
				camera.led = True
			else:
				camera.led = False
		camera.stop_recording()

	#save last duraction
	lastRecordingDuration = d.Decimal((dt.datetime.now() - actualstart).seconds) / d.Decimal(60)
	#turn light back to default status
	camera.led = cfg.camera[0]["cameraLedDefaultOn"]

"""
get file name for video file using timestamp
"""
def getFileName():
	directory = cfg.file[0]["defaultLocation"] + dt.datetime.now().strftime(cfg.file[0]["defaultFolderNameFormat"])
	if not os.path.exists(directory):
		os.makedirs(directory)
	return directory + '/' + dt.datetime.now().strftime(cfg.file[0]["defaultFileNameFormat"]) + '.' + cfg.camera[0]["format"]

"""
clean up old directories
"""
def cleanUp():
	past = dt.datetime.now() - dt.timedelta(days = cfg.file[0]["daysToKeep"])
	directory = cfg.file[0]["defaultLocation"] + past.strftime(cfg.file[0]["defaultFolderNameFormat"])
	if os.path.exists(directory):
		shutil.rmtree(directory, ignore_errors = True)
	return

"""
build JSON string for a response
"""
def buildJSON(msg, error = False):
	resp = {}
	if error:
		resp["status"] = "ERROR"
	else:
		resp["status"] = "OK"
	resp["message"] = msg
	return json.dumps(resp)

#Start server
if __name__ == '__main__':
	app.run(host = cfg.host[0]["host"], port = cfg.host[0]["port"])
