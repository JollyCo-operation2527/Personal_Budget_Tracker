# Credit to geeksforgeeks for the base code
# import the required libraries 
from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import pickle 
import os.path 
import base64 
import email 
import logging
from bs4 import BeautifulSoup 
  
# Define the SCOPES. If modifying it, delete the token.pickle file. 
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] 
  
# Set up basic logging
logging.basicConfig(filename = 'app.log', level=logging.INFO)  

def getEmails(): 
    # Variable creds will store the user access token. 
    # If no valid token found, we will create one. 
    creds = None
  
    # The file token.pickle contains the user access token. 
    # Check if it exists 
    if os.path.exists('token.pickle'): 
  
        # Read the token from the file and store it in the variable creds 
        with open('token.pickle', 'rb') as token: 
            creds = pickle.load(token) 
  
    # If credentials are not available or are invalid, ask the user to log in. 
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else: 
            flow = InstalledAppFlow.from_client_secrets_file('secret/credentials.json', SCOPES) 
            creds = flow.run_local_server(port=8080) 
  
        # Save the access token in token.pickle file for the next run 
        with open('token.pickle', 'wb') as token: 
            pickle.dump(creds, token) 
  
    # Connect to the Gmail API 
    service = build('gmail', 'v1', credentials=creds) 
  
    # request a list of all the messages 
    result = service.users().messages().list(userId='me').execute() 
  
    # We can also pass maxResults to get any number of emails. Like this: 
    result = service.users().messages().list(maxResults=50, userId='me').execute() 
    messages = result.get('messages') 

    if not messages:
        print("No email found.")
    else:
        print(f"{len(messages)} emails fetched")
  
    # List of wanted senders (Only look at emails from these senders)
    wanted_senders = ['Steam <noreply@steampowered.com>',
    'Food Basics Receipts <transaction@transaction.foodbasics.ca>']

    # messages is a list of dictionaries where each dictionary contains a message id. 
  
    # iterate through all the messages 
    for msg in messages: 
        # Get the message from its id 
        txt = service.users().messages().get(userId='me', id=msg['id']).execute() 
  
        # Use try-except to avoid any Errors 
        try: 
            # Get value of 'payload' from dictionary 'txt' 
            payload = txt['payload'] 
            headers = payload['headers'] 

            # Look for Subject and Sender Email in the headers 
            for d in headers: 
                if d['name'] == 'Subject': 
                    subject = d['value'] 
                if d['name'] == 'From': 
                    sender = d['value'] 
            
            # Only look at emails fro mcertain senders
            if sender in wanted_senders:
                # Handle different payload structures
                if 'parts' in payload:
                    parts = payload['parts']
                    for part in parts:
                            # Handle  multipart emails with 'text/html'
                            if part['mimeType'] == 'text/html':
                                data = part['body'].get('data')
                                if data:
                                    data = data.replace("-","+").replace("_","/") 
                                    decoded_data = base64.b64decode(data)
                                    # Now, the data obtained is in lxml. So, we will parse  
                                    # it with BeautifulSoup library 
                                    soup = BeautifulSoup(decoded_data , "lxml") 
                                    body = soup.get_text() 
                                    break
                            # Handle  multipart emails with 'text/plain'
                            elif part['mimeType'] == 'text/plain':
                                data = part['body'].get('data')
                                if data:
                                    data = data.replace("-","+").replace("_","/") 
                                    decoded_data = base64.b64decode(data)
                                    body = decoded_data.decode('utf-8')
                                    break
                # Handle single part emails
                else:
                    data = payload['body'].get('data')
                    if data:
                        data = data.replace("-","+").replace("_","/") 
                        decoded_data = base64.b64decode(data)
                        body = decoded_data.decode('utf-8')
    
                # Printing the subject, sender's email and message 
                logging.info(f"Subject: {subject}") 
                logging.info(f"From: {sender}") 
                logging.info(f"Message: {body}")
                logging.info('\n') 
        except: 
            pass
  
  
getEmails()
