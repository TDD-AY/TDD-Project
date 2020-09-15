import os
from dotenv import load_dotenv
import json
from playhouse.postgres_ext import *

from datetime import datetime

DB_NAME = os.environ.get("DB_NAME")
USER_TDB = os.environ.get("USER_TDB")
PASS_TDB = os.environ.get("PASS_TDB")
db = PostgresqlExtDatabase('trabotories_db', user='tdb', password='tdb')

#Ruta hereda de la clase Model, que tiene implementada las funcionalidades de peewee
class Ruta(Model):

    user = IntegerField()
    date = DateTimeField()
    trajectory = JSONField()
    time = IntegerField( null=True )
    distance = FloatField( null=True )

    class Meta:
        database = db

def test_db():
    Ruta.create(
        user = 1,
        date = datetime.now(),
        trajectory = {"lat":1.0, "long":1.0}
    )

if __name__ == "__main__":
    load_dotenv()
    db.create_tables( [Ruta] )
    test_db()
