# Qualtrics api export list of surveys to csv file type

Install python3 latest, update Pip

pip -m venv .venv
mkdir exports

cp .sample.env .env
nano .env
  - update: baseUrl, apiKey and surveyId

cp .sample.surveyIDs.csv .surveyIDs.csv
nano .surveyIDs.csv
   - populate list of surveyIDs

python connect.py
