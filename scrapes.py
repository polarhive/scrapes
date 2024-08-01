import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import csv

load_dotenv()
csrf_token = os.getenv("CSRF_TOKEN")
cookie = os.getenv("COOKIE")

# config
start_SRN = 1  # Starting SRN without leading zeros
end_SRN = 4  # Ending SRN
prefix = "PES2UG23CS"

# base URL
url = 'https://www.pesuacademy.com/Academy/getStudentClassInfo'

def get_text_or_na(element):
    return element.get_text(strip=True) if element else "NA"

# dump into a CSV file
with open('student_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['ID', 'Name', 'Old Section', 'New Section']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(start_SRN, end_SRN + 1):  # Include end_SRN by using end_SRN + 1
        id_ = f"{prefix}{i:03d}"  # Zero-padded to 3 digits
        print(f"Processing ID: {id_}")

        # POST request
        response = requests.post(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRF-Token': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.pesuacademy.com',
                'DNT': '1',
                'Sec-GPC': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://www.pesuacademy.com/Academy/',
                'Cookie': cookie,
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Priority': 'u=0',
                'TE': 'trailers'
            },
            data={'loginId': id_}
        )

        # parse stuff with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        name = get_text_or_na(soup.select_one('tbody tr:nth-of-type(2) td:nth-of-type(3)'))
        old_section = get_text_or_na(soup.select_one('tbody tr:nth-of-type(1) td:nth-of-type(5)'))
        new_section = get_text_or_na(soup.select_one('tbody tr:nth-of-type(2) td:nth-of-type(5)'))

        print(f"Name: {name} | Old Section: {old_section} | New Section: {new_section}")
        writer.writerow({'ID': id_, 'Name': name, 'Old Section': old_section, 'New Section': new_section})

print("check: 'student_data.csv'")
