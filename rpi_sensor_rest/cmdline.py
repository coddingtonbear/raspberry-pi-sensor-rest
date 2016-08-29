import argparse

import Adafruit_DHT
from flask import Flask, jsonify
import RPIO


ARGS = None


app = Flask(__name__)


@app.route('/temperature')
def temperature():
    _, temperature = Adafruit_DHT.read_retry(
        Adafruit_DHT.DHT11,
        ARGS.dht11_pin,
        retries=3,
    )

    if temperature is None:
        raise Exception("No data received from device")

    return jsonify({
        'degrees_f': temperature * 1.8 + 32
    })


@app.route('/humidity')
def humidity():
    humidity, _ = Adafruit_DHT.read_retry(
        Adafruit_DHT.DHT11,
        ARGS.dht11_pin,
        retries=3,
    )

    if humidity is None:
        raise Exception("No data received from device")

    return jsonify({
        'perecent': humidity,
    })


def readADC(adcnum, clockpin, mosipin, misopin, cspin):
    ADC_BITS = {
        0: (0, 0, 1,),
        1: (1, 0, 1,),
        2: (0, 1, 0,),
        3: (1, 1, 0,),
    }

    RPIO.output(cspin, True)
    bits = [1]

    bits.extend(ADC_BITS[adcnum])
    bits.extend((0, 1, 1, 1, ))

    RPIO.output(cspin, False)     # bring CS low
    RPIO.output(clockpin, False)  # start clock low

    for bit in bits:
        RPIO.output(mosipin, bool(bit))
        RPIO.output(clockpin, True)
        RPIO.output(clockpin, False)

    time.sleep(0.1)

    input_bits = []
    for i in range(12):
        RPIO.output(clockpin, True)
        RPIO.output(clockpin, False)

        input_value = 0
        if (RPIO.input(misopin)):
            input_value = 1

        input_bits.append(input_value)

    RPIO.output(cspin, True)

    return float(int(''.join([str(v) for v in input_bits]), base=2)) / 4096


@app.route('/light')
def light():
    value = readADC(
        ARGS.adc_input_pin,
        ARGS.adc_clk_pin,
        ARGS.adc_mosi_pin,
        ARGS.adc_miso_pin,
        ARGS.adc_cs_pin,
    )

    return jsonify({
        'perecent': value,
    })


def main():
    global ARGS

    parser = argparse.ArgumentParser()
    parser.add_argument('--dht11-pin', default=None, type=int)
    parser.add_argument('--adc-input-pin', default=None, type=int)
    parser.add_argument('--adc-mosi-pin', default=None, type=int)
    parser.add_argument('--adc-miso-pin', default=None, type=int)
    parser.add_argument('--adc-clk-pin', default=None, type=int)
    parser.add_argument('--adc-cs-pin', default=None, type=int)
    args = parser.parse_args()

    if args.adc_input_pin is not None:
        RPIO.setmode(RPIO.BCM)
        RPIO.setup(args.adc_mosi_pin, RPIO.OUT)
        RPIO.setup(args.adc_miso_pin, RPIO.IN)
        RPIO.setup(args.adc_clk_pin, RPIO.OUT)
        RPIO.setup(args.adc_cs_pin, RPIO.OUT)

    ARGS = args

    app.run(host='0.0.0.0', port=6125)
