# import csv
# import requests
# from bs4 import BeautifulSoup
# import time
# import argparse
# from datetime import datetime


# def extract_date(url):
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()

#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find the div tag containing the user information, extract the address
#         user_info_div = soup.find('div', {'class': 'm-campaign-members-main-organizer'})
#         address = user_info_div.find_all('div', {'class': 'hrt-text-body-sm'})[1].get_text() if user_info_div else None

#         # Find the span tag containing the created date
#         date_tag = soup.find('span', {'class': 'm-campaign-byline-created a-created-date'})
#         date = date_tag.get_text() if date_tag else None

#         return [date, address]

#     except Exception as e:
#         with open('log.txt', 'a') as f:
#             print(f"Error processing {url}: {e}", file=f)
#         return None


# def main(start_row, end_row):
#     with open('./sample.csv', 'r', newline='', encoding='utf-8') as urlfile:
#         url_reader = csv.reader(urlfile)
#         rows = list(url_reader)
#         header = rows[0]

#     count = 0
#     max_requests_before_delay = 500
#     delay_seconds = 10

#     updated_header = [header + ['length', 'address']]
#     with open(f'./scrapper/data/campaign_info_updated_{start_row}_{end_row}.csv', 'a', newline='', encoding='utf-8') as csvfile:
#         url_writer = csv.writer(csvfile)
#         url_writer.writerow(updated_header)

#     for idx, row in enumerate(rows[1:], start=1):
#         if start_row <= idx <= end_row:
#             url = row[1]  # Change index to 1 to get the URL from the second column

#             print(f"Extracting specific element from: {url}")
#             result = extract_date(url)

#             if result and all(item is not None for item in result):
#                 date, address = result[0], result[1]

#                 now = "Nov 6, 2023"  # the date that we scrape the data
#                 date_raw = date.split()
#                 day = date_raw[1][:-3]

#                 # Convert the date strings to datetime objects
#                 now = datetime.strptime(now, "%b %d, %Y")
#                 created_date = datetime(int(date_raw[2]), datetime.strptime(date_raw[0], "%B").month, int(day))

#                 time_difference = now - created_date

#                 # Extract the number of days from the timedelta object
#                 days_difference = time_difference.days

#                 # Add the length and address as new columns
#                 row.append(days_difference)
#                 row.append(address)

#                 # Write the updated row to the file immediately
#                 with open(f'./scrapper/data/campaign_info_updated_{start_row}_{end_row}.csv', 'a', newline='', encoding='utf-8') as csvfile:
#                     url_writer = csv.writer(csvfile)
#                     url_writer.writerow(row)

#             count += 1
#             if count % max_requests_before_delay == 0:
#                 print(f"Waiting for {delay_seconds} seconds to avoid being detected as a bot...")
#                 time.sleep(delay_seconds)

#     print(f"Updated rows written to ./scrapper/data/campaign_info_updated_{start_row}_{end_row}.csv")


# if __name__ == "__main__":
#     # Set up argparse for command-line arguments
#     parser = argparse.ArgumentParser(description='Crawl GoFundMe data for a specified range of rows.')
#     parser.add_argument('start_row', type=int, help='Starting row index for data extraction')
#     parser.add_argument('end_row', type=int, help='Ending row index for data extraction')

#     # Parse command-line arguments
#     args = parser.parse_args()

#     # Call the main function with provided arguments
#     main(args.start_row, args.end_row)
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

        # Find the div tag containing the user information, extract the address
        user_info_div = soup.find('div', {'class': 'm-campaign-members-main-organizer'})
        address = user_info_div.find_all('div', {'class': 'hrt-text-body-sm'})[1].get_text() if user_info_div else None

        # Find the span tag containing the created date
        date_tag = soup.find('span', {'class': 'm-campaign-byline-created a-created-date'})
        date = date_tag.get_text() if date_tag else None

        return [date, address]

    except Exception as e:
        with open('log.txt', 'a') as f:
            print(f"Error processing {url}: {e}", file=f)
        return None


def main(start_row, end_row):
    with open('./sample.csv', 'r', newline='', encoding='utf-8') as urlfile:
        url_reader = csv.reader(urlfile)
        rows = list(url_reader)
        header = rows[0]

    count = 0
    max_requests_before_delay = 500
    delay_seconds = 10

    with open(f'./scrapper/data/campaign_info_updated_{start_row}_{end_row}.csv', 'a', newline='', encoding='utf-8') as csvfile:
        url_writer = csv.writer(csvfile)

        # Write the header to the file
        url_writer.writerow(header + ['length', 'address'])

        for idx, row in enumerate(rows[1:], start=1):
            if start_row <= idx <= end_row:
                url = row[1]  # Change index to 1 to get the URL from the second column

                print(f"Extracting specific element from: {url}")
                result = extract_date(url)

                if result and all(item is not None for item in result):
                    date, address = result[0], result[1]

                    now = "Nov 6, 2023"  # the date that we scrape the data
                    date_raw = date.split()
                    day = date_raw[1][:-3]

                    # Convert the date strings to datetime objects
                    now = datetime.strptime(now, "%b %d, %Y")
                    created_date = datetime(int(date_raw[2]), datetime.strptime(date_raw[0], "%B").month, int(day))

                    time_difference = now - created_date

                    # Extract the number of days from the timedelta object
                    days_difference = time_difference.days

                    # Add the length and address as new columns
                    row.append(days_difference)
                    row.append(address)

                    # Write the updated row to the file immediately
                    url_writer.writerow(row)

                count += 1
                if count % max_requests_before_delay == 0:
                    print(f"Waiting for {delay_seconds} seconds to avoid being detected as a bot...")
                    time.sleep(delay_seconds)

    print(f"Updated rows written to ./scrapper/data/campaign_info_updated_{start_row}_{end_row}.csv")


if __name__ == "__main__":
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(description='Crawl GoFundMe data for a specified range of rows.')
    parser.add_argument('start_row', type=int, help='Starting row index for data extraction')
    parser.add_argument('end_row', type=int, help='Ending row index for data extraction')

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the main function with provided arguments
    main(args.start_row, args.end_row)
