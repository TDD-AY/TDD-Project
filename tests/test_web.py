from datetime import datetime
import json
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

    coordinates1=[{"longitude":2.2,"latitude":3.5,"datetime": 34676},{"longitude":6.8,"latitude":7.4,"datetime": 47580}]
    coordinates2=[{"longitude":4.7,"latitude":1.9,"datetime": 30000}]

    time1 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

    Ruta.create(
        user= USER_ID1, 
        message = MESSAGE_ID1, 
        date = time1, 
        trajectory = coordinates1
    )

    time2 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

    Ruta.create(
        user= USER_ID1, 
        message = MESSAGE_ID2, 
        date = time2, 
        trajectory = coordinates2
    )

    rutas=[{"user":USER_ID1,"message":MESSAGE_ID1,"date": time1, "trajectory": coordinates1},
    {"user":USER_ID1,"message":MESSAGE_ID2,"date": time2, "trajectory": coordinates2}]

    rv = json.loads(client.get(f'/api/v1/{USER_ID1}/my-routes').data)

    for i, ruta in enumerate(rutas):
        assert sorted(ruta.items()) == sorted(rv[i].items())                       

    #Undo changes in the database
    Ruta.delete().where(Ruta.message == MESSAGE_ID1).execute()
    Ruta.delete().where(Ruta.message == MESSAGE_ID2).execute()


def test_emptyness(client):
    
    rv = json.loads(client.get(f'/api/v1/{USER_ID1}/my-routes').data)

    assert len(rv)==0

def test_get_route_by_id(client):
        
    #Create a route
    coordinates1=[{"longitude":2.2,"latitude":3.5,"datetime": 34676},{"longitude":6.8,"latitude":7.4,"datetime": 47580}]
    time1 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    distance, time = 46, 6

    Ruta.create(
        user= USER_ID1, 
        message = MESSAGE_ID1, 
        date = time1, 
        trajectory = coordinates1,
        distance = distance,
        time = time
    )


    ruta={"distance_total":distance,"time":time,"date": time1}

    rv = json.loads(client.get(f'/api/v1/{USER_ID1}/route/{MESSAGE_ID1}').data)

    assert sorted(ruta.items()) == sorted(rv.items())

    #TO-DO: checkout that the values are correct                       


    #Undo changes in the database
    Ruta.delete().where(Ruta.message == MESSAGE_ID1).execute()

def test_delete_route_by_id(client):
    
    #Create a route
    coordinates1=[{"longitude":2.2,"latitude":3.5,"datetime": 34676},{"longitude":6.8,"latitude":7.4,"datetime": 47580}]
    
    Ruta.create(
        user= USER_ID1, 
        message = MESSAGE_ID1, 
        date = datetime.now(), 
        trajectory = coordinates1
    )

    client.post(f'/api/v1/{USER_ID1}/route/{MESSAGE_ID1}')
    assert Ruta.get_or_none(message = MESSAGE_ID1 )==None 