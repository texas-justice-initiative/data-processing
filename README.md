# Texas Justic Initiative - data processing

To learn more about TJI, visit our website at www.texasjusticeinitiative.org

## About this repo

All scripts/notebooks to clean, scrape, merge or otherwise process data files. There are two main folders:
  * data_scraping/ - reads data from anywhere on the internet and writes csvs to [TJI's data.world account](https://data.world/tji) 
    * Any written dataset that is not ready for analysis should have a `raw_` prefix.
  * data_cleaning/ - files should both be READ FROM and WRITTEN TO the TJI data.world account. Any dataset not on data.world should be scraped or manually added to data.world first.
    * If you clean a previously `raw_` datafile, the output file of your cleaning script should begin with `clean_`.
