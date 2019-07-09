# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
import datetime
import os
from flask import Flask, render_template, jsonify, request
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
import google.auth.credentials

# Class variables
app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "app.conf"), silent=False)
ProjectName = app.config.get("PROJECT_NAME")
tableName = app.config.get("TABLE_NAME")
client = datastore.Client(ProjectName)
apiPort = app.config.get("PORT")

@app.route('/')
def root():
    return "Welcome to customer details Application !!!!"

@app.route('/getCustomers', methods=['GET'])
def getCustomers():
	# Returns all the customer details
    query = client.query(kind=tableName)
    return jsonify(list(query.fetch()));

@app.route('/getCustomer', methods=['GET'])
def getCustomer():
    # Returns customer details for valid customerId
    # Fetch query parameter
    customerId = request.args.get('customerId')

    if customerId is None:
        return "Please provide customer id"

    query = client.query(kind=tableName)
    query.add_filter('customerId', '=', customerId)
    result = list(query.fetch())

    if len(result) == 0:
        return "No Customer found for customer id: " + customerId;
    return jsonify(result[0]);

@app.route('/addCustomer', methods=['POST'])
def addCustomer():
    # Add customer data into Datastore
    customerKey = client.key(tableName)
    custTable = datastore.Entity(key=customerKey)
    custTable.update(request.get_json())
    client.put(custTable)
    res = {'message' : 'Customer added successfully', 'data' : custTable}
    return jsonify(res);
	

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=apiPort, debug=True)
# [START gae_python37_render_template]
