import pytest
from mock import patch

from glue.core import Data
from glue.app.qt import GlueApplication
from glue_openspace.viewer import OpenSpaceDataViewer


class FakeWebSocketServer:
    def __init__(self):
        self.messages = []
    def send(self, message):
        self.messages.append(message)
    def clear(self):
        self.messages[:] = []


@pytest.fixture
def websocket_server(request):
    server = FakeWebSocketServer()
    with patch('glue_openspace.viewer.create_connection',
               return_value=server):
        yield server


class TestOpenSpaceViewer:

    def setup_method(self, method):

        self.data1 = Data(label='d1', x=[3.4, 2.3, -1.1, 0.3],
                          y=[3.2, 3.3, 3.4, 3.5], z=['a', 'b', 'c', 'a'])
        self.data2 = Data(label='d1', x=[3.4, 2.3, -1.1, 0.3],
                          y=[3.2, 3.3, 3.4, 3.5], z=['a', 'b', 'c', 'a'])

        self.app = GlueApplication()

        self.data_collection = self.app.session.data_collection
        self.data_collection.append(self.data1)
        self.data_collection.append(self.data2)

        self.viewer = self.app.new_data_viewer(OpenSpaceDataViewer)

    def test_add_single_data(self, websocket_server):
        self.viewer.connect_to_openspace()
        assert len(websocket_server.messages) == 0
        self.viewer.add_data(self.data1)
        assert len(websocket_server.messages) == 1 
