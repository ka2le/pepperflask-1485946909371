"""Cloud Foundry test"""
from flask import Flask
import cf_deployment_tracker
import os

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))


@app.route('/')
def hello_world():
    return 'Hello World! I am running on port ' + str(port)
	
@app.route('/<ip>/<port>/<text>', methods=['GET', 'POST', 'OPTIONS'])
def hello_world2(ip, port, text):
	#tts = ALProxy("ALTextToSpeech", str(ip), int(port))
	#tts.say(str(text))
	#execfile('pepperhello.py')
	return "connecting to "+ ip+":"+str(port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
