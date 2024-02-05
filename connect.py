
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

import http.client

conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

payload = "{\n  \"format\": \"csv\",\n  \"compress\": false,\n  \"useLabels\": true\n}"

surveyId = os.getenv("surveyId")

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'X-API-TOKEN': os.getenv("apiKey")
}


conn.request("POST", f'/API/v3/surveys/{surveyId}/export-responses', payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

### Extract the progress ID
import json
# Parse the JSON data
parsed_data = json.loads(data)
# Extract the desired string
progress_id = parsed_data['result']['progressId']
print(progress_id)


### Loop check for 100% completion



## download the file



## Loop through next item in list

