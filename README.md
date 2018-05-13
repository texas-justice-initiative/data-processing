# Texas Justic Initiative - data processing

To learn more about TJI, visit our website at www.texasjusticeinitiative.org

## The data itself lives in our [data.world account](https://data.world/tji)

## About this repo

Many different datasets and files are used by the TJI website and our analyses. All non-manual data processing steps live in this repo.

All scripts/notebooks to clean, scrape, merge or otherwise process data files. There are two main folders:
  * [data_scraping/](https://github.com/texas-justice-initiative/data-processing/tree/master/data_scraping) - reads data from anywhere on the internet and writes csvs to [TJI's data.world account](https://data.world/tji) 
    * Any written dataset that is not ready for analysis should have a `raw_` prefix.
  * [data_cleaning/](https://github.com/texas-justice-initiative/data-processing/tree/master/data_cleaning) - files should both be READ FROM and WRITTEN TO the TJI data.world account. Any dataset not on data.world should be scraped or manually added to data.world first.
    * If you clean a previously `raw_` datafile, the output file of your cleaning script should begin with `clean_`.

## TJI datasets (and their means of creation)
#### [Updated: 2018-05-12]
### Project: [tji/auxiliary-datasets](https://data.world/tji/auxiliary-datasets/workspace/dataset)
----
* **File:** [`texas_counties.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=texas_counties.csv)
* **Description:** List of Texas counties and their "seat" city
* **Generation pipeline:**
  1. Run this notebook: [`data_scraping/scrape_texas_county_names.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_scraping/scrape_texas_county_names.ipynb)
      * Data is fetched from [this Wikipedia page](https://en.wikipedia.org/wiki/List_of_counties_in_Texas)
----
* **File:** [`census_data_by_county.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=census_data_by_county.csv)
* **Description:** Extensive US Census data (2010 and 2016), one row per Texas county.
* **Generation pipeline:**
  1. Run this notebook: [`data_scraping/scrape_census_data_by_county.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_scraping/scrape_census_data_by_county.ipynb)
      * Data is fetched from the US Census QuickFacts (e.g. [here](https://www.census.gov/quickfacts/fact/table/andrewscountytexas))
----
* **File:** [`num_officers_by_agency.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=num_officers_by_agency.csv)
* **Description:** Number of officers in each Texas police department
* **Generation pipeline:**
  1. (Manual) Eva requests data from [TCOLE](https://www.tcole.texas.gov/)
  1. (Manual) TCOLE sends an excel file, which Eva places in Google Drive (`TCOLE.xlsx`)
  1. (Manual) Excel file uploaded to data.world as [`raw_num_officers_by_agency.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=raw_num_officers_by_agency.csv)
  1. Run this notebook: [`data_cleaning/clean_num_officers_by_agency.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_num_officers_by_agency.ipynb)
----
* **File:** [`agencies_and_counties.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=agencies_and_counties.csv)
* **Description:** List of texas police agencies (names are normalized) and the county they belong to
* **Generation pipeline:**
  1. This is also generated in the flow that creates `num_officers_by_agency.csv` above, via the same notebook: [`data_cleaning/clean_num_officers_by_agency.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_num_officers_by_agency.ipynb)
----
* **File:** [`list_of_texas_officers.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=list_of_texas_officers.csv)
* **Description:** Names, agencies, and demographics of all police officers in Texas.
* **Generation pipeline:**
  1. (Manual) Eva requests data from [TCOLE](https://www.tcole.texas.gov/)
  1. (Manual) TCOLE sends an excel file, which Eva places in Google Drive (`Current appointed POs with certs and service time and gender- Ruth.xlsx`)
  1. (Manual) Excel file uploaded to data.world as [`raw_list_of_texas_officers.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=raw_list_of_texas_officers.csv)
  1. Run this notebook: [`data_cleaning/clean_list_of_texas_officers.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_list_of_texas_officers.ipynb)
----
* **File:** [`ucr_crime_by_county_2016.xls`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=ucr_crime_by_county_2016.xls) (and [`2015`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=ucr_crime_by_county_2015.xls) and [`2014`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=ucr_crime_by_county_2014.xls))
* **Description:** Crime by county in Texas from the [FBI's Uniform Crime Report](https://ucr.fbi.gov/)
* **Generation pipeline:**
  1. Direct downloaded to data.world from the FBI website. The source pages are here for [2016](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/tables/table-8/table-8-state-cuts/texas.xls), [2015](https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/tables/table-10/table-10-state-pieces/table_10_offenses_known_to_law_enforcement_texas_by_metropolitan_and_nonmetropolitan_counties_2015.xls), and [2014](https://ucr.fbi.gov/crime-in-the-u.s/2014/crime-in-the-u.s.-2014/tables/table-10/table-10-pieces/Table_10_Offenses_Known_to_Law_Enforcement_Texas_by_Metropolitan_and_Nonmetropolitan_Counties_2014.xls).


