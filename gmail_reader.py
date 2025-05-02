# Credit to geeksforgeeks for the base code
# import the required libraries 
from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import extract_trans
import pickle 
import os.path 
import base64 
import email 
import logging
import re
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
                # CASE: buy items from market
                # Gonna change this later because of different format from case 2 below
                if sender == "Steam Store <noreply@steampowered.com>":
                    for part in payload['parts']:
                        for subpart in part['parts']:
                            data = subpart['body'].get('data')
                            if data:
                                data = data.replace("-","+").replace("_","/") 
                                decoded_data = base64.b64decode(data)
                                body = decoded_data.decode('utf-8')
                                extract_trans.get_steam_store_obj(body)  # This line is IMPORTANT
                                break   
                # CASE: Buy games and Subscriptions
                # Gonna change this later because of different format from case 1 above
                elif sender == "Steam Support <noreply@steampowered.com>" and ("Thank you" in subject or "subscription" in subject):
                    for part in payload['parts']:
                        for subpart in part['parts']:
                            data = subpart['body'].get('data')
                            if data:
                                data = data.replace("-","+").replace("_","/") 
                                decoded_data = base64.b64decode(data)
                                body = decoded_data.decode('utf-8')
                                url = re.search(r"https://store\.steampowered\.com/email/PurchaseReceipt\S+", body).group(0)[:-1]
                                extract_trans.get_steam_supp_obj(url)  # This line is IMPORTANT
                                break      
                # CASE: Food Basics Groceries
                elif sender == 'Food Basics Receipts <transaction@transaction.foodbasics.ca>':
                    # print("Food Basic Receipt")  
                    data = payload['body'].get('data')
                    if data:
                        data = data.replace("-","+").replace("_","/") 
                        decoded_data = base64.b64decode(data)
                        body = extract_receipt_food_basic(decoded_data.decode('utf-8', errors='ignore')) 
                        extract_trans.get_foodbasics_obj(body)                 
    
                # Printing the subject, sender's email and message 
                #logging.info(f"Subject: {subject}") 
                #logging.info(f"From: {sender}") 
                #logging.info(f"Message: {body}")
                #logging.info('\n') 
        except: 
            pass
  
  
getEmails()
