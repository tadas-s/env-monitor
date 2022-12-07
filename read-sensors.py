from Adafruit_BME280 import *
import sqlite3

sensor = BME280(t_mode=4, p_mode=4, h_mode=4)

temperature = sensor.read_temperature()
pressure = sensor.read_pressure() / 100
humidity = sensor.read_humidity()

print("Temperature: %3.2f" % temperature)
print("Humidity: %3.2f" % humidity)
print("Pressure: %3.2f" % pressure)

con = sqlite3.connect("readings.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS readings(
        taken_at TIMESTAMP DEFAULT current_timestamp,
        temperature NUMERIC,
        humidity NUMERIC,
        pressure NUMERIC
    )
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS taken_at_date ON readings(DATE(taken_at))
""")

cur.execute("""
    INSERT INTO readings(temperature, humidity, pressure) VALUES(?, ?, ?)
""", (round(temperature, 2), round(humidity, 2), round(pressure, 2)))

# Remove records older than 6 months
cur.execute("""
    DELETE FROM readings
        WHERE DATE(taken_at) < DATE('now', 'start of month', '-5 month')
""")

con.commit()
con.close()
