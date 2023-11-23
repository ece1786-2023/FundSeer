import csv
import requests
from bs4 import BeautifulSoup
import time
import argparse
from datetime import datetime


def extract_date(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the span tag containing the created date
        date_tag = soup.find('span', {'class': 'm-campaign-byline-created a-created-date'})
        date = date_tag.get_text() if date_tag else None

        return url, date

    except Exception as e:
        with open('log.txt', 'a') as f:
            print(f"Error processing {url}: {e}", file=f)
        return None


def main(start_row, end_row):
    urls = []

    with open('./sample.csv', 'r', newline='', encoding='utf-8') as urlfile:
        url_reader = csv.reader(urlfile)
        rows = list(url_reader)
        header = rows[0]

        for idx, row in enumerate(rows[1:], start=1):
            if start_row <= idx <= end_row:
                urls.append(row[1])  # Change index to 1 to get the URL from the second column
            elif idx > end_row:
                break

    count = 0
    max_requests_before_delay = 500
    delay_seconds = 10

    updated_rows = [header + ['length']]

    for idx, url in enumerate(urls):
        print(f"Extracting specific element from: {url}")
        specific_element_info = extract_date(url)
        if all(element is not None for element in specific_element_info):
            now = "Nov 6, 2023"  # the date that we scrape the data
            date_raw = specific_element_info[1].split()
            day = date_raw[1][:-3]
            # print(day)

            # Convert the date strings to datetime objects
            now = datetime.strptime(now, "%b %d, %Y")
            created_date = datetime(int(date_raw[2]), datetime.strptime(date_raw[0], "%B").month, int(day))

            time_difference = now - created_date

            # Extract the number of days from the timedelta object
            days_difference = time_difference.days

            # Add the length as a new column
            row = rows[idx + 1].copy()
            row.append(days_difference)
            updated_rows.append(row)

        count += 1
        if count % max_requests_before_delay == 0:
            print(f"Waiting for {delay_seconds} seconds to avoid being detected as a bot...")
            time.sleep(delay_seconds)

    # Write the updated rows to a new file
    new_file_path = f'./scrapper/data/campaign_info_updated_{start_row}_{end_row}.csv'
    with open(new_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        url_writer = csv.writer(csvfile)
        url_writer.writerows(updated_rows)

    print(f"Updated rows written to {new_file_path}")


if __name__ == "__main__":
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(description='Crawl GoFundMe data for a specified range of rows.')
    parser.add_argument('start_row', type=int, help='Starting row index for data extraction')
    parser.add_argument('end_row', type=int, help='Ending row index for data extraction')

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the main function with provided arguments
    main(args.start_row, args.end_row)
