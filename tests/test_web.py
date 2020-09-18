from datetime import datetime
import pytest   
from tassi.web_api import server
from tassi.database.model import Ruta


USER_ID1=2
USER_ID2=4
MESSAGE_ID1=6
MESSAGE_ID2=34

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
                    message = MESSAGE_ID1, 
                    date = time1, 
                    trajectory = coordinates1
                )

    time2=datetime.now()

    Ruta.create(
                    user= USER_ID1, 
                    message = MESSAGE_ID2, 
                    date = time2, 
                    trajectory = coordinates2
                )

    rutas=[{"user":USER_ID1,"message":MESSAGE_ID1,"date": time1, "trajectory": coordinates1},
    {"user":USER_ID1,"message":MESSAGE_ID2,"date": time2, "trajectory": coordinates2}]

    rv = client.get(f'/api/v1/{USER_ID1}/my-routes')
    assert sorted(rutas.items()) == sorted(rv.data.items())                       

    #Undo changes in the database
    Ruta.delete().where(Ruta.message == MESSAGE_ID1).execute()
    Ruta.delete().where(Ruta.message == MESSAGE_ID2).execute()


def test_emptyness(client):
    
    rv = client.get(f'/api/v1/{USER_ID1}/my-routes')

    assert len(rv.data)==0

def test_get_route_by_id(client):
        
    #Create some routes 
    coordinates1=[{"longitude":2.2,"latitude":3.5},{"longitude":6.8,"latitude":7.4}]
    time1=datetime.now()

    Ruta.create(
                    user= USER_ID1, 
                    message = MESSAGE_ID1, 
                    date = time1, 
                    trajectory = coordinates1
                )


    ruta={"distance_total":46,"time":6,"date": time1,"speed_km":47,"speed_average":44 }

    rv = client.get(f'/api/v1/{USER_ID1}/route/{MESSAGE_ID1}')
    assert sorted(ruta.items()) == sorted(rv.data.items())

    #TO-DO: checkout that the values are correct                       


    #Undo changes in the database
    Ruta.delete().where(Ruta.message == MESSAGE_ID1).execute()

def test_delete_route_by_id(client):
    
    #Create a route
    coordinates1=[{"longitude":2.2,"latitude":3.5},{"longitude":6.8,"latitude":7.4}]
    
    Ruta.create(
                    user= USER_ID1, 
                    message = MESSAGE_ID1, 
                    date = datetime.now(), 
                    trajectory = coordinates1
                )

    client.delete(f'/api/v1/{USER_ID1}/route/{MESSAGE_ID1}')
    assert Ruta.get_or_none(message = MESSAGE_ID1 )==None 