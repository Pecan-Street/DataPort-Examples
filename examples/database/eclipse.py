import os
import pandas as pd
import psycopg2
import traceback
import sqlalchemy as sqla
import matplotlib.pyplot as plt
import seaborn as sns

from config.read_config import get_database_config

"""
This Python script downloads data from the Pecan Street Inc DataPort database directly
and uses Pandas and Matplotlib to plot average solar production per hour during several
days in August 2017 covering the day of the solar eclipse (21st).

First it gathers a set of homes by dataid from other_datasets.metadata for the date range
that have grid (whole home electrical grid usage), solar, are in the city of Austin,
and have very complete data.

From that set of dataids, we select:
local_15min : the datetime stamp of the record
air1: the usage of the air conditioner (not used here)
car1: the usage of the electrical vehicle charger (not used here)
grid: the usage of the whole home from the electrical grid (not used here)
solar: solar production 

We group the days and group the hours of solar production and take the mean for every hour across all of the homes
and plot that. 

The other unused circuits are there for your convenience.

Please feel free to expand on this or create other examples and submit them by pull request!
"""


me = os.path.basename(__file__)

try:
    # !! Go set your username, password, host, port, and database name in the config/config.txt file!
    database_config = get_database_config("../../config/config.txt")

    engine = sqla.create_engine('postgresql://{}:{}@{}:{}/{}'.format(database_config['username'],
                                                                     database_config['password'],
                                                                     database_config['hostname'],
                                                                     database_config['port'],
                                                                     database_config['database']
                                                                     ))

    # let's select some homes for the a few days of Aug2017 that have grid data that's very complete,
    # and have pv, and solar
    query = """SELECT dataid, local_15min, air1, car1, grid, solar 
            FROM electricity.eg_realpower_15min
            WHERE extract(month from local_15min) = 8 AND local_15min >= '2017-08-19' AND local_15min < '2017-08-24' 
            AND dataid IN(
            	SELECT dataid
            	FROM other_datasets.metadata where 
            	egauge_1min_min_time < '2017-08-19' AND egauge_1min_max_time >= '2017-08-24'
                AND grid is not null
                AND solar is not null
                AND city = 'Austin'
                AND (
                    egauge_1min_data_availability like '100%' OR
                    egauge_1min_data_availability like '99%' OR
                    egauge_1min_data_availability like '98%' 
                    )
            );"""

    # create a dataframe with the data from the sql query
    df = pd.read_sql_query(sqla.text(query), engine)

    print(df.describe())

    # set the index to the timestamps
    df = df.set_index('local_15min')
    # convert to US Central time from UTC
    df = df.tz_convert('US/Central')
    print("DataFrame info:")
    print(df.info())

    # group the data hours and take the mean of those to get kWh
    days = df.groupby(pd.Grouper(freq='H')).mean()

    # create the plot
    # Use seaborn style defaults and set the default figure size
    sns.set(rc={'figure.figsize': (11, 4)})
    solar_plot = days['solar'].plot(linewidth=0.5, marker='.')
    solar_plot.set_xlabel('Date')
    solar_plot.set_ylabel('Solar Production kWh')
    solar_plot.set_title('Solar Production During Aug,21 2017 Eclipse')

    # display the plot
    plt.show()

    print('Done')
    exit(0)


except psycopg2.Error as dbe:
    traceback.print_exc()
    print("Error connecting to database from {}.".format(me))
