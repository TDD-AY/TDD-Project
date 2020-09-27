import os
from playhouse.postgres_ext import *
import pytest
from dotenv import load_dotenv  

load_dotenv()

@pytest.fixture
def db():

    DB_NAME = os.environ.get("DB_NAME")
    USER_TDB = os.environ.get("USER_TDB")
    PASS_TDB = os.environ.get("PASS_TDB")
    HOST = os.environ.get("DB_HOST") or "localhost"
    db = PostgresqlExtDatabase(DB_NAME, user=USER_TDB, password=PASS_TDB, host=HOST)

    class BaseModel(Model):

        Pilar=IntegerField()
        alex=FloatField()
        juanjo=BigIntegerField()
        Yabir=BigIntegerField()
        team=TextField()

        class Meta:
            database = db  
    
    db.create_tables([BaseModel])

    yield BaseModel


def test_insert(db):
    db.create(
        Pilar=10,
        alex=0.5,
        juanjo= 476576889780,
        Yabir=68786490979856745,
        team="super team"
    )

    assert db.select().where(db.Pilar==10) != None
    
    db.drop_table()

