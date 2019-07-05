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
	
firebase_request_adapter = requests.Request()
app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "app.conf"), silent=False)
google_name = app.config.get("GOOGLE_ENDPOINT_NAME")	
table_name = app.config.get("TABLE_NAME")
client=datastore.Client(google_name)
	
@app.route('/')
def root():
    return "Hello world !!!!"
	

@app.route('/getCustomer', methods=['GET'])
def get_customer():
	# Fetch query parameter
	customerId = request.args.get('customerId')
	if customerId is None:
		return "please provide customer id"
	query = client.query(kind=table_name)
	query.add_filter('customerId', '=', customerId)
	result = list(query.fetch())
	if len(result) == 0:	
		return "No Customer found for customer id: "+customerId;
	return jsonify(result[0]);
	
@app.route('/addCustomer', methods=['POST'])
def add_customer():
	content = request.get_json()
	name = content['name']
	email = content['email']
	phoneNumber = content['phone_number']
	customerid= content['customerid']
	if name is None or email is None or customerid is None:
		return "please provide customer name and email and ID"
	customerKey = client.key(table_name,customerid)
	cust_table_name = datastore.Entity(key=customerKey)
	cust_table_name['customerId'] = customerid
	cust_table_name['name'] = name
	cust_table_name['email'] = email
	cust_table_name['phone_number'] = phoneNumber
	client.put(cust_table_name);
	#return "save data successfully";

	return jsonify(cust_table_name);	

@app.route('/getCustomers', methods=['GET'])
def get_customers():
	query = client.query(kind=table_name)
	return jsonify(list(query.fetch()));

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
