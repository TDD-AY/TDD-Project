from flask import Flask, request
app = Flask(__name__)

@app.route('/api/v1/<int:user_id>/my-routes')
def get_routes(user_id):

    """
    list all the routes available for an user_id.
    The result should be a json with basic information
    """

    return 'my routes'

@app.route('/api/v1/<int:user_id>/route/<int:route_id>', methods=['GET', 'DELETE'])
def get_route_by_id(user_id, route_id):

    """
    Retrieve a route by it's id. Here we take user_id to ensure that 
    not anyone can access the route_id. At least you need to know the
    user_id
    """

    if request.method == 'GET':
        return 'getting route by id'
    elif request.method == 'DELETE': 
        return 'DELETED'

@app.route('/health')
def hello_world():

    """
    Route to check that basic setup of the application is working
    """

    return 'Up and running'