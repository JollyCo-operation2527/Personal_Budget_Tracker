import requests, re
from bs4 import BeautifulSoup
from datetime import datetime

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

def get_steam_supp_obj(url):
    # Step 1: Send GET request to the URL
    response = requests.get(url)

    # Step 2: Check response status
    if response.status_code == 200:
        # Step 3: Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the total amount
        total_label_td = soup.find('td', string=lambda s: s and s.strip() == "Total:")
        if total_label_td:
            tr = total_label_td.find_parent('tr')
            if tr:
                tds = tr.find_all('td') 
                total_amount = tds[-1].get_text(strip=True).replace('CDN$', '').strip()
                print(total_amount)

        # Get the date
        date_label_td = soup.find('td', string=lambda s: s and s.strip() == "Date issued:")
        if date_label_td:
            tr = date_label_td.find_parent('tr')
            if tr:
                tds = tr.find_all('td')
                strong_tag = tds[-1].find('strong')
                if strong_tag:
                    date_text = strong_tag.get_text(strip=True).split('@')[0].strip()
                    print(date_text)
        
    else:
        print(f'Failed to fetch page. Status code: {response.status_code}')

def get_steam_store_obj(body):
    # Extract total — the line starting with "Total:" followed by a number
    total_match = re.search(r"Total:\s*\n\s*([\d.]+)\s*CAD", body)
    total = total_match.group(1) if total_match else None
    print(total)

    # Extract date — the line after "Date Confirmed"
    date_match = re.search(r"Date Confirmed\s*\n\s*\w+\s+(\w+)\s+(\d+)\s+[\d:]+\s+(\d{4})", body)
    if date_match:
        month, day, year = date_match.groups()
        date_formatted = f"{day} {month}, {year}"
    else:
        date_formatted = None

    print(date_formatted)

def get_foodbasics_obj(body):
    # Extract TOTAL line
    total_match = re.search(r"^TOTAL\s+([\d.]+)", body, re.MULTILINE)
    total = total_match.group(1) if total_match else None

    # Extract DateTime line
    date_match = re.search(r"DateTime:\s*(\d{2})/(\d{2})/(\d{2})", body)
    if date_match:
        yy, mm, dd = date_match.groups()
        # Assume year 20yy
        full_date = datetime.strptime(f'20{yy}-{mm}-{dd}', "%Y-%m-%d")
        date_formatted = full_date.strftime("%d %b, %Y")  
    else:
        date_formatted = None

    # Output
    print(total)
    print(date_formatted)

def get_domino_obj(html):
    # Search for "Total: $<number>" in a <strong> tag
    match = re.search(r"<strong>\s*Total:\s*\$([\d.]+)\s*</strong>", html)
    if match:
        total = match.group(1)
        print(total)
    
    # Use regex to find the date following the "Date:" label
    match = re.search(r"<strong>\s*Date:\s*</strong>\s*(\d{2}/\d{2}/\d{4})", html)
    if match:
        raw_date = match.group(1) 
        # Convert to datetime object
        dt = datetime.strptime(raw_date, "%m/%d/%Y")
        # Format as dd MM, YYYY
        formatted_date = dt.strftime("%d %b, %Y")
        print(formatted_date)
   
    

