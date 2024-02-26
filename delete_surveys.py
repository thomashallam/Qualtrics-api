from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.
import http.client
import json
import time
import csv
import re

# Working but with no tests or fail safes...

def delete_surveys(surveyId):
    
    surveyId = surveyId[0]
    print(f'deleting... {surveyId}')
    
    conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

    headers = {
        'Accept': "application/json",
        'X-API-TOKEN': os.getenv("apiKey")
    }

    conn.request("DELETE", f'/API/v3/surveys/{surveyId}', headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    
    time.sleep(1)
    
    
    # Check result with get survey description
    
    conn.request("GET", f'/API/v3/survey-definitions/{surveyId}/metadata', headers=headers)

    res = conn.getresponse()
    data = res.read()
    
    json_data = json.loads(data.decode("utf-8"))
    http_status = json_data["meta"].get("httpStatus")
    deleted_date = json_data["result"].get("Deleted")
    print(f'ID:{surveyId}, Status:{http_status}, DateDeleted: {deleted_date}')


def loop_surveys():
    
    #Test with sample survey
    #surveyId = os.getenv("surveyId")
    #delete_surveys(surveyId)
    
    # Specify the CSV file path
    csv_file_path = ".surveyIDs.csv"

    # Read data from CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            delete_surveys(row)
            time.sleep(1)
   
loop_surveys()