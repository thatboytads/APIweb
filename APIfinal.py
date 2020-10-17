# Core Pkg
from flask import Flask,jsonify,make_response,abort,render_template
from livereload import Server


import json
import RPi.GPIO as GPIO
import time
# Init
pir_sensor2 = 13
pir_sensor = 11
piezo = 7


current_state = 0
current = 0
parked = 0
Message="right now who cares"
app = Flask(__name__)

# Using External Local Data
@app.route('/MotionPlease',methods=['GET'])
def index():
	message= Motion()
	return render_template("sensor.html",message=message)

def Motion():
	global current_state,current,parked,Message,piezo,pir_sensor,pir_sensor2
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pir_sensor2, GPIO.IN)
	GPIO.setup(piezo,GPIO.OUT)
	GPIO.setup(pir_sensor, GPIO.IN)

	try:
		while True:
			current_state = GPIO.input(pir_sensor)
			if current_state == 1 and parked == 0:
				time.sleep(1)
				print("are we parking")
				current_state=GPIO.input(pir_sensor)
				current_state2= GPIO.input(pir_sensor2)
				current = current_state + current_state2
				if current == 2:
					Message= "Car parked"
					print("welcome car")
					GPIO.output(piezo,True)
					print("ring")
					time.sleep(1)
					print("stop")
					GPIO.output(piezo,False)
					print("waiting for you to park")
					time.sleep(3)
					print("we done hey!!!!!!")
					parked = 1
					return Message
					continue
			current_state2= GPIO.input(pir_sensor2)
			if current_state2 == 1 and parked == 1:
				print("are you going?")
				time.sleep(1)
				current_state= GPIO.input(pir_sensor)
				current = current_state + current_state2
				if current == 2:
					Message= "Car not parked"
					print("don't go")
					GPIO.output(piezo,True)
					print("ring")
					time.sleep(1)
					print("stop")
					GPIO.output(piezo,False)
					print("waiting for you to go")
					time.sleep(3)
					print("see you next time")
					parked = 0
					return Message
					continue
	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()
@app.route('/')
def scan():
	return 'For the love of god work'

@app.route('/Motion',methods=['GET'])
def get_books():
	
	motion_out = [{"Motion Sensor string": Message}]
	return jsonify({"Motion sensor message":motion_out})




# Using JSONIFY ERROR
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}),404)

if __name__ == '__main__':
	server = Server(app.wsgi_app)
	server.serve(port=5000)

