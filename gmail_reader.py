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

def extract_receipt_food_basic(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the td with the style and class that match the receipt block
    receipt_td = None
    for td in soup.find_all("td"):
        if "Store #100" in td.get_text():
            receipt_td = td
            break

    if receipt_td:
        # Get all text and clean it up
        text = receipt_td.get_text(separator="\n", strip=True)

        # Optional: remove leading/trailing junk lines or excessive empty lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
    else:
        return "RECEIPT BLOCK NOT FOUND"


def extract_receipt_steam(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    return soup



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
    result = service.users().messages().list(maxResults=200, userId='me').execute() 
    messages = result.get('messages') 

    if not messages:
        print("No email found.")
    else:
        print(f"{len(messages)} emails fetched")
  
    # List of wanted senders (Only look at emails from these senders)
    wanted_senders = ['Steam Store <noreply@steampowered.com>',
    'Steam Support <noreply@steampowered.com>',
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
            
            # Only look at emails from certain senders
            if sender in wanted_senders:
                print(sender)
                # Deal with different payload structures
                # Handle multipart emails
                if 'parts' in payload:
                    parts = payload['parts']
                    for part in parts:
                        print(f"Part MIMETYPE: {part['mimeType']}")  # for debugging
                        # Handle 'multipart/alternative' case
                        if part['mimeType'] == 'multipart/alternative':
                            # print("MULTIPART/ALTERNATIVE TYPE")  
                            for subpart in part['parts']:
                                if subpart['mimeType'] == 'text/html':
                                    print("MimeType = multipart/alternative, subpart MimeType = text/html")  
                                    # Do nothing for now

                                # CASE Steam
                                elif subpart['mimeType'] == 'text/plain':
                                    print("Steam receipt")  
                                    data = subpart['body'].get('data')
                                    if data:
                                        data = data.replace("-","+").replace("_","/") 
                                        decoded_data = base64.b64decode(data)
                                        body = decoded_data.decode('utf-8')
                                        break

                        # Handle 'text/html' case
                        elif part['mimeType'] == 'text/html':
                            print("MimeType = text/html")
                            # Do nothing for now

                        # Handle 'text/plain' case
                        elif part['mimeType'] == 'text/plain':
                            print("MimeType = text/plain")
                            # Do nothing for now

                # Handle single part emails
                # CASE: Food Basic Receipt 
                else:
                    # print("Food Basic Receipt")  
                    data = payload['body'].get('data')
                    if data:
                        data = data.replace("-","+").replace("_","/") 
                        decoded_data = base64.b64decode(data)
                        body = extract_receipt_food_basic(decoded_data.decode('utf-8', errors='ignore'))                  
    
                # Printing the subject, sender's email and message 
                logging.info(f"Subject: {subject}") 
                logging.info(f"From: {sender}") 
                logging.info(f"Message: {body}")
                logging.info('\n') 
        except: 
            pass
  
  
getEmails()
