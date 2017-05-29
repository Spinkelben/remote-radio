from flask import Flask, abort
from redis import Redis, RedisError
import os
import socket

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

data = {"station_list":[]}

@app.route('/')
def hello_world():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}</br>" \
	   "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

@app.route("/station/")
def get_station_list():
    return "Stations"

# Used for getting information about a station
@app.route('/station/<int:station_id>')
def show_station(station_id):
    return "Station {station_id}".format(station_id=station_id)

#Used for changing station, or pausing
@app.route('/current-station/')
def current_station():
    return "Now playing..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

