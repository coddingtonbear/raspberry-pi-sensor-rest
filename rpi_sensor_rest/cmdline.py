import argparse

import Adafruit_DHT
from flask import Flask, jsonify


ARGS = None


app = Flask(__name__)


@app.route('/temperature')
def temperature():
    _, temperature = Adafruit_DHT.read_retry(
        Adafruit_DHT.DHT11,
        int(ARGS.dht11_pin),
    )

    return jsonify({
        'degrees_f': temperature * 1.8 + 32
    })


@app.route('/humidity')
def humidity():
    humidity, _ = Adafruit_DHT.read_retry(
        Adafruit_DHT.DHT11,
        int(ARGS.dht11_pin),
    )

    return jsonify({
        'perecent': humidity,
    })


def main():
    global ARGS

    parser = argparse.ArgumentParser()
    parser.add_argument('--dht11-pin', default=None)
    args = parser.parse_args()

    ARGS = args

    app.run(host='0.0.0.0', port=6125)
