import base64
import os.path

from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore
from googleapiclient.errors import HttpError # type: ignore

from flask_cors import CORS # type: ignore
from flask import Flask, jsonify, request # type: ignore

from textAnalysis import *
from dateutil import parser

app = Flask(__name__) # type: ignore
CORS(app)  # Enable CORS

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_email_date(headers):
  for header in headers:
    if header['name'].lower() == 'date':
      date_str = header['value']
      parsed_date = parser.parse(date_str)
      return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
  return None

def fetch_company_names():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=10).execute()
    messages = results.get("messages", [])

    company_names = []

    # Loop through the messages and obtain the body of the message
    for message in messages:
        msg = service.users().messages().get(userId="me", id=message['id']).execute()
        headers = msg.get('payload', {}).get('headers', [])
        print(headers)
        # for p in msg["payload"]["parts"]:
        #   if p["mimeType"] == "text/plain":
        #     data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
        #     company_name = get_organization_name(data)
        snippet = msg['snippet']
        company_name = get_sender_company(snippet)
        date_sent = get_email_date(headers)

        # if not company_name:
        #   headers = msg.get('payload', {}).get('headers', [])
        #   for header in headers:
        #       if header['name'] == 'From':
        #         sender_email = header['value']
        #         company_name = get_sender_company(sender_email)
        #         break

        if company_name:
            company_names.append(company_name)

    return company_names

  except HttpError as error:
    print(f"An error occurred: {error}")
    return []

@app.route('/api/companies', methods=['GET'])
def get_companines():
  # company_names = ["Google", "Amazon", "Netflix"]
  company_names = fetch_company_names()
  return jsonify({"companies": company_names})

if __name__ == "__main__":
  app.run(debug=True)