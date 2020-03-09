import subprocess
from flask import Flask, jsonify
from flask_cors import CORS
import re
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
app = Flask(__name__)
CORS(app)


def get_temp_and_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        print("Failed to retrieve data from DHT22")
        return temperature, humidity


def get_board_temp():
    output = str(subprocess.check_output("/usr/bin/vcgencmd measure_temp", stderr=subprocess.STDOUT, shell=True))
    temperature = re.search(r'[0-9]+\.[0-9]+', output)
    return temperature.group()


def format_temp_and_humidity():
    temperatureValue, humidityValue = get_temp_and_humidity()
    return {
        'sensorsData':
            {'temperature': temperatureValue, 'humidity': humidityValue, 'boardCpuTemp': get_board_temp()}
    }


@app.route("/tempAndHumidity", methods=["GET"])
def get_temperature_and_humidity():
    return jsonify(format_temp_and_humidity())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
