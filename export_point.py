import netCDF4 as nc
from scipy import interpolate

from pathlib import Path
import json
import yaml


fesdir = 'ocean_tide_extrapolated'
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
    point = (site['latitude'], site['longitude']+360)
    data = []
    for path in pathlist:
        # print(path)
        constname = path.stem
        if constname == 'la2':
            constname = 'lam2'
    
        ds = nc.Dataset(path)
        phase = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['phase'], point ) [0]
        ampl = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['amplitude'], point )[0]
        print(f' {sitename} {constname} {ampl}, {phase}')
        data.append({'name':constname.upper(), 'amplitude':ampl, 'phase':phase})

    dfile = site['datafile']
    with open(f'tidesite/assets/{dfile}', 'w') as f:
        json.dump(data, f)
