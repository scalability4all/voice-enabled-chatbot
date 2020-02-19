# flask-splitwise-example
A Flask application to show the usage of Splitwise SDK.

## Installation
This application is dependent on Flask and Splitwise. nstall these python packages using the commands  below:

Install using pip :

```sh
$ pip install flask
$ pip install splitwise
```

## Register your application

Register your application on [splitwise](https://secure.splitwise.com/oauth_clients) and get your consumer key and consumer secret.

Use the following -

Homepage URL - http://localhost:5000 

Callback URL - http://localhost:5000/authorize

Make note of **Consumer Key** and **Consumer Secret**

## Set Configuraion

Open ```config.py``` and replace consumer_key and consumer_secret by the values you got after registering your application.

## Run the application

Goto the cloned repository and type 

```python
python app.py
```

Goto http://localhost:5000/ on your browser and you will be able to see the applcation running. 
