import requests, re
from bs4 import BeautifulSoup
from datetime import datetime

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
