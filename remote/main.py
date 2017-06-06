from flask import Flask, abort, request
from redis import Redis, RedisError
import os
import vlc

redis = Redis(host="redis", port=6379, db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

data = {"station_list":[]}

cur_station = None

def play_station(station):
    print("Playing", station['name'], "from url:\n", station['stream_url'])
    p = vlc.MediaPlayer(station['stream_url'])
    p.play()

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

@app.route("/api/station/")
def get_station_list():
    return "Stations, to be listed sd"

# Used for getting information about a station
@app.route('/api/station/<string:station_id>')
def show_station(station_id):
    return "Station {station_id}".format(station_id=station_id)

#Used for changing station, or pausing
@app.route('/api/current-station/', methods=['GET', 'POST'])
def current_station():
    global cur_station
    if request.method == 'POST':
        print("Test")
        stream_url = request.form['stream_url']
        name = request.form['name']
        new_station = {'name': name, 'stream_url': stream_url}
        play_station(new_station)
        cur_station = new_station
    return "Now playing...{station}".format(station="Nothing" if cur_station is None else cur_station['name'])



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
