from __future__ import absolute_import, division, print_function

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'undefined'


def setup():
    from .viewer import OpenSpaceDataViewer
    from glue.config import qt_client
    qt_client.add(OpenSpaceDataViewer)
