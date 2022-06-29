# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:05:56 2018

@author: rgryan

DOAS PLOTTING CODE: 
 plots differential slant column densities (dSCDs) that are
 calculated by DOASIS automatically on the UCL MAX-DOAS laptop.
 Plots allow dSCDs from a choice of elevation angles and azimuth angles
Rob Ryan 29/06/2022, UCL
"""

# Import section
# =========================================================================
import pandas as pd
import numpy as np
import matplotlib.dates as dates
import datetime
import matplotlib.pyplot as plt

# =========================================================================
# ============== SECTION OF THINGS TO CHECK AND CHANGE ====================
# =========================================================================

# Input files
# =========================================================================
filepath = 'C:/Users/Robert Ryan/OneDrive - University College London/'
filepath = filepath+'Postdoc/MAX-DOAS/Results/DOAS_Results/UV/'

file ='NO2_all' # 'HONO_all' #'BrO_all' # 'NO2_all' #'NO2_all' #'O4_360_all'
fitwindow = file #'435-456_v9'
header = 0

filetosave = 'Images/'+file
ext = '.txt'

# Dates to plot               
# =========================================================================
start_year, end_year = 2022,2022
start_month, end_month = 6,6
start_day, end_day =  26, 28
start_hour, end_hour = 3, 22

# INFO ON THE MEASUREMENT GEOMETRY:
# =========================================================================
EAs = [1,3,5,10,20,40]    # List of the elevation angles to plot
Azi = 180
EAoffset = 0                        #Elevation angle offset(degrees)
EAcolname = 'Viewing elevation angle'   # Name of the column with elevation angle data
ObsType = 'scattered_light' # 'direct sun'

# Plot settings
# =========================================================================  
# column header of the date/time data  
dtlabel = 'Start datetime UTC' 
   
show_error = False      # Show error bars on dSCD plots?   
save_plot = False             # Save the plots generated?
calcO3total = False           # Calculate total ozone dSCD?
#calcDL = False
#DLindex = 0            # Index of EAs list to calculate Detection limit on

fontsize = 10
figsize = (10, 2)          
legend_pos = (1.2,0.5)        #(1.12,1) is good for 15x3 plots 
                             #(1.42,1) is good for 4x3 plots (just 1 day of data)
hourinterval = 4             # x-axis label time interval (hours)
x_label_format = dates.MonthLocator()   # x-axis Label style 
                                       # for multiple day plots, DateLocator() works
                                       # for single day plots, it doesn't (!!), so use
                                       #     YearLocator()
            
hfmt = dates.DateFormatter('%d/%m %H:%M')

# =========================================================================
# ==================== FILE OPENING INSTRUCTIONS ==========================
# =========================================================================

filetoopen = filepath+file+ext       # define the QDOAS file to open 
startdate = datetime.datetime(start_year, start_month, start_day, start_hour)  
enddate = datetime.datetime(end_year, end_month, end_day, end_hour)

# FUNCTIONS TO DO THE PLOTTING
# =========================================================================
def create_readin_df(filetoopen, fitwindow):
    # FILE OPENING INSTRUCTIONS
    readin = pd.read_csv(filetoopen,  header=header, sep = '\t', 
                            parse_dates=['Start datetime UTC'], dayfirst=True)
    readin = readin.astype('float', errors='ignore')
    if calcO3total:
        readin[fitwindow+'.SlCol(O3total)'] = readin[fitwindow+'.SlCol(O3t)'] + readin[fitwindow+'.SlCol(O3s)']
        readin[fitwindow+'.SlErr(O3total)'] = np.sqrt((readin[fitwindow+'.SlErr(O3t)']**2) 
                       + (readin[fitwindow+'.SlCol(O3s)']**2))
        #readin[fitwindow+'.SlCol(O3total)'] = (readin[fitwindow+'.SlCol(O3t)'] + 
        #      readin[fitwindow+'.SlCol(O3s)'] + readin[fitwindow+'.SlCol(O3t_t1)'] +
        #      readin[fitwindow+'.SlCol(O3t_t2)'] + readin[fitwindow+'.SlCol(O3s_t1)'] + 
        #      readin[fitwindow+'.SlCol(O3s_t2)'])
    #readin = readin[readin['SZA']<85]
    
    return readin

def create_EA_dfs(readin_df):
    EAdflist = []
    for EA in EAs:
        if EA>5:
            EAdf_ = readin_df[readin_df[EAcolname]>(EA+EAoffset)-0.5]
            EAdf = EAdf_[EAdf_[EAcolname]<(EA+EAoffset)+0.5]
        else:
            EAdf_ = readin_df[readin_df[EAcolname]>(EA+EAoffset)-0.5]
            EAdf = EAdf_[EAdf_[EAcolname]<(EA+EAoffset)+0.5]
        EAdflist.append(EAdf)
    return EAdflist

def plot_tg_results(tg, ylimit):    
    if tg == 'RMS':
        whattoplot = 'Residual RMS'
        whattoplot1 = 'RMS'
        ylabel = whattoplot
        yerror = 0
    elif tg == 'shift_tg':
        whattoplot = fitwindow+'.Shift(O4)'
        whattoplot1 = 'Shift'
        yerror = fitwindow+'.Err Shift(O4)'
    elif tg == 'shift_spec':
        whattoplot = fitwindow+'.Shift(Spectrum)'
        whattoplot1 = 'Shift'
        yerror = fitwindow+'.Err Shift(Spectrum)'
    elif tg == 'O4':
        whattoplot1 = 'SCD('+tg+')'
        whattoplot = 'O4 dSCD [molec2/cm5]'
        yerror = 'O4 dSCD error [molec2/cm5]'
        ylabel = 'O$_4$ dSCD (molec$^2$.cm$^{-5}$)'
    else:
        whattoplot1 = 'SCD('+tg+')'
        whattoplot = tg+' '+'dSCD [molec/cm2]'
        yerror = tg+' '+'dSCD error [molec/cm2]'
        ylabel = tg+' dSCD (molec.cm$^{-2}$)'
    plottitle = tg+' dSCD '+fitwindow
    ylim = ylimit

    #if calcDL == True:
    #    EAdflist[DLindex]['DL'] = (2*readin[fitwindow+'.RMS']) / XSmax
    #else:
    #    EAdflist[DLindex]['DL'] = 0.0
    
    if show_error == True:        
        f = EAdflist[0].plot(x=dtlabel, y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='k.', ylim=ylim, yerr=yerror)        
        for i in np.arange(len(EAdflist[:])):
            EAdflist[i].plot(x=dtlabel, y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='.', ylim=ylim, yerr=yerror, ax=f)
    
    else:
        fig = plt.figure(figsize=figsize)
        f = fig.add_subplot(111)
        for i in np.arange(len(EAdflist[:])):
            #print('    plotting '+str(EAs[i]))
            EAdflist[i].plot(x=dtlabel, y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='.', ylim=ylim, ax=f)
        #EAdflist[DLindex].plot(x=dtlabel, y = 'DL', fontsize=fontsize, figsize=figsize, 
        #            style='k-', ylim=ylim, ax=f)
        
    f.set_title(plottitle, fontsize=fontsize)
    f.set_xlabel('Date_Time', fontsize=fontsize)
    f.set_ylabel(ylabel, fontsize=fontsize)   
    f.set_xlim(startdate, enddate)
    f.legend([str(i)+' deg' for i in EAs], 
                 loc='center right', bbox_to_anchor=legend_pos)
    f.xaxis.set_major_locator(dates.HourLocator(interval=hourinterval))
    f.xaxis.set_major_formatter(hfmt)
        
    if save_plot:
        fig = f.get_figure()
        fig.savefig(filepath+filetosave+whattoplot1+str(start_day)+str(start_month)+
                str(start_year)+'_'+str(end_day)+str(end_month)+str(end_year)+'_'+
                fitwindow+'.pdf', 
                    bbox_inches='tight')  
#%%
# Run the first function on the data frame read in
# =================================================
readin = create_readin_df(filetoopen, fitwindow) 

readin = readin[readin['Residual RMS'] < 8e-4] # remove the problem ones where
                                                # an error causes a value of 
                                                # ~9e+36
readin = readin[readin['Residual RMS'] > 2e-6]
readin = readin[readin['Solar zenith angle'] < 95]
readin = readin[readin['Viewing azimuth angle']<Azi+5] # Find the right Azimuth angle
readin = readin[readin['Viewing azimuth angle']>Azi-5]
readin = readin[readin['Observation type'] == ObsType ]

EAdflist = create_EA_dfs(readin)
#%%
plot_tg_results('NO2_294K', [-1e16,1e17])
#plot_tg_results(  'O4', [-2e42,8e43]     )
#plot_tg_results('HCHO', [-1e16,0.5e17])
#plot_tg_results('O3total', [-2e18,1e19])
plot_tg_results('RMS', [0.0001,0.001])
#plot_tg_results('O3s', [-8e18,6e18])
#plot_tg_results('O3total', [-2e18,1e19])
#plot_tg_results('O3t', [-2e18,1e19])
#plot_tg_results(('Ring'), [-0.05, 2e-2])
#plot_tg_results('shift_tg', [-0.4, 0.4])
#plot_tg_results('shift_spec', [-0.008, -0.001])
#plot_tg_results('HONO', [-1e15,2e15])
#plot_tg_results('CHOCHO', [-5e15,1e16])
#plot_tg_results('BrO', [-2e14,2e14])
#plot_tg_results('IO', [-2e13,1e14])