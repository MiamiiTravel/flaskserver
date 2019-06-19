from flask import Flask, request, Response
import os
import json


app = Flask(__name__)


def get_all_users():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as data:
            result = json.load(data)
        js = json.dumps(result)
        return Response(js, status=200, mimetype='application/json')
    else:
        return Response('{"status": "ERROR", "error": "No data available"}', status=400, mimetype='application/json')


def get_user(id):
    try:
        with open('data.json', 'r') as data:
            result = json.load(data)
        return Response(json.dumps(result[id]), status=200, mimetype='application/json')
    except KeyError:
        return Response(json.dumps({'status': 'ERROR', 'error': 'The user exists'}),
                        status=404,
                        mimetype='application/json')


def create_user():
    data = request.json
    print(data)
    if 'name' not in data or 'age' not in data:
        return Response('{"status": "error", "error": "Bad request"}', status=400, mimetype='application/json')
    with open('data.json', 'r') as result_data:
        result = json.load(result_data)
    for js in result:
        if result[js]['name'] == data['name']:
            return Response(json.dumps({'status': 'ERROR', 'error': 'The user exists'}),
                            status=409,
                            mimetype='application/json')
    name_id = f'{len(result)+1}'
    name = data['name']
    age = data['age']
    result[name_id] = {'name': name, 'age': age}
    with open('data.json', 'w') as fh:
        fh.writelines(json.dumps(result))
    return Response(json.dumps({'id': name_id, 'name': name, 'age': age}), status=201, mimetype='application/json')


def update_user(id):
    data = request.json
    print(data)
    if 'name' not in data or 'age' not in data:
        return Response('{"status": "error", "error": "Bad request"}', status=400, mimetype='application/json')
    with open('data.json', 'r') as result_data:
        result = json.load(result_data)
    for js in result:
        if result[js]['name'] == data['name']:
            return Response(json.dumps({'status': 'ERROR', 'error': 'The user exists'}),
                            status=409,
                            mimetype='application/json')
    name = data['name']
    age = data['age']
    result[id] = {'name': name, 'age': age}
    with open('data.json', 'w') as fh:
        fh.writelines(json.dumps(result))
    return Response(json.dumps({'name': name, 'age': age}), status=201, mimetype='application/json')


def remove_user(id):
    with open('data.json', 'r') as result_data:
        result = json.load(result_data)
    try:
        result.pop(id)
        with open('data.json', 'w') as fh:
            fh.writelines(json.dumps(result))
        return Response(json.dumps({'status': 'ERROR', 'error': f'REMOVED user ID {id}'}),
                        status=410, mimetype='application/json')
    except KeyError:
        return Response(json.dumps({'status': 'ERROR', 'error': 'The user exists'}),
                        status=404,
                        mimetype='application/json')


@app.route('/')
def index():
    return 'Welcome, user!'


@app.route('/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return get_all_users()
    elif request.method == 'POST':
        return create_user()
    else:
        pass


@app.route('/users/<string:id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def user_id(id):
    if request.method == 'GET':
        return get_user(id)
    elif request.method == 'PUT':
        return update_user(id)
    elif request.method == 'DELETE':
        return remove_user(id)
    elif request.method == 'POST':
        return create_user()
    else:
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
