import netCDF4 as nc
from scipy import interpolate
import numpy as np

from pathlib import Path
import json
import yaml

gridfile = 'grid_tpxo9_atlas_30_v5.nc'  
h_const = dict()
u_const = dict()
h_const['2n2']= 'h_2n2_tpxo9_atlas_30_v5.nc'
h_const['k1'] = 'h_k1_tpxo9_atlas_30_v5.nc'
h_const['k2'] = 'h_k2_tpxo9_atlas_30_v5.nc'
h_const['m2'] = 'h_m2_tpxo9_atlas_30_v5.nc'
h_const['m4'] = 'h_m4_tpxo9_atlas_30_v5.nc'
h_const['mf'] = 'h_mf_tpxo9_atlas_30_v5.nc'
h_const['mm'] = 'h_mm_tpxo9_atlas_30_v5.nc'
h_const['mn4']= 'h_mn4_tpxo9_atlas_30_v5.nc'
h_const['ms3']= 'h_ms4_tpxo9_atlas_30_v5.nc'
h_const['n2'] = 'h_n2_tpxo9_atlas_30_v5.nc'
h_const['o1'] = 'h_o1_tpxo9_atlas_30_v5.nc'
h_const['p1'] = 'h_p1_tpxo9_atlas_30_v5.nc'
h_const['q1'] = 'h_q1_tpxo9_atlas_30_v5.nc'
h_const['s1'] = 'h_s1_tpxo9_atlas_30_v5.nc'
h_const['s2'] = 'h_s2_tpxo9_atlas_30_v5.nc'
u_const['2n2']= 'u_2n2_tpxo9_atlas_30_v5.nc'
u_const['k1'] = 'u_k1_tpxo9_atlas_30_v5.nc'
u_const['k2'] = 'u_k2_tpxo9_atlas_30_v5.nc'
u_const['m2'] = 'u_m2_tpxo9_atlas_30_v5.nc'
u_const['m4'] = 'u_m4_tpxo9_atlas_30_v5.nc'
u_const['mf'] = 'u_mf_tpxo9_atlas_30_v5.nc'
u_const['mm'] = 'u_mm_tpxo9_atlas_30_v5.nc'
u_const['mn4']= 'u_mn4_tpxo9_atlas_30_v5.nc'
u_const['ms4']= 'u_ms4_tpxo9_atlas_30_v5.nc'
u_const['n2'] = 'u_n2_tpxo9_atlas_30_v5.nc'
u_const['o1'] = 'u_o1_tpxo9_atlas_30_v5.nc'
u_const['p1'] = 'u_p1_tpxo9_atlas_30_v5.nc'
u_const['q1'] = 'u_q1_tpxo9_atlas_30_v5.nc'
u_const['s1'] = 'u_s1_tpxo9_atlas_30_v5.nc'
u_const['s2'] = 'u_s2_tpxo9_atlas_30_v5.nc'

fesdir = '/home/indridi/dev/tides/TPXO9_atlas_v5_nc'
yamlfile = 'tidesite/_data/tidesites.yml'

with open(yamlfile) as f:
    sites = yaml.safe_load(f)
    print(sites)

#point = (63, 23)
# Reykjavík : 
for site in sites:
    print(site)
    pathlist = Path(fesdir).glob('**/*.nc')
    sitename = site['sitename']
    # point = (site['latitude'], site['longitude']+360)
    point = (site['longitude']+360, site['latitude'])
    data = []
    data_u = []
    data_v = []
    # for path in pathlist:
    for cname in h_const:
        fname = h_const[cname]
        path = Path(fesdir+"/"+fname)
        ds = nc.Dataset(path)

        imag = interpolate.interpn((ds.variables['lon_z'], ds.variables['lat_z']), ds.variables['hIm'], point, fill_value=None ) [0]
        real = interpolate.interpn((ds.variables['lon_z'], ds.variables['lat_z']), ds.variables['hRe'], point , fill_value=None) [0]
        ampl=np.sqrt(real**2+imag**2)
        phase=np.arctan2(-imag,real)/np.pi*180
        # ampl = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['amplitude'], point )[0]
        # print(f' {sitename} {cname} {ampl}, {phase}')
        data.append({'name':cname.upper(), 'amplitude':ampl, 'phase':phase})

    gridpath = Path(fesdir+"/"+gridfile)
    ds = nc.Dataset(gridpath)
    depth_v = interpolate.interpn((ds.variables['lon_v'], ds.variables['lat_v']), ds.variables['hv'], point, fill_value=None ) [0]
    depth_u = interpolate.interpn((ds.variables['lon_u'], ds.variables['lat_u']), ds.variables['hu'], point, fill_value=None ) [0]

    data_v.append({'sitename': sitename, 'depth': depth_v})
    data_u.append({'sitename': sitename, 'depth': depth_u})

    for cname in u_const:
        fname = u_const[cname]
        path = Path(fesdir+"/"+fname)
        ds = nc.Dataset(path)

        uimag = interpolate.interpn((ds.variables['lon_u'], ds.variables['lat_u']), ds.variables['uIm'], point, fill_value=None ) [0]
        ureal = interpolate.interpn((ds.variables['lon_u'], ds.variables['lat_u']), ds.variables['uRe'], point , fill_value=None) [0]
        vimag = interpolate.interpn((ds.variables['lon_v'], ds.variables['lat_v']), ds.variables['vIm'], point, fill_value=None ) [0]
        vreal = interpolate.interpn((ds.variables['lon_v'], ds.variables['lat_v']), ds.variables['vRe'], point , fill_value=None) [0]
        uampl=np.sqrt(ureal**2+uimag**2)
        uphase=np.arctan2(-uimag, ureal)/np.pi*180

        vampl=np.sqrt(vreal**2+vimag**2)
        vphase=np.arctan2(-vimag, vreal)/np.pi*180
        # ampl = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['amplitude'], point )[0]
        # print(f' {sitename} {cname} {vampl}, {vphase} {uampl}, {uphase}')
        data_u.append({'name':cname.upper(), 'amplitude':uampl, 'phase':uphase})
        data_v.append({'name':cname.upper(), 'amplitude':vampl, 'phase':vphase})

    dfile = site['datafile']
    print(f'datafile : {dfile}')
    with open(f'tidesite/assets/{dfile}.json', 'w') as f:
        json.dump(data, f)
    with open(f'tidesite/assets/{dfile}_u.json', 'w') as f:
        json.dump(data_u, f)
    with open(f'tidesite/assets/{dfile}_v.json', 'w') as f:
        json.dump(data_v, f)
