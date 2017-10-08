from flask import Flask, abort, request, jsonify, render_template, url_for, redirect
import logging
import requests

app = Flask(__name__)

@app.route('/', methods=["GET"])
def root():
    response = requests.get("http://web-api:8080/api/station/")
    context = response.json()
    return render_template("index.html", success=context['success'], station_info=context['station_info'])

@app.route('/change', methods=['POST'])
def change_station():
    logging.info("POST")
    print("POST")
    response = requests.post('http://web-api:8080/api/station/', data=request.form)
    if response.ok:
        return redirect(url_for('root'))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=80, debug=True)
