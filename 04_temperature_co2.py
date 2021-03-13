import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import time
import sys
import bme680
from sgp30 import SGP30


# Intialise temperature sensor
sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Intialise eCO2 sensor
sgp30 = SGP30()

#print("Sensor warming up, please wait...")
#def crude_progress_bar():
#    sys.stdout.write('.')
#    sys.stdout.flush()

#sgp30.start_measurement(crude_progress_bar)
#sys.stdout.write('\n')


# Name variables to append
xs = []
y1s = []
y2s = []

# Explicitly create our figure and subplots
#fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

############

def animate(i, xs, y1s, y2s):

    #ax1.clear()
    #ax2.clear()

    # Read temperature (Celsius)
    sensor.get_sensor_data()
    temp_c = round(sensor.data.temperature, 2)
    
    # Read eCO2 level
    eco2 = sgp30.command('measure_air_quality')[0]
    
    # Append y's lists
    y1s.append(temp_c)
    y2s.append(eco2)

    # Add x to list
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    y1s = y1s[-20:]
    y2s = y2s[-20:]
    
    #for label in ax2.xaxis.get_ticklabels()[::10]:
    #    label.set_visible(False)

    # Draw x and y lists
    ax1.plot(xs, y1s, 'blue')
    ax2.plot(xs, y2s, 'green')
    
    # Add horizontal lines for CO2 graph
    #ax2.hlines(y=1000,colors="r--")
   

    # Format plot
    ax1.tick_params(bottom=False,
                    labelbottom=False)
    ax1.set_title('Température')
    ax1.set_ylabel('Degrés (°C)')
    ax2.set_title('Equivalent CO2')
    ax2.set_ylabel('ppm')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2, hspace=0.2)
    ax1.set_ylim([15,30])
    ax2.set_ylim([380,1200])
    



# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, y1s, y2s), interval=1000)
plt.show()


