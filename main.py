from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
import re
from datetime import datetime

# Reading File
with open('data.txt', 'r') as file:
    data = file.read()

# Regular Expression to find all timestamps and bitrates
reg = r"Timestamp:\s*([0-9\-]+\s+[0-9:]+).*?\[\s\s\d\]\s+[0-9]*\.[0-9]+-[0-9]*\.[0-9]+\s+sec\s+[\d\.]+\s+\w+Bytes\s+([\d\.]+)\s+(Mbits|Kbits)\/sec.*?sender"
matches = re.findall(reg, data, re.S)

timestamps = []
bitrates = []

for timestamp, value, unit in matches:
    # Convert timestamp to datetime object
    dt = datetime.strptime(timestamp.strip(), '%Y-%m-%d %H:%M:%S')
    timestamps.append(dt)
    
    # Convert bitrate to float and adjust based on unit
    if unit == 'Kbits':
        bitrates.append(float(value) / 1000.0)  # Convert Kbits to Mbits
    else:
        bitrates.append(float(value))

# Creating the Bokeh Figure
p = figure(
    title="Testing Jaringan",
    x_axis_type="datetime",
    x_axis_label="DATE TIME",
    y_axis_label="Speed (Mbps)"
)

p.line(timestamps, bitrates, line_width=1.5, color="blue", alpha=1)

# Date Formatting for the x-axis
p.xaxis.formatter = DatetimeTickFormatter(
    hours="%m/%d/%Y %H:%M:%S",
    days="%m/%d/%Y %H:%M:%S",
    months="%m/%d/%Y %H:%M:%S",
    years="%m/%d/%Y %H:%M:%S"
)

# Showing the Bokeh Figure
show(p)