# Datasheet: Composition 

# What do the instances that comprise the dataset represent? 

The data set includes all deaths in custody (a "custodial death" is a death in jail, prison, custody, or the process of arrest) in Texas since 2005, as reported to the Office of the Attorney General. As of 02/01/2020, there are 9980 death records in the data set. Each row of the data set represents a deceased person who died in custody in Texas. Currently, 5 custody types exist: `['JAIL - COUNTY' 'POLICE CUSTODY (PRE-BOOKING)' 'PRIVATE FACILITY'
 'PRISON' 'JAIL - MUNICIPAL']` 

The data set has 51 columns.

|                                                | Description   | Data Types   | Suggested Data Types   |   No. Missing Values |
|:-----------------------------------------------|:--------------|:-------------|:-----------------------|---------------------:|
| record_id                                      | TBD           | object       | str                    |                    0 |
| num_revisions                                  | TBD           | float64      | int                    |                 2531 |
| form_version                                   | TBD           | object       | str                    |                    0 |
| report_date                                    | TBD           | object       | np.datetime64          |                  148 |
| date_time_of_custody_or_incident               | TBD           | object       | np.datetime64          |                  151 |
| name_first                                     | TBD           | object       | str                    |                    0 |
| name_last                                      | TBD           | object       | str                    |                    0 |
| name_middle                                    | TBD           | object       | str                    |                 4446 |
| name_suffix                                    | TBD           | object       | str                    |                 9486 |
| name_full                                      | TBD           | object       | str                    |                    0 |
| date_of_birth                                  | TBD           | object       | np.datetime64          |                  154 |
| age_at_time_of_death                           | TBD           | float64      | int                    |                    8 |
| sex                                            | TBD           | object       | str                    |                    0 |
| race                                           | TBD           | object       | str                    |                   37 |
| death_date                                     | TBD           | object       | np.datetime64          |                    0 |
| death_date_and_time                            | TBD           | object       | np.datetime64          |                    0 |
| death_location_county                          | TBD           | object       | str                    |                 2519 |
| death_location_city                            | TBD           | object       | str                    |                  155 |
| death_location_street_address                  | TBD           | object       | str                    |                 2521 |
| death_location_type                            | TBD           | object       | str                    |                 2519 |
| death_location_type_other                      | TBD           | object       | str                    |                 9839 |
| death_from_pre_existing_medical_condition      | TBD           | object       | str                    |                  149 |
| manner_of_death                                | TBD           | object       | str                    |                    0 |
| manner_of_death_description                    | TBD           | object       | str                    |                 4412 |
| means_of_death                                 | TBD           | object       | str                    |                 2519 |
| means_of_death_other                           | TBD           | object       | str                    |                 9291 |
| medical_cause_of_death                         | TBD           | object       | str                    |                 2528 |
| medical_examinor_coroner_evalution             | TBD           | object       | str                    |                  152 |
| medical_treatment                              | TBD           | object       | str                    |                  148 |
| days_from_custody_to_death                     | TBD           | float64      | int                    |                  159 |
| who_caused_death_in_homicide_or_accident       | TBD           | object       | str                    |                    4 |
| who_caused_death_in_homicide_or_accident_other | TBD           | object       | str                    |                 9933 |
| offense_1                                      | TBD           | object       | str                    |                  164 |
| offense_2                                      | TBD           | object       | str                    |                 5679 |
| offense_3                                      | TBD           | object       | str                    |                 7009 |
| type_of_offense                                | TBD           | object       | str                    |                 5254 |
| type_of_offense_other                          | TBD           | object       | str                    |                 8930 |
| were_the_charges                               | TBD           | object       | str                    |                  147 |
| facility_entry_date_time                       | TBD           | object       | np.datetime64          |                 4584 |
| type_of_custody                                | TBD           | object       | str                    |                    0 |
| specific_type_of_custody_facility              | TBD           | object       | str                    |                  280 |
| agency_address                                 | TBD           | object       | str                    |                 2519 |
| agency_city                                    | TBD           | object       | str                    |                 2519 |
| agency_county                                  | TBD           | object       | str                    |                   19 |
| agency_name                                    | TBD           | object       | str                    |                    0 |
| agency_zip                                     | TBD           | float64      | int                    |                 2520 |
| entry_behavior                                 | TBD           | object       | str                    |                 9255 |
| other_behavior                                 | TBD           | object       | str                    |                 9805 |
| exhibit_any_medical_problems                   | TBD           | object       | str                    |                 7900 |
| exhibit_any_mental_health_problems             | TBD           | object       | str                    |                 7930 |
| make_suicidal_statements                       | TBD           | object       | str                    |                 7932 |

As of 2020/03/08, there are 9980 death records in the data set and each row has 51 attributes (columns). See above.

# Completeness and sampling bias 

## Does the data set contain all possible instances or is it a sample from a larger set? 

