from flask import Flask,, request
app = Flask(__name__)

@app.route('/api/v1/my-routes')
def get_routes():
    return 'my routes'

@app.route('/api/v1/route/<int:route_id>', methods=['GET', 'DELETE'])
def get_route_by_id(route_id):
    if request.method == 'GET':
        return 'getting route by id'
    elif request.method == 'DELETE': 
        return 'DELETED'

@app.route('/health')
def hello_world():
    return 'Up and running'

# example.com/api/v1/my-routes

#GET example.com/api/v1/my-routes ->