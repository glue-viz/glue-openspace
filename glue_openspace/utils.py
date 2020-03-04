import tempfile

from astropy import units as u
from astropy.coordinates import SkyCoord

from matplotlib.colors import ColorConverter

__all__ = ['generate_cmap_table', 'data_to_speck']

to_rgb = ColorConverter().to_rgb

def generate_cmap_table(color):

    tmpfile = tempfile.mktemp(suffix='.cmap')

    r, g, b = to_rgb(color)

    with open(tmpfile, 'w') as f:

        f.write('256\n')
        for i in range(256):
            f.write('{0:8.6f} {1:8.6f} {2:8.6f} {3:8.6f}\n'.format(r, g, b, 1))

    return tmpfile


def data_to_speck(data, lon_att, lat_att, alt_att=None, frame=None, alt_unit=None):

    # TODO: add support for different units, e.g. hour angle

    lon = data[lon_att]
    lat = data[lat_att]

    if alt_att is None:

        # Get cartesian coordinates on unit galactic sphere
        coord = SkyCoord(lon, lat, unit='deg',
                         frame=frame.lower())
        x, y, z = coord.galactic.cartesian.xyz

        # Convert to be on a sphere of radius 100pc
        D = 100
        x *= D
        y *= D
        z *= D

    else:

        distance = data[alt_att]

        # Get cartesian coordinates on unit galactic sphere
        coord = SkyCoord(lon * u.deg, lat * u.deg,
                         distance=distance * u.Unit(alt_unit),
                         frame=frame.lower())
        x, y, z = coord.galactic.cartesian.xyz

        x = x.to_value(u.pc)
        y = y.to_value(u.pc)
        z = z.to_value(u.pc)

    # Create speck table

    tmpfile = tempfile.mktemp(suffix='.speck')

    with open(tmpfile, 'w') as f:

        f.write('datavar 0 colorb_v\n')
        f.write('datavar 1 lum\n')
        f.write('datavar 2 absmag\n')
        f.write('datavar 3 appmag\n')

        for i in range(len(x)):
            f.write('  {0:10.5f} {1:10.5f} {2:10.5f} {3:10.5f} {4:10.5f} {5:10.5f} {6:10.5f}\n'.format(x[i], y[i], z[i], 0., 100., 0., 0.))

    return tmpfile

def generate_openspace_message(script_function, script_arguments):
    message = {"topic":4,
                   "type": "luascript",
                   "payload": {"function": script_function,
                               "arguments":script_arguments,
                               "return": False}}
    return message