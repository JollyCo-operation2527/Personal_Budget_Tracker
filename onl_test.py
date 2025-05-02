import requests
from bs4 import BeautifulSoup

# Step 1: URL of the online receipt
url = 'https://store.steampowered.com/email/PurchaseReceipt?sparams=eJx9VV1vmzAU_SsRz1MaSCBJn1q10x4qtQ9bpW1phW7wLVgxNrVNMjTtv-8aTApJ1Lf4nMu1z7kf-RsIqGVWoLZNhcF1MAu-BBpBlPQ7F2oLgoBKK1ZnVkLpQr5bhJJQU1eV0hZL4IJgf7wxjq7UATWyaaYGkYZb931hbWWuX65ergoU1fRCvE9qUNraZvRJuFwk4Xw9W86J3XIhuMzTTNXS6obou9sBzKtTBrIW8M8HAcYC1-F6vSLSapCGMyKiZTQLF4t5FM7jZB5G8aKnIbNcyZRB-_7-Mcma-LxGY71vVrXPBsY0GkOgzIu6IeeiOFre5I7zAtus3vGQzkgO7zlDnVbQlCQ7LdEWivnE3GjMaq1Jnuc9sTWFOjDc1vkBt6R-53EXjDJzDkTufAAh0KZQOh8IXEZdVbs7j3AnwoJIqVIl2dhKSxZjeA9ijynjJrv8mYU_BK6OoCl4VXUFM-PwI9N9MshTun5J3xBHMLnQZG2RTxmfutXVifXOdgco24uny2hyd3s_0N4Ts5knCjBUg2wHeV-bPdhBQ7krEbRElgrVgLBNatUOpSt37Mi2nemlB9AsrRSX1qQ0RSAzlzCZxXFMUSQCe5M7E8MR2vXGJuif8jokXbdugjBaJFEYj6nOh42r2Qg_rdmGhIwCqAKwFeOQJD6LcfDqDE11Oxn0pvmY6wt84cJx7c_oYQeckSd98Gnu49tOYhiaTPPKDbZjx-S7bVo550o778d4v3kg14jt9PblOzWZl5jWkl8qwJvG97qb2Ut6u-k_juonIR-zfxbkFyFnac7f7EXr2g02oB3b66O12S7Ap8fBuv3YdtTbkweudwel2OR2j4Mgv3rvn-8mj9-ef329kCAifrjcuStB8GQtHGCAV9Tg7bwzl_Ah_D2Jf8aj7e9maRVP16tpuAynyXxEfmiQFjRXJ_8b3aU_lFbSquDff1znZ3k&check=ea0602d223e0dc6b07e3d5a2152d9ad18f881d1e3f85f58aee5a1ff7c95f39da'  # replace with your actual receipt URL

# Step 2: Send GET request to the URL
response = requests.get(url)

# Step 3: Check response status
if response.status_code == 200:
    # Step 4: Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
   
    # Step 5: Extract desired data (e.g., item names, prices, etc.)
    # You need to inspect the structure of the page to get the right tags/classes/ids

    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if any(td.get_text(strip=True) == "Total:" for td in tds):
            total_td = tds[-1] 
            total_amount = total_td.get_text(strip=True).replace('CDN$', '').strip()
            print(total_amount)
        
    #with open('steam_test.txt', "w", encoding="utf-8") as f:
     #   f.write(receipt_td)

    
else:
    print(f'Failed to fetch page. Status code: {response.status_code}')