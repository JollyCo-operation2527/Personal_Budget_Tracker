# Credit to geeksforgeeks for the base code
# import the required libraries 
import os
import django

# Set the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "budget_tracker_backend.settings")

# Setup Django
django.setup()

from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
from transactions.services import extract_trans, recurring_payments
import pickle 
import os.path 
import base64 
import email 
import logging
import re
from bs4 import BeautifulSoup 
from transactions.models import Transaction, Item

  
# Define the SCOPES. If modifying it, delete the token.pickle file. 
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] 
  
# Set up basic logging
logging.basicConfig(filename = 'app.log', level=logging.INFO)  

TOKEN_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'secret', 'token.pickle')
TOKEN_PATH = os.path.abspath(TOKEN_PATH)

def is_docker():
    return os.path.exists('/.dockerenv')

def getEmails(): 
    # Variable creds will store the user access token. 
    # If no valid token found, we will create one. 
    creds = None
  
    # The file token.pickle contains the user access token. 
    # Check if it exists 
    if os.path.exists(TOKEN_PATH): 
  
        # Read the token from the file and store it in the variable creds 
        with open(TOKEN_PATH, 'rb') as token: 
            creds = pickle.load(token) 
  
    # If credentials are not available or are invalid, ask the user to log in. 
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else: 
            if is_docker():
                print("Token not valid or missing. Generate one outside of Docker.")
                return
            else:
                flow = InstalledAppFlow.from_client_secrets_file('secret/credentials.json', SCOPES) 
                creds = flow.run_local_server(port=8080) 
  
        # Save the access token in token.pickle file for the next run 
        with open(TOKEN_PATH, 'wb') as token: 
            pickle.dump(creds, token) 
  
    # Connect to the Gmail API 
    service = build('gmail', 'v1', credentials=creds) 
  
    # Pass maxResults to get any number of emails (maximum is 500 due to Google API limit)
    result = service.users().messages().list(maxResults=500, userId='me').execute() 
    messages = result.get('messages', []) 

    # Use this block if there are more emails to fetch
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(maxResults=300, userId='me', pageToken=page_token).execute()
        messages.extend(result.get('messages', []))
        break

    if not messages:
        print("No email found.")
    else:
        print(f"Fetching {len(messages)} emails")
  
    # List of wanted senders (Only look at emails from these senders)
    wanted_senders = ['Steam Store <noreply@steampowered.com>',
    'Steam Support <noreply@steampowered.com>',
    'Food Basics Receipts <transaction@transaction.foodbasics.ca>',
    'orders@dominos.ca']
    
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
                # CASE: buy items from market
                if sender == "Steam Store <noreply@steampowered.com>":
                    for part in payload['parts']:
                        for subpart in part['parts']:
                            data = subpart['body'].get('data')
                            if data:
                                data = data.replace("-","+").replace("_","/") 
                                decoded_data = base64.b64decode(data)
                                body = decoded_data.decode('utf-8')
                                new_trans = extract_trans.get_steam_store_obj(body)  # This line is IMPORTANT
                                new_trans.save()
                                break   

                # CASE: Buy games and Subscriptions                
                elif sender == "Steam Support <noreply@steampowered.com>" and ("Thank you" in subject or "subscription" in subject):
                    for part in payload['parts']:
                        for subpart in part['parts']:
                            data = subpart['body'].get('data')
                            if data:
                                data = data.replace("-","+").replace("_","/") 
                                decoded_data = base64.b64decode(data)
                                body = decoded_data.decode('utf-8')
                                url = re.search(r"https://store\.steampowered\.com/email/PurchaseReceipt\S+", body).group(0)[:-1]
                                new_trans = extract_trans.get_steam_supp_obj(url)  # This line is IMPORTANT
                                new_trans.save()
                                break      

                # CASE: Food Basics Groceries
                elif sender == 'Food Basics Receipts <transaction@transaction.foodbasics.ca>':
                    # print("Food Basic Receipt")  
                    data = payload['body'].get('data')
                    if data:
                        data = data.replace("-","+").replace("_","/") 
                        decoded_data = base64.b64decode(data)
                        body = extract_trans.extract_receipt_food_basic(decoded_data.decode('utf-8', errors='ignore')) 
                        new_trans = extract_trans.get_foodbasics_obj(body)   # This line is IMPORTANT
                        new_trans.save()

                # CASE: Domino's Pizza
                elif sender == 'orders@dominos.ca' and "Your Domino's Pizza Order" in subject:
                    data = payload['body'].get('data')
                    if data:
                        data = data.replace("-","+").replace("_","/") 
                        decoded_data = base64.b64decode(data)
                        body = decoded_data.decode('utf-8', errors='ignore')
                        new_trans = extract_trans.get_domino_obj(body)  # This line is IMPORTANT
                        new_trans.save()
    
                # Printing the subject, sender's email and message (for debugging)
                """logging.info(f"Subject: {subject}") 
                logging.info(f"From: {sender}") 
                logging.info(f"Message: {body}")
                logging.info('\n') """
        except: 
            pass
  
  
getEmails()
recurring_payments.recur_payments_obj()

