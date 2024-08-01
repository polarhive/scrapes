import os
from dotenv import load_dotenv
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv

load_dotenv()
csrf_token = os.getenv("CSRF_TOKEN")
cookie = os.getenv("COOKIE")

# config
start_SRN = 1
end_SRN = 721
prefix = "PES2UG23CS"
url = 'https://www.pesuacademy.com/Academy/getStudentClassInfo'

def get_text_or_na(element):
    return element.get_text(strip=True) if element else "NA"

async def fetch(session, id_):
    headers = {
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
    }

    try:
        async with session.post(url, headers=headers, data={'loginId': id_}) as response:
            response.raise_for_status()  # raise exception for HTTP errors
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            name = get_text_or_na(soup.select_one('tbody tr:nth-of-type(2) td:nth-of-type(3)'))
            old_section = get_text_or_na(soup.select_one('tbody tr:nth-of-type(1) td:nth-of-type(5)'))
            new_section = get_text_or_na(soup.select_one('tbody tr:nth-of-type(2) td:nth-of-type(5)'))
            fetched_data = {'ID': id_, 'Name': name, 'Old Section': old_section, 'New Section': new_section}
            print(fetched_data)
            return fetched_data
    except Exception as e:
        print(f"Failed to fetch data for ID: {id_}: {e}")
        return {'ID': id_, 'Name': 'Error', 'Old Section': 'Error', 'New Section': 'Error'}

async def main():
    async with aiohttp.ClientSession() as session:
        ids = [f"{prefix}{i:03d}" for i in range(start_SRN, end_SRN + 1)]
        tasks = [fetch(session, id_) for id_ in ids]
        results = await asyncio.gather(*tasks)

    # dump into a CSV file
    with open('student_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Name', 'Old Section', 'New Section']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("Check: 'student_data.csv'.")

if __name__ == "__main__":
    asyncio.run(main())
