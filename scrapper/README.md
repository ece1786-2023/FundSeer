# GoFundMe Data Scrapper

## Overview

This folder provides a set of Python scripts to scrape data from GoFundMe campaigns. Follow the steps below to collect information from GoFundMe URLs and generate statistics based on the collected data.

## Prerequisites

Make sure you have the following installed before running the scripts:

- selenium 4.15.2
- beautifulsoup4 4.12.0
- requests 2.28.2

To install, run `pip install -r scrapper/requirements.txt`
## Usage

### 1. Run `gfm_url_scrapper.py`

This script collects URLs of different GoFundMe campaigns. Execute the following command:

```bash
python3 gfm_url_scrapper.py
```

This will generate a file `gfm_urls.csv` under `data/raw_data named` where each row contains the collected campaign URLs.

### 2. Run `gfm_data_scrapper.py`

Use this script to collect information from the GoFundMe campaign URLs obtained in the previous step. Run the following command:

```bash
python3 gfm_data_scrapper.py a b
```

Where `a` is the starting row number, `b` is ending row number of the url table. The script will save the collected data in a file named `campaign_info_{start_row}_{end_row}.csv`. 

Alternatively, can use a multiprocessing version of the scraper by running `gfm_data_scrapper_multiprocessing.py`. However, currently there may be issue with being detected as bot and hence denial of request issue with this version of the scrapper.

### 3. Run `statistics.py`

To generate statistics based on the collected data, run the following command:

```bash
python3 statistic.py
```

This script will provide insights and statistical information about the crawled GoFundMe data.

## Note

- Ensure that you are respectful and compliant with GoFundMe's terms of service while using this tool.
- Use the collected data responsibly and ethically.
- Can use `stats_final.py` to gain some final insights on the data
