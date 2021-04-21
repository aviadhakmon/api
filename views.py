import re

from sanic import Sanic
from sanic.response import json
import jwt
from configparser import ConfigParser
from datetime import datetime, timedelta

app = Sanic("My Hello, world app")


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


@app.route('/login')
async def login(request):
    parse_settings = ConfigParser()
    try:
        parse_settings.read("users.conf")
    except(IOError, TypeError) as ex:
        return json({"error read conf file": ex}, status=500)
    data = request.json
    if "user" not in data:
        return json({"error": "must contain user name"}, status=500)
    try:
        user = data["user"]
        password = data["password"]
        users = parse_settings.get("USERS_SETTINGS", "users").split(",")
        passwords = parse_settings.get("USERS_SETTINGS", "passwords").split(",")
        if user in users and password in passwords:
            exp = datetime.utcnow() + timedelta(hours=1)
            token = jwt.encode({"user": user, "password": password, "exp": exp}, key="secret_key", algorithms="HS256")
            return json({"jwt": token})
    except Exception as ex:
        return json({"error": ex}, status=500)


def token_valid(token):
    try:
        parse_settings = ConfigParser()
        try:
            parse_settings.read("users.conf")
        except(IOError, TypeError) as ex:
            return json({"error read conf file": ex}, status=500)

        decoded = jwt.decode(token, "secret_key", algorithms="HS256")
        if decoded["user"] not in parse_settings.get("USERS_SETTINGS", "users").split(","):
            return False
        return True
    except jwt.ExpiredSignatureError as ex:
        print(ex)
        return False
    except jwt.DecodeError as ex:
        print(ex)
        return False


def normalized_res(req):
    final_res = {}
    try:
        for dict_ in req:
            value = next(v for (k, v) in dict_.items() if k.endswith('Val'))
            final_res[dict_["name"]] = value
        return final_res
    except Exception as ex:
        print(ex)


@app.route('/normalized', methods=["POST", ])
async def normalized(request):
    req = request.json
    if not token_valid(request.headers.get("Authorization")):
        return json({"error": "token is not valid"}, status=401)
    return json(normalized_res(req), status=200)


if __name__ == '__main__':
    app.run()
