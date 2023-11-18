import csv
import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import argparse
from tqdm import tqdm

def extract_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        category_tag = soup.find('a', {'class': 'hrt-disp-flex hrt-align-center hrt-link hrt-link--gray-dark'})
        category = category_tag.get_text() if category_tag else None

        progress_div = soup.find('div', {'class': 'progress-meter_progressMeter__ebbGu'})
        goal_raw = progress_div.find('span', {'class': 'hrt-text-body-sm hrt-text-gray'}).get_text()
        goal_raw = goal_raw.split()

        if category == "Medical" and 'USD' in goal_raw and len(goal_raw) == 5:
            title = soup.find('h1').get_text()
            description_div = soup.find('div', {'class': 'o-campaign-description'})
            description = ''.join([p.get_text() for p in description_div.find('div')])
            goal_amount = float(goal_raw[3][1:].replace(',', ''))
            raised_amount = progress_div.find('div', {'class': 'hrt-disp-inline'}).get_text()
            raised_amount = float(raised_amount[1:].replace(',', ''))

            return url, title, description, goal_amount, raised_amount
        else:
            return None

    except Exception as e:
        with open('log.txt', 'a') as f:
            print(f"Error processing {url}: {e}", file=f)
        return None

def extract_info_wrapper(url):
    try:
        return extract_info(url)
    except Exception as e:
        with open('log.txt', 'a') as f:
            print(f"Error processing {url}: {e}", file=f)
        return None

def main(start_row, end_row):
    urls = []

    with open('../data/gfm_urls.csv', 'r', newline='', encoding='utf-8') as urlfile:
        url_reader = csv.reader(urlfile)
        next(url_reader, None)

        for idx, row in enumerate(url_reader, start=1):
            if start_row <= idx <= end_row:
                urls.append(row[0])
            elif idx > end_row:
                break

    count = 0
    max_requests_before_delay = 500
    delay_seconds = 10
    pool_size = 10  # You can adjust this based on your system and the number of URLs to process

    with open(f'../data/campaign_info_{start_row}_{end_row}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'Title', 'Description', 'Goal Amount', 'Raised Amount']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        with Pool(pool_size) as pool, tqdm(total=len(urls), desc="Progress") as pbar:
            for result in pool.imap_unordered(extract_info_wrapper, urls):
                if result:
                    writer.writerow(result)

                count += 1
                pbar.update(1)
                
                if count % max_requests_before_delay == 0:
                    print(f"Waiting for {delay_seconds} seconds to avoid being detected as a bot...")
                    time.sleep(delay_seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract information from URLs within a specified range.')
    parser.add_argument('--start_row', type=int, default=400001, help='Start row for URL extraction (default: 1)')
    parser.add_argument('--end_row', type=int, default=500000, help='End row for URL extraction (default: 100)')

    args = parser.parse_args()
    main(args.start_row, args.end_row)

