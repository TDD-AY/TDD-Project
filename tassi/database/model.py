import os
from dotenv import load_dotenv
import json
from playhouse.postgres_ext import *

from datetime import datetime

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
USER_TDB = os.environ.get("USER_TDB")
PASS_TDB = os.environ.get("PASS_TDB")
HOST = os.environ.get("DB_HOST") or "localhost"
db = PostgresqlExtDatabase(DB_NAME, user=USER_TDB, password=PASS_TDB, host=HOST)

#Ruta hereda de la clase Model, que tiene implementada las funcionalidades de peewee
class Ruta(Model):

    """
    This class represent the route taken by an user. The different
    points of the rute are stored in a json field called trajectory. 
    The format for the trajectory points in json is the following

    {
        "longitude": float,
        "latitude": float,
        "datetime": int
    }

    The columns of the table are the following

    user: user id storing the route. We take this id from telegram users' id
    message: id of the message sharing the live location
    date: date when the route was created
    trajectory: a json list containing the deifferent points recorded
    time: total time pre-computed used to complete the route
    distance: total distance of the route (added harvesine distance between points)
    """

    user = IntegerField()
    message = IntegerField(unique=True)
    date = DateTimeField()
    trajectory = JSONField()
    time = IntegerField( null=True )
    distance = FloatField( null=True )

    class Meta:
        database = db

if __name__ == "__main__":
    db.create_tables( [Ruta] )
    #test_db()
