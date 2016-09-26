# pi_camera_web_api
Control the Camera connected to a Raspberry pi through a web API

### Installation and usage

`git clone https://github.com/nwestfall/pi_camera_web_api.git`

### Notes

  * Requires Python `sudo apt-get install python2.7`
  * Requires Flask `pip install Flask`
  * Requires Picamera `sudo apt-get update && apt-get install python-picamera python3-picamera`
  
### How to Use
Once cloned onto your machine, `cd` into the directory.  Before you start the application for the first time, you will need to change the IP address in the 'config.cfg' file.  Under 'host' -> 'host' change '10.1.1.27' to the local IP address of your device.  If you wish to change more settings, please see the reference below.  To start the application, type `nohup python camera.py &` in the command line to run the application even when the command line isn't running.  By default, the application will be running on port '9000'.

### Available Settings
You can change the settings anytime in the 'config.cfg' file.  Make sure to restart the appliation after changing any settings.

|Main Namespace|Config Name            |Default Setting |Description                                                          |
|--------------|-----------------------|----------------|---------------------------------------------------------------------|
|host          |port                   |9000            |This is the port that the API will available from                    |
|              |host                   |'10.1.1.2'      |This is the local IP address of the machine                          |
|file          |defaultLocation        |'/var/www/vids/'|Location where video files will be stored (must end in '/')          |
|              |defaultFileNameFormat  |'%Y%m%d%H%M%S'  |File name format for video files (must be in a valid date format) [reference](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)|
|              |defaultFolderNameFormat|'%Y%m%d'        |File name format for folders (must be in a valid date format) [reference](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)|
|              |minutesPerFile         |5               |This number has to do with your RAM and SD card IO.  If the size is too large, the application may crash due to IO problems |
|              |daysToKeep             |2               |Set the number of days you want to keep vidoe footage for.  Take into consideration how many hours a day you plan to have the device recording and how large your SD card is |
|camera        |quality                |20              |Set the quality of the video being recorded [reference](http://photo.net/learn/jpeg/#qual) |
|              |framerate              |24              |Set the framerate for the video being recorded                       |
|              |format                 |'h264'          |Set for video format you want to record in [reference](http://picamera.readthedocs.io/en/release-1.12/api_encoders.html#piencoder) |
|              |cameraLedDefaultOn     |True            |Control whether the camera LED is on/off by default                  |
|              |resolutionWidth        |1280            |Set the resolution width of what you are recording                   |
|              |resolutionHeight       |720             |Set the resolution height of what you are recording                  |
