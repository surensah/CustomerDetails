# customerDetails

Created a datastore with (kind) "customer" with few attributes like customerId, email, name, phone_Number
By using python and flask framework:

## Created 3 API's:

- /getCustomers - api to fetch customers details from datastore

- /getCustomer?customerId=value - api to fetch specific customer detail from datastore

- /postCustomer - api to create new customer detail into datastore

### GCloud SDK Usage: 
Initialized gcloud sdk before deploying application into app engine

$gcloud auth login

$gcloud config set project projectId

Used app engine "standard environment" to deploy the application for deploying use command

$gcloud app deploy(google sdk)

$gcloud app browse

Application "Welcome to customer details" Endpoint: https://earnest-crow-243811.appspot.com/

#### API endpoints:

- /getCustomers endpoint: 

https://earnest-crow-243811.appspot.com/getCustomers

- /getCustomer?customerId=value endpoint with sample customer id's:


- getCustomer with id:
https://earnest-crow-243811.appspot.com/getCustomer?customerId=100


- getCustomer with id:

https://earnest-crow-243811.appspot.com/getCustomer?customerId=105  --For invalid customer id: 105

-Result:No Customer found for customer id: 105


Using Postman API to insert the values to Customer Kind:

/addCustomer endpoint: https://earnest-crow-243811.appspot.com/addCustomer

sample input for post customer {"customerid":"104","name":"Surendra","email":"surendra@gmail.com","phoneNumber":"7680900689"}
