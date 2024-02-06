from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.
import http.client
import json
import time
import csv
import re

# Working but with no tests or fail safes...

def connect_and_export(surveyId):
    surveyId = surveyId[0]
    print(f'Extracting: {surveyId}')
    
    conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

    payload = "{\n  \"format\": \"csv\",\n  \"compress\": false,\n  \"useLabels\": true\n}"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'X-API-TOKEN': os.getenv("apiKey")
    }

    conn.request("POST", f'/API/v3/surveys/{surveyId}/export-responses', payload, headers)

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))
    
    extract_progress_id(surveyId, data)


def extract_progress_id(surveyId, data):
    # Parse the JSON data
    parsed_data = json.loads(data)
    # Extract the desired string
    exportProgressId = parsed_data['result']['progressId']
    
    print(f'Progress id: {exportProgressId}')
    time.sleep(1)
    
    loop_check_completion(surveyId, exportProgressId)


def loop_check_completion(surveyId, exportProgressId):
    
    percentComplete = 0
    
    while percentComplete < 100:
        
        conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

        headers = {
            'Accept': "application/json",
            'X-API-TOKEN': os.getenv("apiKey")
        }

        conn.request("GET", f'/API/v3/surveys/{surveyId}/export-responses/{exportProgressId}', headers=headers)

        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        
        parsed_data2 = json.loads(data)
        percentComplete = parsed_data2['result']['percentComplete']
        
        print(f'{percentComplete}%')
        
        time.sleep(3)
        
    fileId = parsed_data2['result']['fileId']
    
    get_survey_name(surveyId, fileId)


def get_survey_name(surveyId, fileId):
    
    conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

    headers = {
        'Accept': "application/json",
        'X-API-TOKEN': os.getenv("apiKey")
    }

    conn.request("GET", f"/API/v3/survey-definitions/{surveyId}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    
#    print(data.decode("utf-8"))
    
    parsed_data3 = json.loads(data)
    
    Questions =  parsed_data3['result']['Questions']

    # print(Questions)

    SurveyName = parsed_data3['result']['SurveyName']
    CleanedSurveyName = re.sub(r'[^\w\s]', '_', SurveyName)
    CleanedSurveyName = CleanedSurveyName.replace(' ', '_')
    print(f'Clean Survey name: {CleanedSurveyName}')
        
    export_the_file(surveyId, fileId, CleanedSurveyName, Questions)

    


def export_the_file(surveyId, fileId, CleanedSurveyName, Questions):
    
    conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

    headers = {
        'Accept': "application/octet-stream, application/json",
        'X-API-TOKEN': os.getenv("apiKey")
    }

    conn.request("GET", f'/API/v3/surveys/{surveyId}/export-responses/{fileId}/file', headers=headers)

    res = conn.getresponse()
    data = res.read()
    # print(data)

    utf8_encoded_data = data.decode("utf-8")
        
    # Specify the file path for survey data
    data_file_path = f"./exports/{surveyId}_{CleanedSurveyName}.csv"

    # Write survey data to CSV file
    with open(data_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        rows = list(csv.reader(utf8_encoded_data.splitlines()))
        writer.writerows(rows)

    print(f'Survey data has been exported to {data_file_path}')
    
    time.sleep(1)

    get_questions(surveyId, CleanedSurveyName)


def get_questions(surveyId, CleanedSurveyName):

    conn = http.client.HTTPSConnection(os.getenv("baseUrl"))

    headers = {
    'Accept': "application/json",
    'X-API-TOKEN': os.getenv("apiKey")
    }

    conn.request("GET", f'/API/v3/survey-definitions/{surveyId}/questions', headers=headers)

    res = conn.getresponse()
    data = res.read()

    decode = data.decode("utf-8")

    # Specify the file path for survey questions
    data_file_path2 = f"./exports/{surveyId}_{CleanedSurveyName}_Questions.json"

    # Write survey questions to a json file
    with open(data_file_path2, 'w') as f:
        json.dump(decode, f)

    print(f'Survey questions exported to {data_file_path2}')


def loop_surveys():
    
    #Test with sample survey
    #surveyId = os.getenv("surveyId")
    #connect_and_export(surveyId)
    
    # Specify the CSV file path
    csv_file_path = ".surveyIDs.csv"

    # Read data from CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Process each line in the CSV
        for row in reader:
            # Process the line using the process_line function
            connect_and_export(row)
            time.sleep(1)
   
loop_surveys()