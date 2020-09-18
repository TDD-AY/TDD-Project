import pytest   
from tassi.web_api import server
from tassi.database.model import Ruta

USER_ID1=2
USER_ID2=4

@pytest.fixture
def client():
    server.app.config['TESTING'] = True

    with server.app.test_client() as client:
        yield client

def test_health(client):

    rv = client.get('/health')
    assert rv.data == b'Up and running' 

def test_get_routes(client):

    #Create some routes 

    coordinates1=[{"longitude":2.2,"latitude":3.5},{"longitude":6.8,"latitude":7.4}]
    coordinates2=[{"longitude":4.7,"latitude":1.9}]
   
    time1=datetime.now()

    Ruta.create(
                    user= USER_ID1, 
                    message = 6, 
                    date = time1, 
                    trajectory = coordinates1
                )

    time2=datetime.now()

    Ruta.create(
                    user= USER_ID1, 
                    message = 34, 
                    date = time2, 
                    trajectory = coordinates2
                )

    rutas=[{"user":USER_ID1,"message":6,"date": time1, "trajectory": coordinates1},
    {"user":USER_ID1,"message":34,"date": time2, "trajectory": coordinates2}]

    rv = client.get(f'/api/v1/{USER_ID1}/my-routes')
    assert sorted(rutas.items()) == sorted(rv.data.items())                       

    #Undo changes in the database
    Ruta.delete().where(Ruta.message == 6).execute()
    Ruta.delete().where(Ruta.message == 34).execute()


def test_emptyness(client):
    
    rv = client.get(f'/api/v1/{USER_ID1}/my-routes')

    assert len(rv.data)==0
