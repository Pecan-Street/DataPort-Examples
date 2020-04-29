import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# This constant limits the number of rows read in from the big CSV file.
# Set to None if you want to read the whole thing
LIMIT = 10000

if not os.path.isfile('metadata.csv'):
    print("Could not find metadata.csv file in {} .".format(os.getcwd()))
    exit(1)
if not os.path.isfile('15minute_data_austin.csv'):
    print("Could not find 15minute_data_austin.csv file in {} .".format(os.getcwd()))
    exit(1)

# read in the metadata file, skip the 2nd row because it has the comments further describing the headers
metadata = pd.read_csv('metadata.csv', engine='python', encoding="ISO-8859-1", skiprows=[1])


# filter down to our houses of interest. Active, Austin-based, has complete data, and has the grid circuit
dataids = metadata[metadata.active_record.eq('yes') &
                   metadata.city.eq('Austin') &
                   metadata.egauge_1min_data_availability.isin(['100%', '99%', '98%', '97%']) &
                   metadata.grid.eq('yes')]


# read the 15 minute data file for Austin
all_data = pd.read_csv('15minute_data_austin.csv', engine='python', encoding="ISO-8859-1",
                                  parse_dates=['local_15min'], index_col=['local_15min'],
                                  usecols=['dataid', 'local_15min', 'grid'],
                                  nrows=LIMIT)

# filter down to the dataids we're interested in
filt = all_data[all_data.dataid.isin(dataids.dataid)]

filt.index = pd.to_datetime(filt.index, utc=True, infer_datetime_format=True)
filt = filt.tz_convert('US/Central')

print(filt.describe())

# group the data by days and take the mean of those
days = filt.groupby(pd.Grouper(freq='D')).mean()

# convert from kW to kWh
days['grid_kwh'] = days['grid'].apply(lambda x: x * 24)

print(days.describe())

# create the plot
# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize': (11, 4)})
solar_plot = days['grid_kwh'].plot(linewidth=0.5, marker='.')
solar_plot.set_xlabel('Date')
solar_plot.set_ylabel('Grid Usage kWh')
solar_plot.set_title('Average Grid Usage in Austin, TX')

# display the plot
plt.show()

print('done')
exit(0)
