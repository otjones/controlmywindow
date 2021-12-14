# controlmywindow
A project to control my living room window and collect and analyse air quality and weather data

Source code split into:
-----------------------
Server - code to run on the Raspberry Pi  
Client - code hosted to run the dashboard on controlmywindow.co.uk  
Analysis - scripts to  estimate database size and perform data analysis  

3D STL files for actuator assembly included   

Demonstration video:
--------------------
https://youtu.be/NgbbmP9EjUA

Description of all source files
===============================

/server/src/ST7735  - libraries for LCD display  
/server/src/bme280  - libraries for air quality sensor  
/server/src/fonts...  - font files for LCD display  
/server/src/i2cdevice  - I2C libraries for communication with Enviroboard from Raspberr Pi
/server/src/app.js  - main Node.js file for hosting the server and handling requests
/server/src/endStop.py  - watches microswitches and stoppes the motor when triggered. Is spawned by app.js and runs continuously
/server/src/messageServer.py  - hosts a localhost webserver to control the LCD display. Accepts /message/<body> requests from app.js
/server/src/motorBACKWARD.py  - sets motor to turn in one direction indefinitely (until stopped by another command)
/server/src/motorFORWARD.py  - same as above in reverse direction
/server/src/motorSTOP.py  - stops the motor
/server/src/weather.py  - reads the sensor data from the Pimoroni Enviro board and prints the result, spawned and read by worker.js
/server/src/worker.js  - file of Javascript functions written to carry out repeatable tasks, called from app.js

/client/css/  - CSS files generated by Webflow
/client/images/  - favicon and webclip image files
/client/js/  - Javascript files generated by Webflow (for UI interactions such as hover effects on buttons)
/client/index.html  - main page for the dashboard, mix of Webflow generated HTML and custom HTML, including custom form for sending messages to LCD screen
/client/script.js  - Custom Javascript file with functions for plotting all graphs, sending motor control requests (onCLick) and getting the window status (on page load)

/analysis/insights.py  - script for running a CLI in a terminal to interactively plot data, plot the derivative of the data, print out temperature drop events, humidity spike events, and a routine for testing any two datasets for the sample Pearson's correlation coefficient
/analysis/jsonSize.py  - the script used for estimating the database size
  
/gear.STL  - Gear used in assembly
/pinion.STL  - Pinion used in assembly. A right angled bracket was also stuck to the side of the pinion to actuate end stop switch
/window.STL  - Main window mount clips over window frame and locks into place over the protrusion (shown in video)

Parts list
==========
  
Motor - 
Motor driver - 
Microswitches x2 - 
Raspberry Pi 4 Model B - 
Pimoroni Enviro Board - 
Power supply (15v 1.5A) with step down to 12v and split to motor voltage of motor driver and another step down to 5v USB 3A

ngrok for Linux - 
