# Texas Justic Initiative - data processing

To learn more about TJI, visit our website at www.texasjusticeinitiative.org

## The data itself lives in our [data.world account](https://data.world/tji)

## About this repo

Many different datasets and files are used by the TJI website and our analyses. All non-manual data processing steps live in this repo.

All scripts/notebooks to clean, scrape, merge or otherwise process data files. There are two main folders:
  * [data_scraping/](https://github.com/texas-justice-initiative/data-processing/tree/master/data_scraping) - reads data from anywhere on the internet and writes csvs to [TJI's data.world account](https://data.world/tji) 
  * [data_cleaning/](https://github.com/texas-justice-initiative/data-processing/tree/master/data_cleaning) - files should both be READ FROM and WRITTEN TO the TJI data.world account. Any dataset not on data.world should be scraped or manually added to data.world first.
    * The output of a cleaning script should be a file whose name begins with `clean_`.

## TJI datasets, their means of creation, and data quirks to be aware of

#### [Updated: 2018-05-21]
----
### Project: Texas Deaths in Custody from 2005-present - [tji/tx-deaths-in-custody-2005-2015](https://data.world/tji/tx-deaths-in-custody-2005-2015/workspace/dataset)
----
* **File:** [`cleaned_custodial_death_reports.csv`](https://data.world/tji/tx-deaths-in-custody-2005-2015/workspace/file?filename=cleaned_custodial_death_reports.csv)
* **Description:** All Texas custodial deaths since 2005 (a "custodial death" is a death in jail, prison, custody, or the process of arrest -- see [Wikipedia](https://en.wikipedia.org/wiki/Death_in_custody#United_States))
* **Generation pipeline:**
  1. (Manual) TJI staff manually parse and enter the data into a master spreadsheet, `CDR Reports All.xlsx`, in Google Drive, which is synced to data.world [here](https://data.world/tji/tx-deaths-in-custody-2005-2015/workspace/file?filename=CDR+Reports+All.xlsx)
  1. A member of TJI runs this notebook to create the final file: [`data_cleaning/clean_cdr.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_cdr.ipynb)
* **Quirks**
  1. The Texas Department of Criminal Justice, which runs Texas prisons and a few state jails, until 2013 did NOT file custodial death reports for prisoners that died in an _inpatient_ setting. In practice, this means that a good number of deaths from natural causes of state prisoners were not reported from 2005-2012 (you can see this clearly in the exploratory analysis [here](https://github.com/texas-justice-initiative/analysis/blob/master/analyses/cdr_explore.ipynb)). Thus, if you simply plot custodial deaths over time, you'll see a jump from 2012 to 2013 for this reason.
  1. The form that was used to report custodial deaths changed in 2016, and by 2017 all records use the new form. The forms differ, but many questions are nearly the same. You can see the [forms](https://github.com/texas-justice-initiative/data-processing/tree/master/forms) in this repo. The cleaning script attempts to match fields and options across form versions so the output file only has data that is consistent across all versions. See the `form_version` column in the output file to see what version was used for entering that record.
  1. Diligent collection of custodial deaths in texas began in 2005, but inconsistent data exists as far back as 1980. To see these older files, explore the `older_versions` tab of raw data file [here](https://data.world/tji/tx-deaths-in-custody-2005-2015/workspace/file?filename=CDR+Reports+All.xlsx).

----
### Project: Officer Involved Shootings [tji/officer-involved-shootings](https://data.world/tji/officer-involved-shootings/workspace/dataset)
----
* **File:** [`shot_civilians.csv`](https://data.world/tji/officer-involved-shootings/workspace/file?filename=shot_civilians.csv)
* **Description:** Civilians shot by police, late 2015 - present
* **Generation pipeline:**
  1. A TJI bot monitors the [Texas Attorney General's website](https://www.texasattorneygeneral.gov/cj/peace-officer-involved-shooting-report) for new OIS reports.
  1. New reports are emailed to TJI staff.
  1. TJI staff manually parse and enter the data into a master spreadsheet, `OIS.xlsx`, in Google Drive, which is synced to data.world [here](https://data.world/tji/officer-involved-shootings/workspace/file?filename=OIS.xlsx.xlsx)
  1. A member of TJI runs this notebook to create the final file: [`data_cleaning/clean_ois_civilians_shot.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_ois_civilians_shot.ipynb)
* **Quirks**
  1. There is one record for every _shot civilian_. Thus, if a single incident results in multiple civilians shot, there will be multiple rows with largely duplicate information (e.g. address, date, officer details, etc). Incident-level analysis should de-duplicate, say by matching on date and address.
  1. It's hard to know exactly how many officers were on scene. In theory, there are two pieces of information in each record that reveal this information. First, there is a checkbox on the form called "multiple officers involved," which is checked about 80% of the time. Second, there are spaces in the form for the details (agency, gender, race, age, etc) of each officer involved. However, when "multiple officers involved" is checked, only ~half the time do details for more than one officer exist. Similarly, sometimes "multiple officers involved" is NOT checked, yet details for multiple officers exist. It's unclear what to make of this information.
----
* **File:** [`shot_officers.csv`](https://data.world/tji/officer-involved-shootings/workspace/file?filename=shot_officers.csv)
* **Description:** Peace officers shot in the line of duty, late 2015 - present
* **Generation pipeline:**
  1. Identical to `shot_civilians.csv` above, except that in the last step, a different notebook is run: [`data_cleaning/clean_ois_officers_shot.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_ois_officers_shot.ipynb)
* **Quirks**
  1. Analogous to the previous file, there is one record for every _shot officer_. Thus, if a single incident results in officers civilians shot, there will be multiple rows with largely duplicate information (e.g. address, date, civilian details, etc). Incident-level analysis should de-duplicate, say by matching on date and address.
----
### Project: Auxiliary Datasets [tji/auxiliary-datasets](https://data.world/tji/auxiliary-datasets/workspace/dataset)
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
  1. TJI staff request data from [TCOLE](https://www.tcole.texas.gov/)
  1. TCOLE emails an excel file, which TJI staff place in Google Drive (`TCOLE.xlsx`)
  1. The first/only sheet of the Excel file is uploaded to data.world as [`raw_num_officers_by_agency.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=raw_num_officers_by_agency.csv)
  1. Run this notebook to generate the final data file: [`data_cleaning/clean_num_officers_by_agency.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_num_officers_by_agency.ipynb)
----
* **File:** [`agencies_and_counties.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=agencies_and_counties.csv)
* **Description:** List of texas police agencies (names are normalized) and the county they belong to
* **Generation pipeline:**
  1. This is also generated in the flow that creates `num_officers_by_agency.csv` above, via the same notebook: [`data_cleaning/clean_num_officers_by_agency.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_num_officers_by_agency.ipynb)
----
* **File:** [`list_of_texas_officers.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=list_of_texas_officers.csv)
* **Description:** Names, agencies, and demographics of all police officers in Texas.
* **Generation pipeline:**
  1. TJI staff request data from [TCOLE](https://www.tcole.texas.gov/)
  1. TCOLE sends an excel file, which TJI staff place in Google Drive (`Current appointed POs with certs and service time and gender- Ruth.xlsx`)
  1. Excel file uploaded to data.world as [`raw_list_of_texas_officers.csv`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=raw_list_of_texas_officers.csv)
  1. Run this notebook: [`data_cleaning/clean_list_of_texas_officers.ipynb`](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_list_of_texas_officers.ipynb)
----
* **File:** [`ucr_crime_by_county_2016.xls`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=ucr_crime_by_county_2016.xls) (and [`2015`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=ucr_crime_by_county_2015.xls) and [`2014`](https://data.world/tji/auxiliary-datasets/workspace/file?filename=ucr_crime_by_county_2014.xls))
* **Description:** Crime by county in Texas from the [FBI's Uniform Crime Report](https://ucr.fbi.gov/)
* **Generation pipeline:**
  1. Direct downloaded to data.world from the FBI website. The source pages are here for [2016](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/tables/table-8/table-8-state-cuts/texas.xls), [2015](https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/tables/table-10/table-10-state-pieces/table_10_offenses_known_to_law_enforcement_texas_by_metropolitan_and_nonmetropolitan_counties_2015.xls), and [2014](https://ucr.fbi.gov/crime-in-the-u.s/2014/crime-in-the-u.s.-2014/tables/table-10/table-10-pieces/Table_10_Offenses_Known_to_Law_Enforcement_Texas_by_Metropolitan_and_Nonmetropolitan_Counties_2014.xls).


