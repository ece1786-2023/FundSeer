from src.scrapingtools.scrapemanager import ScrapeManager
from src.scrapingtools.urlcollectors import URLCollector, WaybackURLCollector
from src import data_io
from pathlib import Path

# SCRAPE ON BOTH GFM AND WAYBACK MACHINE
# create a table of all urls to scrape, only need to generate once
tablepath, urls_df = URLCollector().create_url_table()
wbcollector = WaybackURLCollector(start_year=2019,end_year=2021)
wbtablepath, wburls_df = wbcollector.create_url_table()
masterpath, master_df = wbcollector.compare_url_tables(urls_df, wburls_df)
# start scraping
manager = ScrapeManager(urltable_path=masterpath)
manager.deploy()
