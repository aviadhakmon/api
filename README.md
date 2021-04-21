# API
api is a  web service that gives a normalized version of the input that it gets

## Requests
In order to use the api you must log in with the username and password and will get a jwt.

After that you can send your json request and get a normalized version of it:

for example:

[
    {
        “name”: “device”,
        “strVal”: “iPhone”,
        “metadata”: “not interesting”
    },
    {
        “name”: “isAuthorized”,
        “boolVal”: “false”,
        “lastSeen”: “not interesting”
    }
]

will response:

{
“device”: “iPhone”,
“isAuthorized”: “false”
}

##Requirements in order to deploy it
sanic==21.3.2
pyjwt==2.0.1
