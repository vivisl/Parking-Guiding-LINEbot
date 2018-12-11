'''
# if Flask version < 0.11.0
from flask.ext.cache import Cache
# if Flask version >= 0.11.0
from flask_cache import Cache

Flask==1.0.2
Flask-Cache==0.13.1
'''

from flask_caching import Cache
from datetime import timedelta
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)

# flask cache disable method 1:
cache = Cache(config={'CACHE_TYPE': 'redis'})
app.config["CACHE_TYPE"] = "null"
cache.init_app(app)

# flask cache disable method 2:
#app.config['DEBUG'] = True
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds = 1)


@app.route('/output/<path:path>')
def send_js(path):
    return send_from_directory('output', path)
@app.route('/getimg')
def getimg():
	return jsonify(
		imgpath='http://em2lab.comm.yzu.edu.tw:8080/js/ic_action_alarm.png',
		available='01,02,03'
		)

@app.route('/parking')
def parking():
	return jsonify(
		# output image with time
		imgpath1='http://140.138.178.69:5000/output/parking.jpg',
		# output image without time
		imgpath2='http://140.138.178.69:5000/output/parking_space_info.jpg',
		# output cameras image 
		imgpath3='http://140.138.178.69:5000/output/cameras.jpg',
		available='01,02,03'
		)


# output cameras image link
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
@app.route('/cameras')
def cameras():
    return '<img src="/output/cameras.jpg" alt="cameras.">'



if __name__ == "__main__":
    app.run(host='192.168.1.199', port=5000)

