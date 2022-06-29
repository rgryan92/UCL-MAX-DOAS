"""
Created on Wed Jun 29 11:32:36 2022

@author: Robert Ryan
"""
import pandas as pd

## PATHS FOR FINDING THE DATA 
###############################################################################
path = 'C:/Users/Robert Ryan/OneDrive - University College London/Postdoc/'
path = path + 'MAX-DOAS/Results/log/'
files = ['MiniMax220625.log','MiniMax220626.log', 'MiniMax220627.log', 
         'MiniMax220628.log' ]

# ARRAYS TO POPULATE
###############################################################################
azi_dt, azi_north     = [],[]
sun_elev_dt, sun_elev = [],[]


# LOOP OVER FILES TO FIND OCCURENCES OF ANGLE CHECKING
###############################################################################
for file in files:
    with open(path+file, "r") as f:
        data = f.readlines()
    for line in data:
        if 'New azimotor_north' in line:
            azi_dt.append(line[:19])
            azi_north.append(float(line[-6:-1]))
        elif 'degree above expected elevation' in line:
            sun_elev_dt.append(line[:19])
            sun_elev.append(float(line[34:39]))

# CREATE PANDAS DATAFRAMES WITH DATETIME OF OCCURENCE AND UPDATED ANGLES
###############################################################################         
azi_dt_series = pd.Series(azi_dt)
sun_elev_dt_series = pd.Series(sun_elev_dt)

azi_df = pd.DataFrame(pd.to_datetime(azi_dt_series))
azi_df['azi_north'] = pd.Series(azi_north)
azi_df.columns = ['dt', 'azi_north']

# TIMESERIES PLOT OF AZI_NORTH UPDATES 
###############################################################################
azi_plot = azi_df.plot('dt', 'azi_north', style='bo')
azi_plot.set_ylabel('Calculated north position ($^o$)')
azi_plot.set_xlabel('Date and time')

# TIMESERIES PLOT OF SUN ELEVATION UPDATES 
###############################################################################
sun_elev_df = pd.DataFrame(pd.to_datetime(sun_elev_dt_series))
sun_elev_df['sun_elev'] = pd.Series(sun_elev)
sun_elev_df.columns = ['dt', 'sun_elev']
sun_elev_plot = sun_elev_df.plot('dt', 'sun_elev', style='ro')
sun_elev_plot.set_ylabel('Sun position difference ($^o$)')
sun_elev_plot.set_xlabel('Date and time')
