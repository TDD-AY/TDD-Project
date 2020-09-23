from tassi.database.model import Ruta
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/v1/<int:user_id>/my-routes')
def get_routes(user_id):

    """
    list all the routes available for an user_id.
    The result should be a json with basic information
    """

    user_routes = Ruta.select().where(Ruta.user == user_id)

    routes = []

    for route in user_routes:
        routes.append(
            {
                "user": user_id,
                "message": route.message,
                "date": route.date,
                "trajectory": route.trajectory
            }
        )

    return jsonify(routes)
    

@app.route('/api/v1/<int:user_id>/route/<int:route_id>', methods=['GET', 'POST'])
def get_route_by_id(user_id, route_id):

    """
    Retrieve a route by it's id. Here we take user_id to ensure that 
    not anyone can access the route_id. At least you need to know the
    user_id
    """

    if request.method == 'GET':
        r = Ruta.get_or_none(message=route_id)
        if r != None:
            return jsonify(
                {
                    "distance_total": r.distance,
                    "time": r.time,
                    "date": r.date,
                }
            )
        else:
            return jsonify({})
    elif request.method == 'POST': 
        ruta = Ruta.get_or_none(message=route_id)
        if (ruta != None) and (ruta.user == user_id):
            Ruta.delete().where(Ruta.message == route_id).execute()
            return "Deleted"

        return "Doesn't exist"
        

@app.route('/health')
def hello_world():

    """
    Route to check that basic setup of the application is working
    """

    return 'Up and running'