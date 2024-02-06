from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.
import http.client
import json
import time
import csv
import re

# Working but with no tests or fail safes...

def get_surveys():
    
    conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

    #payload = "{\n  \"Group\": \"Covid Testing\",}"

    headers = {
        'Accept': "application/json",
        'X-API-TOKEN': os.getenv("apiKey")
    }

    conn.request("GET", "/API/v3/surveys", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


get_surveys()