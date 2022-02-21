import netCDF4 as nc
from scipy import interpolate

from pathlib import Path

dir = 'ocean_tide_extrapolated'

pathlist = Path(dir).glob('**/*.nc')
point = (63, 23)
for path in pathlist:
    constname = path.stem
    if constname == 'la2':
        constname = 'lambda2'

    ds = nc.Dataset(path)
    phase = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['phase'], point ) [0]

    ampl = interpolate.interpn((ds.variables['lat'], ds.variables['lon']), ds.variables['amplitude'], point )[0]

    print(f' {constname} {ampl}, {phase}')

