import sqlite3
from pathlib import Path
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from dateutil.parser import parse as parse_date

class Plot:
    def __init__(self, month):
        self.month = month
        self.timestamps = []
        self.temperatures = []
        self.humidities = []
        self.pressures = []

    def add_reading(self, taken_at, temperature, humidity, pressure):
        self.timestamps.append(parse_date(taken_at))
        self.temperatures.append(temperature)
        self.humidities.append(humidity)
        self.pressures.append(pressure)

    def plot(self):
        plt.clf()

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_title("Environmental data for %s" % self.month)

        # configure x ticks
        # TODO

        l1, = ax1.plot_date(self.timestamps, self.temperatures, '-', label="Temperature", color='r')

        ax2 = ax1.twinx()
        ax2.set_ylabel("Humidity")
        l2, = ax2.plot_date(self.timestamps, self.humidities, '-', label="Humidity", color='b')

        # Format the x-axis for dates (label formatting, rotation)
        fig.autofmt_xdate(rotation=60)
        fig.tight_layout()

        # Show grids and legends
        ax1.grid(True)
        ax2.legend([l1, l2], ['Temperature', 'Humidity'], framealpha=0.9)

        plt.savefig("%s.png" % self.month.lower())

matplotlib.use('agg')

con = sqlite3.connect(Path(__file__).parent.absolute().joinpath("readings.db"))
cur = con.cursor()

query = cur.execute("""
    SELECT taken_at, temperature, humidity, pressure FROM readings
    ORDER BY taken_at
""")

plot = None

for row in query:
    row_month = datetime.fromisoformat(row[0]).strftime('%B')

    if plot is None:
        plot = Plot(row_month)

    if plot.month != row_month:
        # Output the current plot
        plot.plot()

        # Start a new one
        plot = Plot(row_month)

    plot.add_reading(taken_at = row[0], temperature = row[1], humidity = row[2], pressure = row[3])

plot.plot()

con.close()
