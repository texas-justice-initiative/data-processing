import pandas as pd
import pickle
import time


def save_obj(obj, pathname):
    # Save an object file as pickle
    with open(pathname, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(pathname):
    # Load a pickle file
    with open(pathname, 'rb') as f:
        return pickle.load(f)


df = pd.read_csv('../../Data/Website/tji_custodialDeaths.csv')

# What do the instances that comprise the dataset represent?
s_instances = '# Datasheet: Composition \n\n' \
              '# What do the instances that comprise the dataset represent? \n\n' \
              'The dataset includes all deaths in custody (a "custodial death" is a death in jail, ' \
              'prison, custody, or the process of arrest) in Texas since 2005, ' \
              'as reported to the Office of the Attorney General. ' \
              'As of 02/01/2020, there are {n_rows} death records in the dataset. ' \
              'Each row of the dataset represents a deceased person who died in custody in Texas. ' \
              'Currently, {n_type_of_custody} custody types exist: `{types_of_custody}` \n\n' \
              'The dataset has {n_columns} columns.'. \
    format(n_rows=df.shape[0],
           n_type_of_custody=df['type_of_custody'].nunique(),
           types_of_custody=df['type_of_custody'].unique(),
           n_columns=df.shape[1])

# Data summary for the markdown table
suggest_data_type_dict = load_obj('DIC_suggest_data_type_dict.pkl')
df_summary = pd.DataFrame(index=df.columns)
df_summary['Description'] = 'TBD'
df_summary['Data Types'] = df.dtypes
df_summary['Suggested Data Types'] = suggest_data_type_dict.values()
df_summary['No. Missing Values'] = df.isnull().sum()

# to use this, tabulate should be installed
s_summary_table = df_summary.to_markdown()

# Size
s_size = 'As of {current_date}, there are {n_rows} death records in the dataset ' \
         'and each row has {n_columns} attributes (columns). See above.'.\
    format(current_date=time.strftime('%Y/%m/%d', time.gmtime()),
           n_rows=df.shape[0],
           n_columns=df.shape[1])

s_completeness = '# Completeness and sampling bias \n\n' \
                 '## Does the dataset contain all possible instances or is it a sample from a larger set? \n\n' \
                 'The dataset has a sampling bias. According to the [Texas Sunset Advisory Commission Report on ' \
                 'Jail Standards](https://www.sunset.texas.gov/public/uploads/files/reports/' \
                 'Texas%20Commission%20on%20Jail%20Standards%20SER.pdf):\n\n' \
                 '>"On multiple occasions, counties have not reported a death because they claim that ' \
                 "at the time of death the inmate was not in custody. This is because when the inmate's " \
                 "medical condition became acute, and the jail had either released the inmate abruptly " \
                 "on a Personal Recognizance Bond (PR Bond) without the inmate's signature or" \
                 "immediately transported the inmate to a hospital. In their opinion, this negates the requirements " \
                 "to report the death as they do not believe the individual is in custody. This most often occurs " \
                 "with a suicide attempt that later results in the inmate's death at a hospital.\n\n" \
                 "In a way, this data can be considered as a subset of the entire population in custody " \
                 "where the criteria for creating the subset are whether the people in custody are alive."

s_preprocessing = "# Raw data and data preprocessing: [TJI's Analysis Pipeline]" \
                  "(https://texasjusticeinitiative.org/about-the-data/)\n\n" \
                  "After an incident, the governmental agency in which it occurred (i.e. a county jail etc.) is " \
                  "required to file a report for the respective incident with the Texas Office of the Attorney " \
                  "General (OAG) within 30 days. The Texas OAG publishes the raw PDFs of these reports " \
                  "that are queriable. Through open records requests filed monthly, TJI obtains data " \
                  "from the reports through the Texas OAG. We then clean, analyze, and present the data " \
                  "to the public – both in the form of a full dataset and in comparative graphics" \
                  " – through our analysis pipeline.\n\n" \
                  "Once a month, TJI staff request new custodial death reports from the Texas Department of " \
                  "Criminal Justice. A spreadsheet is emailed to staff members, who copy/paste the new rows " \
                  "to the bottom of a master spreadsheet, in Google Drive, which is synced to our " \
                  "[data.world temporary files repo](https://data.world/tji/raw-and-processing/workspace/file?" \
                  "filename=CDR+Reports+All.xlsx).\n\n" \
                  "Once the raw data is cleaned with our [preprocessing script](https://github.com/" \
                  "texas-justice-initiative/data-processing/blob/master/data_cleaning/clean_cdr.ipynb), " \
                  "csv files are generated and then uploaded to data.world. For our website, the csv files are " \
                  "transformed to JSON files, which are uploaded to Amazon Web Services (AWS). " \
                  "The AWS-hosted JSON files are used to display TJI website graphs."

s_label = "# Label or target\n\n" \
          "There is no label or target associated with this dataset. However, depending on " \
          "the purpose of analyses, it is possible that certain categotical columns " \
          "such as gender or locations can become a target. Since every row is a person " \
          "who died in custody, one can consider this dataset as single-labelled given " \
          "that the label is whether the person is alive."

s_missing = "# Missing data\n\n" \
            "The dataset has missing information. The number of missing rows per column is summarized " \
            "in the table above. Some columns have both 'Unknown' and missing values. These are different. " \
            "In the custodial death report, certain questions have 'Unknown' as a checkbox. Thus, 'Unknown' " \
            "means this box has been checked and a missing value means the question was not answered at all. " \
            "Sometimes OAG will release amended reports after certain investigations to address missing values. " \
            "In this case, the amended reports will overwrite the old ones."

s_recommended_data_split = "# Recommended data splits\n\n" \
                           "Currently the dataset does not have a label and thus we do not have " \
                           "any recommendations on data splits. However, please consult TJI first if you are " \
                           "planning to conduct any predictive analyses by choosing one of the columns as a label."

s_gotchas = "# Errors, noise, and redundancies\n\n" \
            "## Missing reports\n\n" \
            "The Texas Department of Criminal Justice, which runs Texas prisons and a few state jails, " \
            "until 2013 did NOT file custodial death reports for prisoners that died in an inpatient setting. " \
            "In practice, this means that a good number of deaths from natural causes of state prisoners were not " \
            "reported from 2005-2012 (you can see this clearly in [the exploratory analysis](https://github.com/" \
            "texas-justice-initiative/analysis/blob/master/analyses/cdr_explore.ipynb)). " \
            "Thus, if you simply plot custodial deaths over time, you'll see a jump " \
            "from 2012 to 2013 for this reason.\n\n" \
            "## Change in the record format\n\n" \
            "The form that was used to report custodial deaths changed in 2016, and by 2017 " \
            "all records use the new form. The forms differ, but many questions are nearly the same. " \
            "You can see the forms in [our github repo](https://github.com/texas-justice-initiative/" \
            "data-processing/tree/master/forms). The cleaning script attempts to match fields and options " \
            "across form versions so the output file only has data that is consistent across all versions. " \
            "See the `form_version` column in the output file to see what version was used for " \
            "entering that record.\n\n" \
            "## Data inconsistency\n\n" \
            "Diligent collection of custodial deaths in texas began in 2005, but inconsistent data exists " \
            "as far back as 1980. To see these older files, check " \
            "[our data.world repository](https://data.world/tji/raw-and-processing/workspace/file?" \
            "filename=CDR+Reports+All.xlsx)."

s_dependencies = "# Dependencies\n\n" \
                 "The dataset is self-contained but it is based on [the raw OAG reports](" \
                 "https://oagtx.force.com/cdr/cdrreportdeaths).\n\n" \
                 "## Are there guarantees that the sources will exist, and remain constant, over time?\n\n" \
                 "As we mentioned in the previous section, there has been a change in the record format. " \
                 "We expect this will very likely to happen in the future.\n\n" \
                 "## Are there official archival versions of the complete dataset " \
                 "(i.e., including the external resources as they existed at the time the dataset was created)?\n\n" \
                 "The OAG website has [the raw reports](https://oagtx.force.com/cdr/cdrreportdeaths). The csv files " \
                 "of the older forms exist in [our data.world repository](https://data.world/tji/" \
                 "raw-and-processing/workspace/file?filename=CDR+Reports+All.xlsx).\n\n" \
                 "## Are there any restrictions (e.g., licenses, fees) associated with any of the external " \
                 "resources that might apply to a future user?\n\n" \
                 "The data are public records and thus there are no restrictions."

s_confidentiality = "# Sensitive information\n\n" \
                    "## Confidentiality: Does the dataset contain data that might be considered confidential " \
                    "(e.g., data that is protected by legal privilege or by doctor-patient confidentiality, " \
                    "data that includes the content of individuals’ non-public communications)?\n\n" \
                    "At the moment, since our dataset is based on the public record published by OAG, " \
                    "it does not have any confidential information. However, it has information about medical " \
                    "conditions of the deceased. Although medical privacy after death is a debatable topic, " \
                    "according to the [Summary of the HIPAA Privacy Rule](https://www.hhs.gov/hipaa/for-professionals/" \
                    "privacy/laws-regulations/index.html), 'Law Enforcement Purposes' fall in their " \
                    "'Permitted Uses and Disclosures'."

s_subpopulation_identification_age_table = df['age_at_time_of_death'].describe().to_markdown()
s_subpopulation_identification_sex_race_table = pd.crosstab(df['sex'], df['race']).to_markdown()
s_subpopulation_identification = "## Subpopulation identification\n\n" \
                                 "The dataset identifies subpopulations by age (`age_at_time_of_death`), " \
                                 "gender (`sex`, binary), and race (`race`: {type_race}). Their respective " \
                                 "distributions are the following:\n\n" \
                                 "{subpopulation_identification_age_table}\n\n" \
                                 "{subpopulation_identification_sex_race_table}\n\n" \
                                 "Note that the identification of gender and race are NOT based on self-reporting.".\
    format(type_race=df['race'].unique(),
           subpopulation_identification_age_table=s_subpopulation_identification_age_table,
           subpopulation_identification_sex_race_table=s_subpopulation_identification_sex_race_table)

s_individual_identification = "## Individual identification\n\n" \
                              "Every person is identifiable in the dataset becasue their " \
                              "full name is revealed in the dataset."

s_sensitive_info = "## Sensitive information\n\n" \
                   "Even though the dataset contains the information of the deceased, " \
                   "it contains sensitive information such as race, gender, medical conditions, " \
                   "and the location of incident."

s_list = [s_instances, s_summary_table, s_size, s_completeness, s_preprocessing, s_label, s_missing,
          s_recommended_data_split, s_gotchas, s_dependencies, s_confidentiality, s_subpopulation_identification,
          s_individual_identification, s_sensitive_info]

s_joined = '\n\n'.join(s_list)

# writing a markdown file
f = open('datasheet_DIC_composition.md', 'w')
f.write(s_joined)
f.close()
