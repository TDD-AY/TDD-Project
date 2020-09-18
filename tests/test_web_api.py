import pytest   
from tassi.web_api import server

@pytest.fixture
def client():
    server.app.config['TESTING'] = True

    with server.app.test_client() as client:
        yield client

def test_health(client):

    rv = client.get('/health')
    assert rv.data == b'Up and running'