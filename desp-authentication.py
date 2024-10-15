import json
import sys
from getpass import getpass, getuser
from pathlib import Path
from typing import Annotated, Optional
from urllib.parse import parse_qs, urlparse

import requests
from conflator import CLIArg, ConfigModel, Conflator, EnvVar
from lxml import html
from pydantic import Field

IAM_URL = "https://auth.destine.eu"
CLIENT_ID = "polytope-api-public"
REALM = "desp"
SERVICE_URL = "https://polytope.lumi.apps.dte.destination-earth.eu/"


class Config(ConfigModel):
    user: Annotated[
        Optional[str],
        Field(description="Your DESP username"),
        CLIArg("-u", "--user"),
        EnvVar("USER"),
    ] = None
    password: Annotated[
        Optional[str],
        Field(description="Your DESP password"),
        CLIArg("-p", "--password"),
        EnvVar("PASSWORD"),
    ] = None
    outpath: Annotated[
        str,
        Field(description='The file to write the token to (or "stdout")'),
        CLIArg("-o", "--outpath"),
    ] = str(Path().home() / ".polytopeapirc")


config = Conflator("despauth", Config).load()

if config.user == None:
    config.user = input("Username: ")
if config.password == None:
    config.password = getpass(prompt="Password: ")

with requests.Session() as s:
    # Get the auth url
    auth_url = (
        html.fromstring(
            s.get(
                url=IAM_URL + "/realms/" + REALM + "/protocol/openid-connect/auth",
                params={
                    "client_id": CLIENT_ID,
                    "redirect_uri": SERVICE_URL,
                    "scope": "openid offline_access",
                    "response_type": "code",
                },
            ).content.decode()
        )
        .forms[0]
        .action
    )

    # Login and get auth code
    login = s.post(
        auth_url,
        data={
            "username": config.user,
            "password": config.password,
        },
        allow_redirects=False,
    )

    # We expect a 302, a 200 means we got sent back to the login page and there's probably an error message
    if login.status_code == 200:
        tree = html.fromstring(login.content)
        error_message_element = tree.xpath('//span[@id="input-error"]/text()')
        error_message = (
            error_message_element[0].strip()
            if error_message_element
            else "Error message not found"
        )
        raise Exception(error_message)

    if login.status_code != 302:
        raise Exception("Login failed")

    auth_code = parse_qs(urlparse(login.headers["Location"]).query)["code"][0]

    # Use the auth code to get the token
    response = requests.post(
        IAM_URL + "/realms/" + REALM + "/protocol/openid-connect/token",
        data={
            "client_id": CLIENT_ID,
            "redirect_uri": SERVICE_URL,
            "code": auth_code,
            "grant_type": "authorization_code",
            "scope": "",
        },
    )

    if response.status_code != 200:
        raise Exception("Failed to get token")

    # instead of storing the access token, we store the offline_access (kind of "refresh") token
    token = response.json()["refresh_token"]
    # offline_token = response.json()['refresh_token']

    if config.outpath != "stdout":
        with open(config.outpath, "w") as file:
            dico = {"user_key": token}
            json.dump(dico, file)
            print(f"Token successfully written to {config.outpath}")
    else:
        print(token)
