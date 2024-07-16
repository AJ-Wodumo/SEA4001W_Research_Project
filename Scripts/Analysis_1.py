#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:06:32 2024

@author: student

This is just to play around with the netcdf file, improve the analysis

nino years

2014 (weak)
2015 (strongest ever recorded)
2016 (strongest ever recorded)
2019

nina years 

2017
2018
2020
2021
2022

"""

### Import modules

import xarray as xr
import cartopy as ccrs
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np

### Open file

filename = '../Data/ERA5_SST_wind.nc'
wind_sst = xr.open_dataset(filename)
print(wind_sst)

### Variables

lon = wind_sst['longitude']
lat = wind_sst['latitude']
time = wind_sst['time']
u10 = wind_sst['u10']
v10 = wind_sst['v10']
sst = wind_sst['sst'] - 273

### Region of interest

lon_min = 5
lon_max = 60
lat_min = -10 
lat_max = -40 

time_min = '2015-12-01'
time_max = '2016-02-01'

sa_sst = sst.sel(longitude=slice(lon_min, lon_max), latitude=slice(lat_min, lat_max),time=slice(time_min, time_max))
sa_uwind = u10.sel(longitude=slice(lon_min, lon_max), latitude=slice(lat_min, lat_max),time=slice(time_min, time_max) )
sa_vwind = v10.sel(longitude=slice(lon_min, lon_max), latitude=slice(lat_min, lat_max),time=slice(time_min, time_max))
sa_lon = lon.sel(longitude=slice(lon_min, lon_max))
sa_lat = lat.sel(latitude=slice(lat_min, lat_max))


### Plot data - we're gonna look from December 2014 - February 2015

## Figure properties

xdim = 10
ydim = 6
colormap = 'viridis'
extents = [lon_min, lon_max, lat_min, lat_max]
title = 'Southern Africa SST - Nov 2015 - Feb 2016'
contours = np.linspace(15, 31, 10)

## Actual plot

fig, ax = plt.subplots(figsize=(xdim, ydim), subplot_kw={'projection': ccrs.PlateCarree()})
m = ax.pcolor(sa_lon, sa_lat, sa_sst.mean(dim='time'), cmap=colormap, transform=ccrs.PlateCarree())
contours = ax.contour(sa_lon, sa_lat, sa_sst.mean(dim='time'), levels=contours, colors='black', transform=ccrs.PlateCarree())
ax.clabel(contours, inline=True, fontsize=8)
ax.set_extent(extents, crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.COASTLINE)
gl = ax.gridlines(draw_labels=True)
gl.right_labels = False
gl.top_labels = False


# Colourbar

cbar = plt.colorbar(m, ax=ax, orientation='vertical')
cbar.set_label('SST in degrees Celsius (degC)')

# Title

plt.suptitle(title, fontsize = 20)
plt.show()