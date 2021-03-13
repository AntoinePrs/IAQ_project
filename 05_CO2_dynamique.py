import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sgp30 import SGP30
import sys

sgp30 = SGP30()

#print("Sensor warming up, please wait...")
#def crude_progress_bar():
#    sys.stdout.write('.')
#    sys.stdout.flush()

#sgp30.start_measurement(crude_progress_bar)
#sys.stdout.write('\n')

2500*500/1000/60


# Parameters
x_len = 3000         # Number of points to display
y_range = [380, 1200]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys, linewidth=1.5)

# Add labels
plt.title('CO2 concentration')
plt.xlabel('Samples')
plt.ylabel('eCO2 (ppm)')

plt.axhline(y = 1000, color = 'r', linestyle = ':')
plt.axhline(y = 800, color = 'orange', linestyle = ':')
plt.axhline(y = 600, color = 'yellow', linestyle = ':') 

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read CO2 level
    eco2 = sgp30.command('measure_air_quality')[0]

    # Add y to list
    ys.append(eco2)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=500,
    blit=True)
plt.show()
