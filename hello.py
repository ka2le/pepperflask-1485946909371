"""Cloud Foundry test"""
from flask import Flask
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import cf_deployment_tracker
import os

#from importlib.machinery import SourceFileLoader
#naoqi = SourceFileLoader("ALProxy", "naoqipythonlib/naoqi.py").load_module()
import imp
#qi = imp.load_source("", "naoqipythonlib/qi/qi.py")
#foo = imp.load_source('ALProxy', 'naoqipythonlib/naoqi.py')
naoqi = imp.load_source('ALProxy', 'naoqipythonlib/naoqi.py')
#from naoqipythonlib/naoqi.py import ALProxy

# Emit Bluemix deployment event
cf_deployment_tracker.track()





def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator






app = Flask(__name__)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))


@app.route('/')
@crossdomain(origin='*')
def hello_world():
    return 'Hello World! I am running on port ' + str(port)
	
@app.route('/<ip>/<port>/<text>', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
def hello_world2(ip, port, text):
	tts = naoqi.ALProxy("ALTextToSpeech", str(ip), int(port))
	tts.say(str(text))
	#execfile('pepperhello.py')
	return "connecting to "+ ip+":"+str(port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
