import pytest
from tassi.database.model import Ruta
from tassi.telegram_bot.bot import store_location
from tassi.database.errors import InvalidEntry
from haversine import haversine
from math import isclose


USER_ID = 1
MESSAGE_ID = 11

def test_add_entry_correct():

    # add route to the database
    store_location(USER_ID, MESSAGE_ID, {"longitude": 1.0, "latitude": 2.0})

    route = Ruta.select().order_by(Ruta.id.desc()).get()

    assert route.trajectory[0].get("longitude") == 1.0
    assert route.trajectory[0].get("latitude") == 2.0
    assert route.user == USER_ID

    # undo changes

    Ruta.delete().where(Ruta.message == MESSAGE_ID).execute()


def test_add_entry_when_already_exists():

    # add route to the database
    store_location(USER_ID, MESSAGE_ID, {"longitude": 1.0, "latitude": 2.0})
    store_location(USER_ID, MESSAGE_ID, {"longitude": 3.0, "latitude": 4.0})

    route = Ruta.select().order_by(Ruta.id.desc()).get()

    assert len(route.trajectory) == 2

    # undo changes
    Ruta.delete().where(Ruta.message == MESSAGE_ID).execute()


def test_add_distance_when_adding_entry():

    store_location(USER_ID, MESSAGE_ID, {"longitude": 1.0, "latitude": 2.0})
    store_location(USER_ID, MESSAGE_ID, {"longitude": 3.0, "latitude": 4.0})
    store_location(USER_ID, MESSAGE_ID, {"longitude": 7.0, "latitude": 9.0})

    route = Ruta.select().order_by(Ruta.id.desc()).get()

    pos1 = (1.0, 2.0)
    pos2 = (3.0, 4.0)
    pos3 = (7.0, 9.0)

    assert isclose(route.distance, haversine(pos1,pos2)+haversine(pos2,pos3), abs_tol=0.1)

    # undo changes
    Ruta.delete().where(Ruta.message == MESSAGE_ID).execute()


def test_add_with_no_coordinates():

    with pytest.raises(InvalidEntry):
        assert store_location(USER_ID, MESSAGE_ID, {})


def test_add_with_invalid_coordinates():

    with pytest.raises(InvalidEntry):
        assert store_location(USER_ID, MESSAGE_ID, {"longitude": "a", "latitude": "b"})
