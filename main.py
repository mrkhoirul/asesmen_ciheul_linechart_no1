from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
import re
from datetime import datetime
from collections import defaultdict

# Reading File
with open('data.txt', 'r') as file:
    data = file.read()

# Regular Expression to find all timestamps and bitrates
reg = r"Timestamp:\s*([0-9\-]+\s+[0-9:]+).*?\[\s\s\d\]\s+[0-9]*\.[0-9]+-[0-9]*\.[0-9]+\s+sec\s+[\d\.]+\s+\w+Bytes\s+([\d\.]+)\s+(Mbits|Kbits)\/sec.*?sender"
matches = re.findall(reg, data, re.S)

# Parsing the matches to extract timestamps and bitrates & convert to Mbits
data_in_hour = defaultdict(list)
for timestamp, value, unit in matches:
    # Convert timestamp to datetime object
    dt = datetime.strptime(timestamp.strip(), '%Y-%m-%d %H:%M:%S')
    hour = dt.replace(minute=0, second=0, microsecond=0)
    
    # Convert bitrate to float and adjust based on unit
    val = float(value)
    if unit == 'Kbits':
        val /= 1000.0  # Convert Kbits to Mbits
    data_in_hour[hour].append(val)

# Take the data for each hour
timestamps = []
bitrates = []
for hour in sorted(data_in_hour.keys()):
    average = sum(data_in_hour[hour]) / len(data_in_hour[hour])
    timestamps.append(hour)
    bitrates.append(average)

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