import netCDF4 as nc
from scipy import interpolate

from pathlib import Path
import json

dir = 'ocean_tide_extrapolated'

pathlist = Path(dir).glob('**/*.nc')
#point = (63, 23)
# Reykjavík : 
point = (64.166535, -21.972971+360)

data = []
for path in pathlist:
    constname = path.stem
    if constname == 'la2':
        constname = 'lam2'

    ds = nc.Dataset(path)
    phase = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['phase'], point ) [0]

    ampl = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['amplitude'], point )[0]

    print(f' {constname} {ampl}, {phase}')
    data.append({'name':constname.upper(), 'amplitude':ampl, 'phase':phase})


with open('rvk.json', 'w') as f:
    json.dump(data, f)
