import os
import json
import uuid

import numpy as np
from glue.core import Data, Subset

from glue.viewers.common.layer_artist import LayerArtist

from .state import OpenSpaceLayerState
from .utils import data_to_speck, generate_cmap_table

__all__ = ['OpenSpaceLayerArtist']


TEXTURE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'halo.png'))


class OpenSpaceLayerArtist(LayerArtist):

    _layer_state_cls = OpenSpaceLayerState

    def __init__(self, websocket, *args, **kwargs):

        super(OpenSpaceLayerArtist, self).__init__(*args, **kwargs)

        self.websocket = websocket

        # self.state.add_callback('fill', self._on_fill_change)
        self.state.add_callback('visible', self._on_attribute_change)
        # self.state.add_callback('zorder', self._on_zorder_change)

        self._viewer_state.add_callback('ra_att', self._on_attribute_change)
        self._viewer_state.add_callback('dec_att', self._on_attribute_change)
        self._viewer_state.add_callback('distance_att', self._on_attribute_change)

        self._uuid = str(uuid.uuid4())

    # def _on_visible_change(self, value=None):
    #     self.artist.set_visible(self.state.visible)
    #     self.redraw()
    #
    # def _on_zorder_change(self, value=None):
    #     self.artist.set_zorder(self.state.zorder)
    #     self.redraw()

    def _on_attribute_change(self, value=None):

        if self._viewer_state.ra_att is None or self._viewer_state.dec_att is None:
            return

        self.clear()

        if not self.state.visible:
            return

        try:
            tmpfile = data_to_speck(self.state.layer,
                                    self._viewer_state.ra_att,
                                    self._viewer_state.dec_att)
        except Exception:
            return

        if isinstance(self.state.layer, Subset) and np.sum(self.state.layer.to_mask()) == 0:
            print("SKIPPING EMPTY SUBSET")
            return

        self._uuid = str(uuid.uuid4())

        cmap_table = generate_cmap_table(self.state.color)

        if isinstance(self.state.layer, Data):
            magexp = 6.2
        else:
            magexp = 7.0

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

    def clear(self):
        if self._uuid is None:
            return
        message = {"topic": 4,
                   "type": "luascript",
                   "payload": {"function": "openspace.removeSceneGraphNode",
                               "arguments": [self._uuid],
                               "return": False}}
        print(message)
        self.websocket.send(json.dumps(message).encode('ascii'))
        self._uuid = None

    def update(self):
        # self._on_fill_change()
        self._on_attribute_change()
