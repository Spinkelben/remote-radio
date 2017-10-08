from flask import Flask, abort, request, jsonify
from redis import Redis, RedisError
from message_pb2 import Request, Response
import os
import socket
import logging
import json

redis = Redis(host="redis", port=6379, db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


def play_station(station):
    logging.debug("Sending change station request")
    request_message = Request()
    request_message.type = Request.SET_CHANNEL
    request_message.channel = station['stream_url']
    radio_answer = _send_message_to_radio(request_message)
    logging.debug("Playing", station['name'], "from url:\n", station['stream_url'])
    return radio_answer.success


def get_info():
    logging.debug("Sending get info request")
    info_request = Request()
    info_request.type = Request.INFO
    info_answer = _send_message_to_radio(info_request)
    return {
        "success": True,
        "station_info": {
            "name": info_answer.name,
            "stream_url": None,
            "bitrate": info_answer.bitrate,
            "codec": info_answer.codec,
            "title": info_answer.title,
            "location": info_answer.location,
            "extra": json.loads(info_answer.extra) if info_answer.extra else None,
            "stereo": info_answer.stereo
        }
    }


def _send_message_to_radio(request_message):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/var/sockets/radio-sock')
    s.send(request_message.SerializeToString())
    s.shutdown(socket.SHUT_WR)

    response_message = []
    while True:
        data = s.recv(4096)
        if not data: break
        response_message.append(data)
    s.close()

    response = Response()
    response.ParseFromString(b''.join(response_message))
    return response


# Used for changing station, or pausing
@app.route('/api/station/', methods=['GET', 'POST'])
def current_station():
    if request.method == 'GET':
        return jsonify(get_info())

    elif request.method == 'POST':
        logging.debug("Recieved POST request")
        stream_url = request.form['stream_url']
        name = request.form['name']
        new_station = {'name': name, 'stream_url': stream_url}
        success = play_station(new_station)
        logging.info("Station changed successfully = {}".format(success))
        new_station['bitrate'] = None
        new_station['codec'] = None
        response = {
            "success": success,
            "station_info": new_station
        }
        return jsonify(response)

@app.route('/api/stop', methods=["GET"])
def stop_playing():
    stop_request = Request()
    stop_request.type = Request.STOP
    answer = _send_message_to_radio(stop_request)
    logging.debug("Stop request sent")
    return jsonify(answer.success)

@app.route('/api/start', methods=["GET"])
def start_playing():
    start_request = Request()
    start_request.type = Request.PLAY
    answer = _send_message_to_radio(start_request)
    logging.debug("Start request sent")
    return jsonify(answer.success)

@app.route('/api/pause', methods=["GET"])
def pause_playing():
    pause_request = Request()
    pause_request.type = Request.STOP
    answer = _send_message_to_radio(pause_request)
    logging.debug("Pause request sent")
    return jsonify(answer.success)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=80, debug=True)
