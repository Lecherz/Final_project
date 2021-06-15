import flask
import pymongo
from flask import Flask, render_template, request, jsonify, make_response, json, Response
import logging
import warnings
from bson.json_util import dumps

# packages for swagger
from flasgger import Swagger
from flasgger import swag_from

# setup flask app
app = Flask(__name__)

# setup swagger online document
swagger = Swagger(app)

#conn to db
#myclient = pymongo.MongoClient('mongodb://%s:%s/' % ('rs1','27041'))
#db_1 = myclient["List_user"]
#mycol = db_1["User"]


# create user restful API
@app.route('/list_user', methods=['GET'])
@swag_from('apidocs/api_list_user.yml')
def lsit_user():
    myclient = pymongo.MongoClient('mongodb://192.168.0.44:27018')
    db_1 = myclient["List_user"]
    mycol = db_1["User"]
    inf = []
    for i in mycol.find():
        inf.append({'id':str(i['_id']),'username': i['username'],'password':i['password']})
    return jsonify(inf)

@app.route('/')
def index():
    return 'Web App with Python Flask!'


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5001)
