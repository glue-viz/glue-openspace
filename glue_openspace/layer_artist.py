import os
import json
import uuid
import time

import numpy as np
from astropy import units as u
from glue.core import Data, Subset

from glue.viewers.common.layer_artist import LayerArtist

from .layer_state import OpenSpaceLayerState
from .utils import data_to_speck, generate_cmap_table

__all__ = ['OpenSpaceLayerArtist']

TEXTURE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'halo.png'))

# Time to wait after sending websocket message
WAIT_TIME = 0.2


class OpenSpaceLayerArtist(LayerArtist):

    _layer_state_cls = OpenSpaceLayerState

    def __init__(self, viewer, *args, **kwargs):

        super(OpenSpaceLayerArtist, self).__init__(*args, **kwargs)

        self._viewer = viewer

        self.state.add_global_callback(self._on_attribute_change)
        self._viewer_state.add_global_callback(self._on_attribute_change)

        self._uuid = None

    @property
    def websocket(self):
        return self._viewer.websocket

    # def _on_visible_change(self, value=None):
    #     self.artist.set_visible(self.state.visible)
    #     self.redraw()
    #
    # def _on_zorder_change(self, value=None):
    #     self.artist.set_zorder(self.state.zorder)
    #     self.redraw()

    def _on_attribute_change(self, *args, **kwargs):

        force = kwargs.get('force', False)

        if self.websocket is None:
            return

        if self._viewer_state.lon_att is None or self._viewer_state.lat_att is None:
            return

        changed = self.pop_changed_properties()

        if len(changed) == 0 and not force:
            return
        
        self.clear()

        if not self.state.visible:
            return

        try:
            tmpfile = data_to_speck(self.state.layer,
                                    self._viewer_state.lon_att,
                                    self._viewer_state.lat_att,
                                    alt_att=self._viewer_state.alt_att,
                                    alt_unit=self._viewer_state.alt_unit,
                                    frame=self._viewer_state.frame)
        except Exception as exc:
            print(str(exc))
            return

        if isinstance(self.state.layer, Subset) and np.sum(self.state.layer.to_mask()) == 0:
            return

        self._uuid = str(uuid.uuid4())

        cmap_table = generate_cmap_table(self.state.color)

        # For now, the size of the points in OpenSpace is absolute, so we need to include
        # some scaling based on the largest absolute distance in the data.
        maxdist = np.nanmax(self.state.layer[self._viewer_state.alt_att]) * u.Unit(self._viewer_state.alt_unit)
        magexp = 5 + np.log10(maxdist / (1 * u.pc)).value

        magexp += np.log10(self.state.size * self.state.size_scaling)

        message = {"topic":4,
                   "type": "luascript",
                   "payload": {"function": "openspace.addSceneGraphNode",
                               "arguments":[{"Identifier": self._uuid,
                                             "Parent": "Root",
                                             "Renderable": {"Type": "RenderableStars",
                                                                    "File": tmpfile,
                                                                    "Texture": TEXTURE,
                                                                    "MagnitudeExponent": magexp,
                                                                    "ColorMap": cmap_table,
                                                                    "SizeComposition": "Distance Modulus",
                                                                    "RenderMethod": "Texture Based"},
                                              "GUI":{"Path": "/Milky Way/Stars"}}],
                               "return": False}}

        self.websocket.send(json.dumps(message).encode('ascii'))

        # Wait for a short time to avoid sending too many messages in quick succession
        time.sleep(WAIT_TIME)

    def clear(self):
        if self.websocket is None:
            return
        if self._uuid is None:
            return
        message = {"topic": 4,
                   "type": "luascript",
                   "payload": {"function": "openspace.removeSceneGraphNode",
                               "arguments": [self._uuid],
                               "return": False}}

        self.websocket.send(json.dumps(message).encode('ascii'))
        self._uuid = None

        # Wait for a short time to avoid sending too many messages in quick succession
        time.sleep(WAIT_TIME)

    def update(self):
        if self.websocket is None:
            return
        # self._on_fill_change()
        self._on_attribute_change(force=True)
