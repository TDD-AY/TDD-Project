import pytest
from database.model import Ruta
from telegram_bot.bot import store_location
from database.errors import InvalidEntry


USER_ID = 1
MESSAGE_ID = 10

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

def test_add_with_no_coordinates():
    
    with pytest.raises(InvalidEntry):
        assert store_location(USER_ID, MESSAGE_ID, {})

def test_add_with_invalid_coordinates():
    
    with pytest.raises(InvalidEntry):
        assert store_location(USER_ID, MESSAGE_ID, {"longitude": "a", "latitude": "b"})