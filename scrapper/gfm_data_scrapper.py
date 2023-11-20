import csv
import requests
from bs4 import BeautifulSoup
import time
import argparse  # Import the argparse module for handling command-line arguments

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

def main(start_row, end_row):
    urls = []

    with open('./scrapper/data/raw_data/sitemap_20231106/gfm_urls.csv', 'r', newline='', encoding='utf-8') as urlfile:
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

    with open(f'./scrapper/data/campaign_info_{start_row}_{end_row}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'Title', 'Description', 'Goal Amount', 'Raised Amount']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for url in urls:
            print(f"Extracting info from: {url}")
            info = extract_info(url)
            if info:
                writer.writerow(info)  # Write data immediately to the CSV file

            count += 1
            if count % max_requests_before_delay == 0:
                print(f"Waiting for {delay_seconds} seconds to avoid being detected as a bot...")
                time.sleep(delay_seconds)

if __name__ == "__main__":
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(description='Crawl GoFundMe data for a specified range of rows.')
    parser.add_argument('start_row', type=int, help='Starting row index for data extraction')
    parser.add_argument('end_row', type=int, help='Ending row index for data extraction')

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the main function with provided arguments
    main(args.start_row, args.end_row)
