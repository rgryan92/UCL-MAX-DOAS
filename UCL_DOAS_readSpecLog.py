# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:48:13 2022

@author: Robert Ryan
"""

import pandas as pd

## PATHS FOR FINDING THE DATA 
###############################################################################
path = 'C:/Users/Robert Ryan/OneDrive - University College London/Postdoc/'
path = path + 'MAX-DOAS/Results/log/'
files = ['Spec220626.log','Spec220627.log','Spec220628.log','Spec220629.log',
         'Spec220630.log','Spec220701.log' ]
        
var2plot = 'tele_dewpoint_controllerboard'
'''
VARIABLES IN THE SPEC LOG FILE
===============================================================================
'date_time', 'sza', 'saa', 'lat', 'lon', 'measurement_type',
'uv_spec_filename', 'uv_spec_filenumber', 'vis_spec_filename',
'vis_spec_filenumber', 'elevmotor_npos', 'elevmotor_pos',
'elev_absolute', 'elev_offset', 'azimotor_npos', 'azimotor_pos',
'azi_absolute', 'azimotor_north', 'servo_pos', 'uv_spec_min',
'uv_spec_max', 'uv_spec_avg', 'vis_spec_min', 'vis_spec_max',
       'vis_spec_avg', 'sbox_controller_uptime_ms', 'sbox_pressure',
       'sbox_temp', 'sbox_humidity', 'sbox_dewpoint', 'sbox_temp_spectrometer',
       'sbox_temp1', 'sbox_temp2', 'sbox_temp3', 'sbox_peltier_power',
       'tele_temp0', 'tele_elevsens_x', 'tele_elevsens_y', 'tele_elevsens_z',
       'tele_elevsens_angle', 'tele_elevsens_angle_noise', 'tele_temp_outside',
       'tele_temp_outside_noise', 'tele_temp_elevsens',
       'tele_humidity_controllerboard', 'tele_temp_controllerboard',
       'tele_pressure_controllerboard', 'tele_dewpoint_controllerboard',
       'tele_supply_voltage', 'tele_controller_uptime',
       'tele_temp_controllerchip', 'sbox_temp_controllerchip',
       'sbox_supply_voltage', 'sbox_supply_voltage_5V', 'sbox_hbridge_current',
       'instrument_supply_current', 'sbox_temp_spectrometer_noise',
       'sbox_temp1_noise', 'sbox_temp2_noise', 'sbox_temp3_noise',
       'sbox_pid_p', 'sbox_pid_i', 'sbox_pid_d',
       'sbox_temp_controllerboard_noise', 'sbox_pres_controllerboard_noise',
       'sbox_humidity_controllerboard_noise', 'twito_internal_use_only',
       'instrument_power_limitation_enabled',
       'sbox_total_controller_uptime_hours'
===============================================================================
'''


datetimes, what2plot = [], []
df_ = pd.read_csv(path+files[0], sep=' ',header=0,parse_dates=[['date','time']])
if len(files)>1:
    F = [df_]
    for file in files[1:]:
        data = pd.read_csv(path+file, sep=' ',header=0,
                           parse_dates=[['date','time']], dayfirst=True)
        F.append(data)
    df_ = pd.concat(F)
    
p = df_.plot('date_time', var2plot, style='ro')