The data set has a sampling bias. According to the [Texas Sunset Advisory Commission Report on Jail Standards](https://www.sunset.texas.gov/public/uploads/files/reports/Texas%20Commission%20on%20Jail%20Standards%20SER.pdf):

>"On multiple occasions, counties have not reported a death because they claim that at the time of death the inmate was not in custody. This is because when the inmate's medical condition became acute, and the jail had either released the inmate abruptly on a Personal Recognizance Bond (PR Bond) without the inmate's signature orimmediately transported the inmate to a hospital. In their opinion, this negates the requirements to report the death as they do not believe the individual is in custody. This most often occurs with a suicide attempt that later results in the inmate's death at a hospital.

In a way, this data can be considered as a subset of the entire population in custody where the criteria for creating the subset are whether the people in custody are alive.

# Raw data and data preprocessing: [TJI's Analysis Pipeline](https://texasjusticeinitiative.org/about-the-data/)

After an incident, the governmental agency in which it occurred (i.e. a county jail etc.) is required to file a report for the respective incident with the Texas Office of the Attorney General (OAG) within 30 days. The Texas OAG publishes the raw PDFs of these reports that are queriable. Through open records requests filed monthly, TJI obtains data from the reports through the Texas OAG. We then clean, analyze, and present the data to the public – both in the form of a full data set and in comparative graphics – through our analysis pipeline.

Once a month, TJI staff request new custodial death reports from the Texas Department of Criminal Justice. A spreadsheet is emailed to staff members, who copy/paste the new rows to the bottom of a master spreadsheet, in Google Drive, which is synced to our [data.world temporary files repo](https://data.world/tji/raw-and-processing/workspace/file?filename=CDR+Reports+All.xlsx).

Once the raw data is cleaned with our [preprocessing script](https://github.com/texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_cdr.ipynb), csv files are generated and then uploaded to data.world. For our website, the csv files are transformed to JSON files, which are uploaded to Amazon Web Services (AWS). The AWS-hosted JSON files are used to display TJI website graphs.

# Label or target

There is no label or target associated with this dataset. However, depending on the purpose of analyses, it is possible that certain categotical columns such as gender or locations can become a target. Since every row is a person who died in custody, one can consider this dataset as single-labelled given that the label is whether the person is alive.

# Missing data

The data set has missing information. The number of missing rows per column is summarized in the table above. Some columns have both 'Unknown' and missing values. These are different. In the custodial death report, certain questions have 'Unknown' as a checkbox. Thus, 'Unknown' means this box has been checked and a missing value means the question was not answered at all. Sometimes OAG will release amended reports after certain investigations to address missing values. In this case, the amended reports will overwrite the old ones.

# Recommended data splits

Currently the dataset does not have a label and thus we do not have any recommendations on data splits. However, please consult TJI first if you are planning to conduct any predictive analyses by choosing one of the columns as a label.

# Errors, noise, and redundancies

## Missing reports

The Texas Department of Criminal Justice, which runs Texas prisons and a few state jails, until 2013 did NOT file custodial death reports for prisoners that died in an inpatient setting. In practice, this means that a good number of deaths from natural causes of state prisoners were not reported from 2005-2012 (you can see this clearly in [the exploratory analysis](https://github.com/texas-justice-initiative/analysis/blob/master/analyses/cdr_explore.ipynb)). Thus, if you simply plot custodial deaths over time, you'll see a jump from 2012 to 2013 for this reason.

## Change in the record format

The form that was used to report custodial deaths changed in 2016, and by 2017 all records use the new form. The forms differ, but many questions are nearly the same. You can see the forms in [our github repo](https://github.com/texas-justice-initiative/data-processing/tree/master/forms). The cleaning script attempts to match fields and options across form versions so the output file only has data that is consistent across all versions. See the `form_version` column in the output file to see what version was used for entering that record.

## Data inconsistency

Diligent collection of custodial deaths in texas began in 2005, but inconsistent data exists as far back as 1980. To see these older files, check [our data.world repository](https://data.world/tji/raw-and-processing/workspace/file?filename=CDR+Reports+All.xlsx).

# Dependencies

The data set is self-contained but it is based on [the raw OAG reports](https://oagtx.force.com/cdr/cdrreportdeaths).

## Are there guarantees that the sources will exist, and remain constant, over time?

As we mentioned in the previous section, there has been a change in the record format. We expect this will very likely to happen in the future.

## Are there official archival versions of the complete data set (i.e., including the external resources as they existed at the time the data set was created)?

The OAG website has [the raw reports](https://oagtx.force.com/cdr/cdrreportdeaths). The csv files of the older forms exist in [our data.world repository](https://data.world/tji/raw-and-processing/workspace/file?filename=CDR+Reports+All.xlsx).

## Are there any restrictions (e.g., licenses, fees) associated with any of the external resources that might apply to a future user?

The data are public records and thus there are no restrictions.

# Sensitive information

## Confidentiality: Does the data set contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor-patient confidentiality, data that includes the content of individuals’ non-public communications)?

At the moment, since our data set is based on the public record published by OAG, it does not have any confidential information. However, it has information about medical conditions of the deceased. Although medical privacy after death is a debatable topic, according to the [Summary of the HIPAA Privacy Rule](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html), 'Law Enforcement Purposes' fall in their 'Permitted Uses and Disclosures'.

## Subpopulation identification

The data set identifies subpopulations by age (`age_at_time_of_death`), gender (`sex`, binary), and race (`race`: ['OTHER' 'HISPANIC' 'BLACK' 'WHITE' nan]). Their respective distributions are the following:

|       |   age_at_time_of_death |
|:------|-----------------------:|
| count |              9972      |
| mean  |                49.3686 |
| std   |                15.5414 |
| min   |               -35      |
| 25%   |                38      |
| 50%   |                51      |
| 75%   |                60      |
| max   |                93      |

| sex    |   BLACK |   HISPANIC |   OTHER |   WHITE |
|:-------|--------:|-----------:|--------:|--------:|
| FEMALE |     186 |         95 |       1 |     291 |
| MALE   |    2693 |       2668 |      92 |    3917 |

Note that the identification of gender and race are NOT based on self-reporting.

## Individual identification

Every person is identifiable in the dataset becasue their full name is revealed in the dataset.

## Sensitive information

Even though the dataset contains the information of the deceased, it contains sensitive information such as race, gender, medical conditions, and the location of incident.