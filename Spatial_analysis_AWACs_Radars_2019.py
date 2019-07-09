# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 13:40:08 2018
This code will analyse AWAC data and provide information on the spatial difference of wave characteristics between locations. 
Primarily written for 2016 AWAC Deployment but should be used for 2013 deployment and future deployments too. 
@author: DS12
"""
#%%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.patches as mpatches
import os
import Sizewell_Radar_Core as SRC
import datetime
#%%
# Load data files for AWAC 
data=pd.read_excel('O:/Beems_Share/07_Work_Package/Sizewell/TR504 Sizewell inshore wave and current seabed lander data February – May 2019/MicroLander AWAC Inshore/Data/AWAC_SZ_2019_SZ3_6562D101_wave_parameters.xlsx','6562D101wap')

dstart = datetime.date(2019,2,1)    
dfinish = datetime.date(2019,5,30)    
CA3 = SRC.LoadAndFormatRadarData(dstart, dfinish, r"O:\Beems_Data\10 BEEMS DATA CENTRE - SITES\SIZEWELL\SZ_WP4_Radar_WaMoS_TimeSeriesData\WaMoS TimeSeries\MPA", 3) # Find relevant data from Zone (CA) 1.
CA2 = SRC.LoadAndFormatRadarData(dstart, dfinish, r"O:\Beems_Data\10 BEEMS DATA CENTRE - SITES\SIZEWELL\SZ_WP4_Radar_WaMoS_TimeSeriesData\WaMoS TimeSeries\MPA", 2) # Find relevant data from Zone (CA) 1.
CA1 = SRC.LoadAndFormatRadarData(dstart, dfinish, r"O:\Beems_Data\10 BEEMS DATA CENTRE - SITES\SIZEWELL\SZ_WP4_Radar_WaMoS_TimeSeriesData\WaMoS TimeSeries\MPA", 1) # Find relevant data from Zone (CA) 1.

CA3= CA3.data_good
CA3= CA3.replace(-9, np.nan)
CA3= CA3.resample('h').mean()
CA3= CA3.drop(columns=['ELEVL', 'HMax', 'INDEX', 'IQ', 'LP', 'NORI', 'NSPEC',
       'PD1', 'PD2', 'PDir', 'Tlim', 'Tm2', 'Tp1', 'Tp2', 'Udir', 'Usp','lp1', 'lp2'])
CA2= CA2.data_good
CA2= CA2.replace(-9, np.nan)
CA2= CA2.resample('h').mean()
CA2= CA2.drop(columns=['ELEVL', 'HMax', 'INDEX', 'IQ', 'LP', 'NORI', 'NSPEC',
       'PD1', 'PD2', 'PDir', 'Tlim', 'Tm2', 'Tp1', 'Tp2', 'Udir', 'Usp','lp1', 'lp2'])
CA1= CA1.data_good
CA1= CA1.replace(-9, np.nan)
CA1= CA1.resample('h').mean()
CA1= CA1.drop(columns=['ELEVL', 'HMax', 'INDEX', 'IQ', 'LP', 'NORI', 'NSPEC',
       'PD1', 'PD2', 'PDir', 'Tlim', 'Tm2', 'Tp1', 'Tp2', 'Udir', 'Usp','lp1', 'lp2'])

AWAC_INM= pd.concat([data['MS Date'], data['Significantheight(Hm0) (m)'], data['Peakperiod(Tp) (s)'], data['Meandirection(Mdir) (deg)']] , axis=1)
AWAC_INM.index= AWAC_INM['MS Date']
AWAC_INM=AWAC_INM.drop(columns='MS Date')
AWAC_INM.columns=['Hs_AWAC','Tp_AWAC','MDir_AWAC']
AWAC_INM = AWAC_INM.resample('h').mean()

#%%
path = 'O:/Beems_Share/04_Work_Package/Sizewell/TR317_Ed2/Data/Virtual_wave_buoy_analysis/Data/2019'
if not os.path.exists(path):
    os.makedirs(path)        
os.chdir(path)

# North Radar / Middle AWAC

CA3_AWAC_INM= pd.merge(AWAC_INM,CA3, left_on=AWAC_INM.index, right_on=CA3.index, how='inner')
CA3_AWAC_INM.rename(columns={'key_0': 'Dates'}, inplace=True)
CA3_AWAC_INM.index=CA3_AWAC_INM.Dates
CA3_AWAC_INM=CA3_AWAC_INM.drop(['Dates'], axis=1)

# Direction
mask = ~np.isnan(CA3_AWAC_INM.MDir) & ~np.isnan(CA3_AWAC_INM.MDir_AWAC)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA3_AWAC_INM.MDir[mask],CA3_AWAC_INM.MDir_AWAC[mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar North (CA3)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction 2019', fontsize= 12)
plt.savefig('CA3_AWAC_INM_Dir_2019.jpeg')

# Period 

sns.set_style("ticks")
mask = ~np.isnan(CA3_AWAC_INM.Tp) & ~np.isnan(CA3_AWAC_INM.Tp_AWAC)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA3_AWAC_INM.Tp[mask], CA3_AWAC_INM.Tp_AWAC[mask])
g=sns.jointplot(CA3_AWAC_INM.Tp[mask],CA3_AWAC_INM.Tp_AWAC[mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.2,) #.plot_joint(sns.kdeplot,n_levels=20,shade=False, cmap="RdBu_r")
plt.xlim(0,20)
plt.ylim(0,20)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(15.5,17.75, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar North (CA3)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA3_AWAC_INM_Tp_2019.jpeg')


#%%
##############################################################################
# Middle Radar / Middle AWAC

CA2_AWAC_INM= pd.merge(AWAC_INM,CA2, left_on=AWAC_INM.index, right_on=CA2.index, how='inner')
CA2_AWAC_INM.rename(columns={'key_0': 'Dates'}, inplace=True)
CA2_AWAC_INM.index=CA2_AWAC_INM.Dates
CA2_AWAC_INM=CA2_AWAC_INM.drop(['Dates'], axis=1)

# Direction
mask = ~np.isnan(CA2_AWAC_INM.MDir) & ~np.isnan(CA2_AWAC_INM.MDir_AWAC)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA2_AWAC_INM.MDir[mask],CA2_AWAC_INM.MDir_AWAC[mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar Middle (CA2)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA2_AWAC_INM_Dir_2019.jpeg')

# Period 

sns.set_style("ticks")
mask = ~np.isnan(CA2_AWAC_INM.Tp) & ~np.isnan(CA2_AWAC_INM.Tp_AWAC)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA2_AWAC_INM.Tp[mask], CA2_AWAC_INM.Tp_AWAC[mask])
g=sns.jointplot(CA2_AWAC_INM.Tp[mask],CA2_AWAC_INM.Tp_AWAC[mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.2,) #.plot_joint(sns.kdeplot,n_levels=20,shade=False, cmap="RdBu_r")
plt.xlim(0,20)
plt.ylim(0,20)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(15.5,17.75, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar Middle (CA2)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA2_AWAC_INM_Tp_2019.jpeg')

#%%
# South Radar / Middle AWAC

CA1_AWAC_INM= pd.merge(AWAC_INM,CA1, left_on=AWAC_INM.index, right_on=CA1.index, how='inner')
CA1_AWAC_INM.rename(columns={'key_0': 'Dates'}, inplace=True)
CA1_AWAC_INM.index=CA1_AWAC_INM.Dates
CA1_AWAC_INM=CA1_AWAC_INM.drop(['Dates'], axis=1)

# Direction
mask = ~np.isnan(CA1_AWAC_INM.MDir) & ~np.isnan(CA1_AWAC_INM.MDir_AWAC)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA1_AWAC_INM.MDir[mask],CA1_AWAC_INM.MDir_AWAC[mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar South (CA1)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA1_AWAC_INM_Dir_2019.jpeg')

# Period 

sns.set_style("ticks")
mask = ~np.isnan(CA1_AWAC_INM.Tp) & ~np.isnan(CA1_AWAC_INM.Tp_AWAC)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA1_AWAC_INM.Tp[mask], CA1_AWAC_INM.Tp_AWAC[mask])
g=sns.jointplot(CA1_AWAC_INM.Tp[mask],CA1_AWAC_INM.Tp_AWAC[mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.2,) #.plot_joint(sns.kdeplot,n_levels=20,shade=False, cmap="RdBu_r")
plt.xlim(0,20)
plt.ylim(0,20)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(15.5,17.75, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar South (CA1)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA1_AWAC_INM_Tp_2019.jpeg')

#%%
# Save files
CA1_AWAC_INM.to_excel('CA1_AWAC_INM.xlsx')
CA2_AWAC_INM.to_excel('CA2_AWAC_INM.xlsx')
CA3_AWAC_INM.to_excel('CA3_AWAC_INM.xlsx')


#%%
######## Add Period Filter of 9 sec!##########################################
#%%

# North Radar/Middle AWAC
# Period
sns.set_style("ticks")
mask = ~np.isnan(CA3_AWAC_INM.Tp) & ~np.isnan(CA3_AWAC_INM.Tp_AWAC)
mask1 = (CA3_AWAC_INM.Tp<=9) & (CA3_AWAC_INM.Tp_AWAC<=9)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA3_AWAC_INM.Tp[mask][mask1], CA3_AWAC_INM.Tp_AWAC[mask][mask1])
g=sns.jointplot(CA3_AWAC_INM.Tp[mask1][mask],CA3_AWAC_INM.Tp_AWAC[mask1][mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.3,) 
plt.xlim(0,15)
plt.ylim(0,15)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(10.5,13.25, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar North (CA3)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA3_AWAC_INM_Tp_9sec_2019.jpeg')


# Direction
mask = ~np.isnan(CA3_AWAC_INM.MDir) & ~np.isnan(CA3_AWAC_INM.MDir_AWAC)
mask1 = (CA3_AWAC_INM.Tp<=9) & (CA3_AWAC_INM.Tp_AWAC<=9)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA3_AWAC_INM.MDir[mask1][mask],CA3_AWAC_INM.MDir_AWAC[mask1][mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar North (Z3)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA3_AWAC_INM_Dir_9sec_2019.jpeg')

#%% Middle Radar/Middle AWAC with filter 9 sec period on Radar
# Period
sns.set_style("ticks")
mask = ~np.isnan(CA2_AWAC_INM.Tp) & ~np.isnan(CA2_AWAC_INM.Tp_AWAC)
mask1 = (CA2_AWAC_INM.Tp<=9) & (CA2_AWAC_INM.Tp_AWAC<=9)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA2_AWAC_INM.Tp[mask][mask1], CA2_AWAC_INM.Tp_AWAC[mask][mask1])
g=sns.jointplot(CA2_AWAC_INM.Tp[mask1][mask],CA2_AWAC_INM.Tp_AWAC[mask1][mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.3,) 
plt.xlim(0,15)
plt.ylim(0,15)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(10.5,13.25, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar Middle (CA2)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA2_AWAC_INM_Tp_9sec_2019.jpeg')


# Direction
mask = ~np.isnan(CA2_AWAC_INM.MDir) & ~np.isnan(CA2_AWAC_INM.MDir_AWAC)
mask1 = (CA2_AWAC_INM.Tp<=9) & (CA2_AWAC_INM.Tp_AWAC<=9)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA2_AWAC_INM.MDir[mask1][mask],CA2_AWAC_INM.MDir_AWAC[mask1][mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar Middle (CA2)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA2_AWAC_INM_Dir_9sec_2019.jpeg')

#%% South Radar/Middle AWAC with filter 9 sec period on Radar
# Period
sns.set_style("ticks")
mask = ~np.isnan(CA1_AWAC_INM.Tp) & ~np.isnan(CA1_AWAC_INM.Tp_AWAC)
mask1 = (CA1_AWAC_INM.Tp<=9) & (CA1_AWAC_INM.Tp_AWAC<=9)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA1_AWAC_INM.Tp[mask][mask1], CA1_AWAC_INM.Tp_AWAC[mask][mask1])
g=sns.jointplot(CA1_AWAC_INM.Tp[mask1][mask],CA1_AWAC_INM.Tp_AWAC[mask1][mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.3,) 
plt.xlim(0,15)
plt.ylim(0,15)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(10.5,13.25, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar South (CA1)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA1_AWAC_INM_Tp_9sec_2019.jpeg')

# Direction
mask = ~np.isnan(CA1_AWAC_INM.MDir) & ~np.isnan(CA1_AWAC_INM.MDir_AWAC)
mask1 = (CA1_AWAC_INM.Tp<=9) & (CA1_AWAC_INM.Tp_AWAC<=9)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA1_AWAC_INM.MDir[mask1][mask],CA1_AWAC_INM.MDir_AWAC[mask1][mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar South (CA1)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA1_AWAC_INM_Dir_9sec_2019.jpeg')

#%% ###########################################################################
##############################################################################
######## Add Period Filter of 9 sec and a Hs Filter of 0.85!##################
##############################################################################


# North Radar/Middle AWAC
# Period
sns.set_style("ticks")
mask = ~np.isnan(CA3_AWAC_INM.Tp) & ~np.isnan(CA3_AWAC_INM.Tp_AWAC) & (CA3_AWAC_INM.Tp<=9) & (CA3_AWAC_INM.Tp_AWAC<=9) & (CA3_AWAC_INM.Hs>=0.85) & (CA3_AWAC_INM.Hs_AWAC>=0.85)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA3_AWAC_INM.Tp[mask], CA3_AWAC_INM.Tp_AWAC[mask])
g=sns.jointplot(CA3_AWAC_INM.Tp[mask],CA3_AWAC_INM.Tp_AWAC[mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.3,) 
plt.xlim(0,15)
plt.ylim(0,15)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(10.5,13.25, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar North (CA3)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA3_AWAC_INM_Tp_9sec_85cm_Hs_2019.jpeg')


# Direction
mask = ~np.isnan(CA3_AWAC_INM.MDir) & ~np.isnan(CA3_AWAC_INM.MDir_AWAC)
mask1 = ~np.isnan(CA3_AWAC_INM.Tp) & ~np.isnan(CA3_AWAC_INM.Tp_AWAC) & (CA3_AWAC_INM.Tp<=9) & (CA3_AWAC_INM.Tp_AWAC<=9) & (CA3_AWAC_INM.Hs>=0.85) & (CA3_AWAC_INM.Hs_AWAC>=0.85)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA3_AWAC_INM.MDir[mask1][mask],CA3_AWAC_INM.MDir_AWAC[mask1][mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar North (CA3)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA3_AWAC_INM_Dir_9sec_85cm_Hs_2019.jpeg')


# Middle Radar/Middle AWAC with filter 9 sec period on Radar
# Period
sns.set_style("ticks")
mask = ~np.isnan(CA2_AWAC_INM.Tp) & ~np.isnan(CA2_AWAC_INM.Tp_AWAC) & (CA2_AWAC_INM.Tp<=9) & (CA2_AWAC_INM.Tp_AWAC<=9) & (CA2_AWAC_INM.Hs>=0.85) & (CA2_AWAC_INM.Hs_AWAC>=0.85)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA2_AWAC_INM.Tp[mask], CA2_AWAC_INM.Tp_AWAC[mask])
g=sns.jointplot(CA2_AWAC_INM.Tp[mask],CA2_AWAC_INM.Tp_AWAC[mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.3,) 
plt.xlim(0,15)
plt.ylim(0,15)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(10.5,13.25, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar Middle (CA2)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA2_AWAC_INM_Tp_9sec_85cm_Hs_2019.jpeg')

# Direction
mask = ~np.isnan(CA2_AWAC_INM.MDir) & ~np.isnan(CA2_AWAC_INM.MDir_AWAC)
mask1 = ~np.isnan(CA2_AWAC_INM.Tp) & ~np.isnan(CA2_AWAC_INM.Tp_AWAC) & (CA2_AWAC_INM.Tp<=9) & (CA2_AWAC_INM.Tp_AWAC<=9) & (CA2_AWAC_INM.Hs>=0.85) & (CA2_AWAC_INM.Hs_AWAC>=0.85)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA2_AWAC_INM.MDir[mask1][mask],CA2_AWAC_INM.MDir_AWAC[mask1][mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar Middle (CA2)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA2_AWAC_INM_Dir_9sec_85cm_Hs_2019.jpeg')


# South Radar/Middle AWAC 
# Period
sns.set_style("ticks")
mask =~np.isnan(CA1_AWAC_INM.Tp) & ~np.isnan(CA1_AWAC_INM.Tp_AWAC) & (CA1_AWAC_INM.Tp<=9) & (CA1_AWAC_INM.Tp_AWAC<=9) & (CA1_AWAC_INM.Hs>=0.85) & (CA1_AWAC_INM.Hs_AWAC>=0.85)
slope, intercept, r_value_1, p_value, std_err = stats.linregress(CA1_AWAC_INM.Tp[mask], CA1_AWAC_INM.Tp_AWAC[mask])
g=sns.jointplot(CA1_AWAC_INM.Tp[mask],CA1_AWAC_INM.Tp_AWAC[mask], color="b",kind='reg',scatter_kws={'alpha':0.15}, line_kws={'color': 'red'},space = 0.3,) 
plt.xlim(0,15)
plt.ylim(0,15)
linear_fit= mpatches.Patch(color='red',label='y = {}*x {}'.format(round(slope,2), round(intercept,2)))
plt.legend(handles=[linear_fit], loc='best')
plt.text(10.5,13.25, 'r ={}'.format(round(r_value_1,3)))
g.set_axis_labels("Tp (s) Radar South (CA1)", "Tp (s) AWAC Middle (INM)");
plt.savefig('CA1_AWAC_INM_Tp_9sec_85cm_Hs_2019.jpeg')

# Direction
mask = ~np.isnan(CA1_AWAC_INM.MDir) & ~np.isnan(CA1_AWAC_INM.MDir_AWAC)
mask1 =~np.isnan(CA1_AWAC_INM.Tp) & ~np.isnan(CA1_AWAC_INM.Tp_AWAC) & (CA1_AWAC_INM.Tp<=9) & (CA1_AWAC_INM.Tp_AWAC<=9) & (CA1_AWAC_INM.Hs>=0.85) & (CA1_AWAC_INM.Hs_AWAC>=0.85)
sns.set(style="white", color_codes=True)
g=sns.jointplot(CA1_AWAC_INM.MDir[mask1][mask],CA1_AWAC_INM.MDir_AWAC[mask1][mask],scatter=True,fit_reg=False, color="b",kind='reg',space = 0.2, ci=None, truncate=True, order=0, scatter_kws={"s": 80, 'alpha':0.15}).plot_joint(sns.kdeplot, n_levels=20,shade=True, cmap="RdBu_r")
g.set_axis_labels("Wave Dir (Degrees) Radar South (CA1)", "Wave Dir (Degrees) AWAC Middle (INM)");
g.fig.suptitle('Direction', fontsize= 12)
plt.savefig('CA1_AWAC_INM_Dir_9sec_85cm_Hs_2019.jpeg')


##############################################################################
#%% Splitting to directions and saving files
CA1_AWAC_INM_Tp_Hs=CA1_AWAC_INM[(CA1_AWAC_INM.Tp <= 9) & (CA1_AWAC_INM.Tp_AWAC <= 9) & (CA1_AWAC_INM.Hs>=0.85) & (CA1_AWAC_INM.Hs_AWAC>=0.85)]
CA1_AWAC_INM_Tp_Hs_NE= CA1_AWAC_INM_Tp_Hs[(CA1_AWAC_INM_Tp_Hs.MDir < 67.5) & (CA1_AWAC_INM_Tp_Hs.MDir >= 22.5) & (CA1_AWAC_INM_Tp_Hs.MDir_AWAC < 67.5) & (CA1_AWAC_INM_Tp_Hs.MDir_AWAC >= 22.5)]
CA1_AWAC_INM_Tp_Hs_E= CA1_AWAC_INM_Tp_Hs[(CA1_AWAC_INM_Tp_Hs.MDir < 112.5) & (CA1_AWAC_INM_Tp_Hs.MDir >= 67.5) & (CA1_AWAC_INM_Tp_Hs.MDir_AWAC < 112.5) & (CA1_AWAC_INM_Tp_Hs.MDir_AWAC >= 67.5)]
CA1_AWAC_INM_Tp_Hs_SE= CA1_AWAC_INM_Tp_Hs[(CA1_AWAC_INM_Tp_Hs.MDir < 157.5) & (CA1_AWAC_INM_Tp_Hs.MDir >= 112.5) & (CA1_AWAC_INM_Tp_Hs.MDir_AWAC < 157.5) & (CA1_AWAC_INM_Tp_Hs.MDir_AWAC >= 112.5)]


CA2_AWAC_INM_Tp_Hs=CA2_AWAC_INM[(CA2_AWAC_INM.Tp <= 9) & (CA2_AWAC_INM.Tp_AWAC <= 9) & (CA2_AWAC_INM.Hs>=0.85) & (CA2_AWAC_INM.Hs_AWAC>=0.85)]
CA2_AWAC_INM_Tp_Hs_NE= CA2_AWAC_INM_Tp_Hs[(CA2_AWAC_INM_Tp_Hs.MDir < 67.5) & (CA2_AWAC_INM_Tp_Hs.MDir >= 22.5) & (CA2_AWAC_INM_Tp_Hs.MDir_AWAC < 67.5) & (CA2_AWAC_INM_Tp_Hs.MDir_AWAC >= 22.5)]
CA2_AWAC_INM_Tp_Hs_E= CA2_AWAC_INM_Tp_Hs[(CA2_AWAC_INM_Tp_Hs.MDir < 112.5) & (CA2_AWAC_INM_Tp_Hs.MDir >= 67.5) & (CA2_AWAC_INM_Tp_Hs.MDir_AWAC < 112.5) & (CA2_AWAC_INM_Tp_Hs.MDir_AWAC >= 67.5)]
CA2_AWAC_INM_Tp_Hs_SE= CA2_AWAC_INM_Tp_Hs[(CA2_AWAC_INM_Tp_Hs.MDir < 157.5) & (CA2_AWAC_INM_Tp_Hs.MDir >= 112.5) & (CA2_AWAC_INM_Tp_Hs.MDir_AWAC < 157.5) & (CA2_AWAC_INM_Tp_Hs.MDir_AWAC >= 112.5)]

CA3_AWAC_INM_Tp_Hs=CA3_AWAC_INM[(CA3_AWAC_INM.Tp <= 9) & (CA3_AWAC_INM.Tp_AWAC <= 9) & (CA3_AWAC_INM.Hs>=0.85) & (CA3_AWAC_INM.Hs_AWAC>=0.85)]
CA3_AWAC_INM_Tp_Hs_NE= CA3_AWAC_INM_Tp_Hs[(CA3_AWAC_INM_Tp_Hs.MDir < 67.5) & (CA3_AWAC_INM_Tp_Hs.MDir >= 22.5) & (CA3_AWAC_INM_Tp_Hs.MDir_AWAC < 67.5) & (CA3_AWAC_INM_Tp_Hs.MDir_AWAC >= 22.5)]
CA3_AWAC_INM_Tp_Hs_E= CA3_AWAC_INM_Tp_Hs[(CA3_AWAC_INM_Tp_Hs.MDir < 112.5) & (CA3_AWAC_INM_Tp_Hs.MDir >= 67.5) & (CA3_AWAC_INM_Tp_Hs.MDir_AWAC < 112.5) & (CA3_AWAC_INM_Tp_Hs.MDir_AWAC >= 67.5)]
CA3_AWAC_INM_Tp_Hs_SE= CA3_AWAC_INM_Tp_Hs[(CA3_AWAC_INM_Tp_Hs.MDir < 157.5) & (CA3_AWAC_INM_Tp_Hs.MDir >= 112.5) & (CA3_AWAC_INM_Tp_Hs.MDir_AWAC < 157.5) & (CA3_AWAC_INM_Tp_Hs.MDir_AWAC >= 112.5)]



CA1_AWAC_INM_Tp_Hs.to_excel('CA1_AWAC_INM_Tp_Hs.xlsx')
CA1_AWAC_INM_Tp_Hs_NE.to_excel('CA1_AWAC_INM_Tp_Hs_NE.xlsx')
CA1_AWAC_INM_Tp_Hs_E.to_excel('CA1_AWAC_INM_Tp_Hs_E.xlsx')
CA1_AWAC_INM_Tp_Hs_SE.to_excel('CA1_AWAC_INM_Tp_Hs_SE.xlsx')
CA2_AWAC_INM_Tp_Hs.to_excel('CA2_AWAC_INM_Tp_Hs.xlsx')
CA2_AWAC_INM_Tp_Hs_NE.to_excel('CA2_AWAC_INM_Tp_Hs_NE.xlsx')
CA2_AWAC_INM_Tp_Hs_E.to_excel('CA2_AWAC_INM_Tp_Hs_E.xlsx')
CA2_AWAC_INM_Tp_Hs_SE.to_excel('CA2_AWAC_INM_Tp_Hs_SE.xlsx')
CA3_AWAC_INM_Tp_Hs.to_excel('CA3_AWAC_INM_Tp_Hs.xlsx')
CA3_AWAC_INM_Tp_Hs_NE.to_excel('CA3_AWAC_INM_Tp_Hs_NE.xlsx')
CA3_AWAC_INM_Tp_Hs_E.to_excel('CA3_AWAC_INM_Tp_Hs_E.xlsx')
CA3_AWAC_INM_Tp_Hs_SE.to_excel('CA3_AWAC_INM_Tp_Hs_SE.xlsx')

#%% Stats
from sklearn import metrics

RMSE_CA1_INM_NE_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA1_AWAC_INM_Tp_Hs_NE.Hs,CA1_AWAC_INM_Tp_Hs_NE.Hs_AWAC)),2))
RMSE_CA2_INM_NE_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA2_AWAC_INM_Tp_Hs_NE.Hs,CA2_AWAC_INM_Tp_Hs_NE.Hs_AWAC)),2))
RMSE_CA3_INM_NE_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA3_AWAC_INM_Tp_Hs_NE.Hs,CA3_AWAC_INM_Tp_Hs_NE.Hs_AWAC)),2))

RMSE_CA1_INM_E_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA1_AWAC_INM_Tp_Hs_E.Hs,CA1_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))
RMSE_CA2_INM_E_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA2_AWAC_INM_Tp_Hs_E.Hs,CA2_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))
RMSE_CA3_INM_E_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA3_AWAC_INM_Tp_Hs_E.Hs,CA3_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))

RMSE_CA1_INM_SE_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA1_AWAC_INM_Tp_Hs_SE.Hs,CA1_AWAC_INM_Tp_Hs_SE.Hs_AWAC)),2))
RMSE_CA2_INM_SE_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA2_AWAC_INM_Tp_Hs_SE.Hs,CA2_AWAC_INM_Tp_Hs_SE.Hs_AWAC)),2))
RMSE_CA3_INM_SE_Hs= (np.round(np.sqrt(metrics.mean_squared_error(CA3_AWAC_INM_Tp_Hs_SE.Hs,CA3_AWAC_INM_Tp_Hs_SE.Hs_AWAC)),2))

RMSE_CA1_INM_NE_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA1_AWAC_INM_Tp_Hs_NE.Tp,CA1_AWAC_INM_Tp_Hs_NE.Tp_AWAC)),2))
RMSE_CA2_INM_NE_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA2_AWAC_INM_Tp_Hs_NE.Tp,CA2_AWAC_INM_Tp_Hs_NE.Tp_AWAC)),2))
RMSE_CA3_INM_NE_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA3_AWAC_INM_Tp_Hs_NE.Tp,CA3_AWAC_INM_Tp_Hs_NE.Tp_AWAC)),2))

RMSE_CA1_INM_E_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA1_AWAC_INM_Tp_Hs_E.Tp,CA1_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))
RMSE_CA2_INM_E_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA2_AWAC_INM_Tp_Hs_E.Tp,CA2_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))
RMSE_CA3_INM_E_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA3_AWAC_INM_Tp_Hs_E.Tp,CA3_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))

RMSE_CA1_INM_SE_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA1_AWAC_INM_Tp_Hs_SE.Tp,CA1_AWAC_INM_Tp_Hs_SE.Tp_AWAC)),2))
RMSE_CA2_INM_SE_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA2_AWAC_INM_Tp_Hs_SE.Tp,CA2_AWAC_INM_Tp_Hs_SE.Tp_AWAC)),2))
RMSE_CA3_INM_SE_Tp= (np.round(np.sqrt(metrics.mean_squared_error(CA3_AWAC_INM_Tp_Hs_SE.Tp,CA3_AWAC_INM_Tp_Hs_SE.Tp_AWAC)),2))

CORR_CA1_INM_NE_Hs= (np.round((np.corrcoef(CA1_AWAC_INM_Tp_Hs_NE.Hs,CA1_AWAC_INM_Tp_Hs_NE.Hs_AWAC)),2))[0,1]
CORR_CA2_INM_NE_Hs= (np.round((np.corrcoef(CA2_AWAC_INM_Tp_Hs_NE.Hs,CA2_AWAC_INM_Tp_Hs_NE.Hs_AWAC)),2))[0,1]
CORR_CA3_INM_NE_Hs= (np.round((np.corrcoef(CA3_AWAC_INM_Tp_Hs_NE.Hs,CA3_AWAC_INM_Tp_Hs_NE.Hs_AWAC)),2))[0,1]

CORR_CA1_INM_E_Hs= (np.round((np.corrcoef(CA1_AWAC_INM_Tp_Hs_E.Hs,CA1_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))[0,1]
CORR_CA2_INM_E_Hs= (np.round((np.corrcoef(CA2_AWAC_INM_Tp_Hs_E.Hs,CA2_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))[0,1]
CORR_CA3_INM_E_Hs= (np.round((np.corrcoef(CA3_AWAC_INM_Tp_Hs_E.Hs,CA3_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))[0,1]

CORR_CA1_INM_SE_Hs= (np.round((np.corrcoef(CA1_AWAC_INM_Tp_Hs_SE.Hs,CA1_AWAC_INM_Tp_Hs_SE.Hs_AWAC)),2))[0,1]
CORR_CA2_INM_SE_Hs= (np.round((np.corrcoef(CA2_AWAC_INM_Tp_Hs_SE.Hs,CA2_AWAC_INM_Tp_Hs_SE.Hs_AWAC)),2))[0,1]
CORR_CA3_INM_SE_Hs= (np.round((np.corrcoef(CA3_AWAC_INM_Tp_Hs_SE.Hs,CA3_AWAC_INM_Tp_Hs_SE.Hs_AWAC)),2))[0,1]

CORR_CA1_INM_NE_Tp= (np.round((np.corrcoef(CA1_AWAC_INM_Tp_Hs_NE.Tp,CA1_AWAC_INM_Tp_Hs_NE.Tp_AWAC)),2))[0,1]
CORR_CA2_INM_NE_Tp= (np.round((np.corrcoef(CA2_AWAC_INM_Tp_Hs_NE.Tp,CA2_AWAC_INM_Tp_Hs_NE.Tp_AWAC)),2))[0,1]
CORR_CA3_INM_NE_Tp= (np.round((np.corrcoef(CA3_AWAC_INM_Tp_Hs_NE.Tp,CA3_AWAC_INM_Tp_Hs_NE.Tp_AWAC)),2))[0,1]

CORR_CA1_INM_E_Tp= (np.round((np.corrcoef(CA1_AWAC_INM_Tp_Hs_E.Tp,CA1_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))[0,1]
CORR_CA2_INM_E_Tp= (np.round((np.corrcoef(CA2_AWAC_INM_Tp_Hs_E.Tp,CA2_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))[0,1]
CORR_CA3_INM_E_Tp= (np.round((np.corrcoef(CA3_AWAC_INM_Tp_Hs_E.Tp,CA3_AWAC_INM_Tp_Hs_E.Hs_AWAC)),2))[0,1]

CORR_CA1_INM_SE_Tp= (np.round((np.corrcoef(CA1_AWAC_INM_Tp_Hs_SE.Tp,CA1_AWAC_INM_Tp_Hs_SE.Tp_AWAC)),2))[0,1]
CORR_CA2_INM_SE_Tp= (np.round((np.corrcoef(CA2_AWAC_INM_Tp_Hs_SE.Tp,CA2_AWAC_INM_Tp_Hs_SE.Tp_AWAC)),2))[0,1]
CORR_CA3_INM_SE_Tp= (np.round((np.corrcoef(CA3_AWAC_INM_Tp_Hs_SE.Tp,CA3_AWAC_INM_Tp_Hs_SE.Tp_AWAC)),2))[0,1]


#%%######################Try cor coeff for a dataframe#####################
AWAC_2019_NE=pd.concat([CA1_AWAC_INM_Tp_Hs_NE.Hs, CA1_AWAC_INM_Tp_Hs_NE.Tp,CA1_AWAC_INM_Tp_Hs_NE.Hs_AWAC, CA1_AWAC_INM_Tp_Hs_NE.Tp_AWAC, CA2_AWAC_INM_Tp_Hs_NE.Hs, CA2_AWAC_INM_Tp_Hs_NE.Tp,
                     CA2_AWAC_INM_Tp_Hs_NE.Hs_AWAC, CA2_AWAC_INM_Tp_Hs_NE.Tp_AWAC, CA3_AWAC_INM_Tp_Hs_NE.Hs, CA3_AWAC_INM_Tp_Hs_NE.Tp, CA3_AWAC_INM_Tp_Hs_NE.Hs_AWAC, CA3_AWAC_INM_Tp_Hs_NE.Tp_AWAC], axis=1)
AWAC_2019_NE.columns=('CA1_AWAC_INM.Hs', 'CA1_AWAC_INM.Tp','CA1_AWAC_INM.Hs_AWAC', 'CA1_AWAC_INM.Tp_AWAC', 'CA2_AWAC_INM.Hs', 'CA2_AWAC_INM.Tp',
                     'CA2_AWAC_INM.Hs_AWAC', 'CA2_AWAC_INM.Tp_AWAC', 'CA3_AWAC_INM.Hs', 'CA3_AWAC_INM.Tp', 'CA3_AWAC_INM.Hs_AWAC', 'CA3_AWAC_INM.Tp_AWAC')

AWAC_2019_E=pd.concat([CA1_AWAC_INM_Tp_Hs_E.Hs, CA1_AWAC_INM_Tp_Hs_E.Tp,CA1_AWAC_INM_Tp_Hs_E.Hs_AWAC, CA1_AWAC_INM_Tp_Hs_E.Tp_AWAC, CA2_AWAC_INM_Tp_Hs_E.Hs, CA2_AWAC_INM_Tp_Hs_E.Tp,
                     CA2_AWAC_INM_Tp_Hs_E.Hs_AWAC, CA2_AWAC_INM_Tp_Hs_E.Tp_AWAC, CA3_AWAC_INM_Tp_Hs_E.Hs, CA3_AWAC_INM_Tp_Hs_E.Tp, CA3_AWAC_INM_Tp_Hs_E.Hs_AWAC, CA3_AWAC_INM_Tp_Hs_E.Tp_AWAC], axis=1)
AWAC_2019_E.columns=('CA1_AWAC_INM.Hs', 'CA1_AWAC_INM.Tp','CA1_AWAC_INM.Hs_AWAC', 'CA1_AWAC_INM.Tp_AWAC', 'CA2_AWAC_INM.Hs', 'CA2_AWAC_INM.Tp',
                     'CA2_AWAC_INM.Hs_AWAC', 'CA2_AWAC_INM.Tp_AWAC', 'CA3_AWAC_INM.Hs', 'CA3_AWAC_INM.Tp', 'CA3_AWAC_INM.Hs_AWAC', 'CA3_AWAC_INM.Tp_AWAC')

AWAC_2019_SE=pd.concat([CA1_AWAC_INM_Tp_Hs_SE.Hs, CA1_AWAC_INM_Tp_Hs_SE.Tp,CA1_AWAC_INM_Tp_Hs_SE.Hs_AWAC, CA1_AWAC_INM_Tp_Hs_SE.Tp_AWAC, CA2_AWAC_INM_Tp_Hs_SE.Hs, CA2_AWAC_INM_Tp_Hs_SE.Tp,
                     CA2_AWAC_INM_Tp_Hs_SE.Hs_AWAC, CA2_AWAC_INM_Tp_Hs_SE.Tp_AWAC, CA3_AWAC_INM_Tp_Hs_SE.Hs, CA3_AWAC_INM_Tp_Hs_SE.Tp, CA3_AWAC_INM_Tp_Hs_SE.Hs_AWAC, CA3_AWAC_INM_Tp_Hs_SE.Tp_AWAC], axis=1)
AWAC_2019_SE.columns=('CA1_AWAC_INM.Hs', 'CA1_AWAC_INM.Tp','CA1_AWAC_INM.Hs_AWAC', 'CA1_AWAC_INM.Tp_AWAC', 'CA2_AWAC_INM.Hs', 'CA2_AWAC_INM.Tp',
                     'CA2_AWAC_INM.Hs_AWAC', 'CA2_AWAC_INM.Tp_AWAC', 'CA3_AWAC_INM.Hs', 'CA3_AWAC_INM.Tp', 'CA3_AWAC_INM.Hs_AWAC', 'CA3_AWAC_INM.Tp_AWAC')
fig, ax = plt.subplots(1,figsize=(30,30))
sns.heatmap(AWAC_2019_NE.corr(), mask=np.zeros_like(AWAC_2019_NE.corr(), dtype=np.bool),cmap='RdBu_r',annot=True, linewidths=.5, cbar_kws={'label': 'Correlation Coefficient'}, annot_kws={"fontsize": 12}, square=True, ax=ax)
plt.savefig('Cor_Matrix_Awacs_2019_NE.jpeg')

fig, ax = plt.subplots(1,figsize=(30,30))
sns.heatmap(AWAC_2019_E.corr(), mask=np.zeros_like(AWAC_2019_E.corr(), dtype=np.bool),cmap='RdBu_r',annot=True, linewidths=.5, cbar_kws={'label': 'Correlation Coefficient'}, annot_kws={"fontsize": 12}, square=True, ax=ax)
plt.savefig('Cor_Matrix_Awacs_2019_E.jpeg')

fig, ax = plt.subplots(1,figsize=(30,30))
sns.heatmap(AWAC_2019_SE.corr(), mask=np.zeros_like(AWAC_2019_SE.corr(), dtype=np.bool),cmap='RdBu_r',annot=True, linewidths=.5, cbar_kws={'label': 'Correlation Coefficient'}, annot_kws={"fontsize": 12}, square=True, ax=ax)
plt.savefig('Cor_Matrix_Awacs_2019_SE.jpeg')

#%%

os.chdir(r"O:\Beems_Share\04_Work_Package\Sizewell\TR317_Ed2\Data\Virtual_wave_buoy_analysis\Data\Final Results")
# 
data_NE= pd.ExcelFile(r'O:\Beems_Share\04_Work_Package\Sizewell\TR317_Ed2\Data\Virtual_wave_buoy_analysis\Data\Final Results\45 Bins\NE\data_CA3_INN_filt_dir_NE_new.xlsx')
data_NE= data_NE.parse('Sheet1')

data_E= pd.ExcelFile(r'O:\Beems_Share\04_Work_Package\Sizewell\TR317_Ed2\Data\Virtual_wave_buoy_analysis\Data\Final Results\45 Bins\E\data_CA2_INM_filt_dir_E_new.xlsx')
data_E= data_E.parse('Sheet1')

data_SE_Hs= pd.ExcelFile(r'O:\Beems_Share\04_Work_Package\Sizewell\TR317_Ed2\Data\Virtual_wave_buoy_analysis\Data\Final Results\45 Bins\SE\data_CA2_INM_filt_dir_SE_new.xlsx')
data_SE_Hs= data_SE_Hs.parse('Sheet1')

data_SE_Tp= pd.ExcelFile(r'O:\Beems_Share\04_Work_Package\Sizewell\TR317_Ed2\Data\Virtual_wave_buoy_analysis\Data\Final Results\45 Bins\SE\data_CA1_INS_filt_dir_SE_new.xlsx')
data_SE_Tp= data_SE_Tp.parse('Sheet1')

# 
# Hs Scatterplots
ax=sns.regplot(x="Hs_INN", y="Hs", data=data_NE, label='NE', color='b')
sns.regplot(x="Hs_INM", y="Hs Radar", data=data_E, label='E', color='r')
sns.regplot(x="Hs_INM", y="Hs Radar", data=data_SE_Hs, label='SE', color='g')
plt.xlabel("Hs AWAC (m)")
plt.ylabel("Hs Radar (m)")
plt.xlim(0.5, 3)
plt.xticks(np.arange(0.5, 3.5, 0.5))
plt.ylim(0.5, 4)
ax.plot([0, 1], [0, 1],'k--', linewidth=0.5, transform=ax.transAxes )
plt.legend()
plt.savefig('Hs_AWAC_Radar_NE_E_SE.jpeg')

# Tp Scatterplots
ax=sns.regplot(x="Tp_INN", y="Tp", data=data_NE, label='NE', color='b')
sns.regplot(x="Tp_INM", y="Tp", data=data_E, label='E', color='r')
sns.regplot(x="Tp_ISS", y="Tp", data=data_SE_Tp, label='SE', color='g')
ax.plot([0, 1], [0, 1],'k--', linewidth=0.5, transform=ax.transAxes )
plt.xlabel("Tp AWAC (s)")
plt.ylabel("Tp Radar (s)")
plt.xlim(3, 11)
plt.xticks(np.arange(3, 12, 1))
plt.ylim(3, 12)
plt.legend()
plt.savefig('Tp_AWAC_Radar_NE_E_SE.jpeg')

# Do then the scatterplots with the corrected versions and add also the 1-1 line

ax=sns.regplot(x="Hs_INN", y="Hs_New", data=data_NE, label='NE', color='b')
ax.plot([0, 1], [0, 1],'k--', linewidth=0.5, transform=ax.transAxes )
sns.regplot(x="Hs_INM", y="Hs_new", data=data_E, label='E', color='r')
sns.regplot(x="Hs_INM", y="Hs_new", data=data_SE_Hs, label='SE', color='g')
plt.xlabel("Hs AWAC (m)")
plt.ylabel("Hs Cor. (m)")
plt.xlim(0.5, 3)
plt.xticks(np.arange(0.5, 3.5, 0.5))
plt.ylim(0.5, 3)
plt.legend()
plt.savefig('Hs_AWAC_Cor_NE_E_SE.jpeg')

# Tp Scatterplots
ax=sns.regplot(x="Tp_INN", y="Tp_New", data=data_NE, label='NE', color='b')
sns.regplot(x="Tp_INM", y="Tp new", data=data_E, label='E', color='r')
sns.regplot(x="Tp_ISS", y="Tp new", data=data_SE_Tp, label='SE', color='g')
ax.plot([0, 1], [0, 1],'k--', linewidth=0.5, transform=ax.transAxes )
plt.xlabel("Tp AWAC (s)")
plt.ylabel("Tp Cor. (s)")
plt.xlim(3, 11)
plt.xticks(np.arange(3, 12, 1))
plt.ylim(3, 11)
plt.legend()
plt.savefig('Tp_AWAC_Radar_NE_E_SE_cor.jpeg')






