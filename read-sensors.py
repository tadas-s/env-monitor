from Adafruit_BME280 import *


sensor = BME280(t_mode=4, p_mode=4, h_mode=4)

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()

print("Temperature: %3.1f" % degrees)
print("Humidity: %3.1f" % humidity)

