# [Datasheet](https://arxiv.org/abs/1803.09010): The Death in Custody

Any death of an individual while they are in a penal institution, in the custody of a peace officer or as a result of a peace officer’s use of force, in a jail, correctional facility, or state juvenile facility dies. After an incident, the governmental agency in which it occurred (i.e. a county jail etc.) is required to file a report for the respective incident with the Texas Office of the Attorney General (OAG) within 30 days. The Texas OAG publishes the raw PDFs of these reports. Through open records requests filed monthly, Texas Justice Initiative (TJI) obtains data from the reports through the Texas OAG. We then clean, analyze, and present the data to the public – both in the form of a full data set and in comparative graphics – through our analysis pipeline. Our analysis pipeline is summarized below. The scripts we use in the analysis pipeline can be found on our [GitHub](https://github.com/texas-justice-initiative) and on our [website](https://texasjusticeinitiative.org/about-the-data/).

The data is availabe at [website](https://texasjusticeinitiative.org/data/). Click the **Download (CSV)** button to access the file (file name: `tji_custodialDeaths.csv`)

# Motivation
## For what purpose was the dataset created? Who created this dataset?
In 2015, lawmakers passed legislation that required agencies to report shootings to the state. Paired with a decades-old law that mandates deaths by officer-involved shootings and in any other type of law enforcement custody are reported to the state, the laws set Texas apart from most other states in requiring such reporting by police.

Amanda Woog and Eva Ruth Moravec had each worked with one of the data sets independently but decided to join forces in 2016, when they co-founded the Texas Justice Initiative to build a portal for our criminal justice data. Through the portal and other tools, TJI makes the data available to the public in a user-friendly way. TJI also analyzes the data and explains our findings, and attempts to provide oversight by helping to ensure the data sets are complete and accurate.

We believe that with quality information, we can better understand each other, craft good policy, improve governance, ensure accountability and identify creative solutions. TJI hopes to promote informed discussion on controversial topics of grave importance and impact research that leads to police, detention, and sentencing policy reform. We hope our work will also encourage replication in other states, both by bringing attention to the Texas policies and how they do or do not work, and by creating a platform that can be duplicated using data from other states.

## What support was needed to make this dataset? 
### Who funded the creation of the dataset? 
### If there is an associated grant, provide the name of the grantor and the grant name and number.
### If it was supported by a company or government agency, give those details.

# Composition
## What do the instances that comprise the dataset represent?
The dataset includes all deaths in custody in Texas since 2005, as reported to the Office of the Attorney General. As of 02/01/2020, there are 9980 death records in the dataset. Each row of the dataset represents a deceased person who died in custody in Texas. Currently, in the dataset, 5 custody types:
- `JAIL - COUNTY`
- `POLICE CUSTODY (PRE-BOOKING)`
- `PRIVATE FACILITY`
- `PRISON`
- `JAIL - MUNICIPAL`

Are there multiple types of instances (e.g., movies, users, and ratings; people and interactions between them; nodes and edges)? Please provide a description.

### Size
How many instances are there in total (of each type, if appropriate)?

### Completeness and sampling bias
Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set? If the dataset is a sample, then what is the larger set? Is the sample representative of the larger set (e.g., geographic coverage)? If so, please describe how this representativeness was validated/verified. If it is not representative of the larger set, please describe why not (e.g., to cover a more diverse range of instances, because instances were withheld or unavailable).

### Raw data
What data does each instance consist of? “Raw” data (e.g., unprocessed text or images) or features? In either case, please provide a description.

### Label or target
Is there a label or target associated with each instance? If so,please provide a description.

### Missing data
Is any information missing from individual instances? If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include, e.g., redacted text.

### Relationships between individual instances
Are relationships between individual instances made explicit (e.g.,users’ movie ratings, social network links)? If so, please describe how these relationships are made explicit.

### Recommended data splits
Are there recommended data splits (e.g., training, development/validation, testing)? If so, please provide a description of these splits, explaining the rationale behind them.

### Errors, noise, and redundancies
Are there any errors, sources of noise, or redundancies in the dataset? If so, please provide a description.

### Dependencies
Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, tweets, other datasets)? If it links to or relies on external resources, a) are there guarantees that they will exist, and remain constant, over time; b) are there official archival versions of the complete dataset (i.e., including the external resources as they ex- isted at the time the dataset was created); c) are there any restrictions (e.g., licenses, fees) associated with any of the external resources that might apply to a future user? Please pro- vide descriptions of all external resources and any restrictions associated with them, as well as links or other access points, as appropriate.

### Sensitive information
#### Confidentiality
Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor-patient confidentiality, data that includes the content of individuals’ non-public communications)? If so, please provide a description.

#### Potential harm
Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety? If so, please describe why.

#### Subpopulation identification
Does the dataset identify any subpopulations (e.g., by age, gender)? If so, please de- scribe how these subpopulations are identified and provide a description of their respective distributions within the dataset.

#### Individual identification
Is it possible to identify individuals (i.e.,one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset? If so, please describe how.

#### Sensitive information
Does the dataset contain data that might be considered sensitive in any way (e.g., data that reveals racial or ethnic origins, sexual orientations, religious beliefs, political opin- ions or union memberships, or locations; financial or health data; biometric or genetic data; forms of government identification, such as social security numbers; criminal history)? If so, please provide a description.

## Collection Process
### Data acquisition
How was the data associated with each instance acquired? Was the data directly observable (e.g., raw text, movie ratings), reported by subjects (e.g., survey responses), or indirectly inferred/derived from other data (e.g., part-of-speech tags, model-based guesses for age or language)? If data was reported by subjects or indirectly inferred/derived from other data, was the data validated/verified? If so, please describe how.

### Collection period
Over what timeframe was the data collected? Does this timeframe match the creation timeframe of the data associated with the instances (e.g., recent crawl of old news articles)? If not, please describe the timeframe in which the data associated with the instances was created. Finally, list when the dataset was first published.

### Procedure and validation
What mechanisms or procedures were used to collect the data (e.g., hardware appa- ratus or sensor, manual human curation, software program, software API)? How were these mechanisms or procedures validated?

### Resource cost
What was the resource cost of collecting the data? (e.g. what were the required computational resources, and the associated financial costs, and energy consumption - estimate the carbon footprint. See Strubell et al. for approaches in this area.)

### Sampling strategy
If the dataset is a sample from a larger set, what was the sampling strategy (e.g., deter- ministic, probabilistic with specific sampling probabilities)?

### Participants and compensation
Who was involved in the data collection process? (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)?

### Ethical review process
Were any ethical review processes conducted (e.g., by an institutional review board)? If so, please provide a description of these review processes, including the outcomes, as well as a link or other access point to any supporting documentation.

### Directness
Did you collect the data from the individuals in question directly, or obtain it via third parties or other sources (e.g., websites)?

### Notification to individuals
Were the individuals in question notified about the data collection? If so, please describe (or show with screenshots or other information) how notice was provided, and provide a link or other access point to, or otherwise reproduce, the exact language of the notification itself. Did the individuals in question consent to the collection and use of their data? If so, please describe (or show with screenshots or other information) how consent was requested and provided, and provide a link or other access point to, or otherwise reproduce, the exact language to which the individuals consented.

### Consent
If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses? If so, please provide a description, as well as a link or other access point to the mechanism (if appropriate).

### Potential impact on data subjects
Has an analysis of the potential impact of the dataset and its use on data subjects (e.g., a data protection impact analysis)been conducted? If so, please provide a description of this analysis, including the outcomes, as well as a link or other access point to any supporting documentation.

## Preprocessing, Cleaning, and Labeling
### Description
Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)? If so, please provide a description. If not, you may skip the remainder of the questions in this section.

### Access to the raw data
- Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)? If so, please provide a link or other access point to the “raw” data.
- Is the software used to preprocess/clean/label the instances available? If so, please pro- vide a link or other access point.

## Uses
### History
Has the dataset been used for any tasks already? If so, please provide a description.

### Repository
Is there a repository that links to any or all papers or systems that use the dataset? If so, please provide a link or other access point.

### Other potential uses 
What (other) tasks could the dataset be used for?

### Potential harmful uses
Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses? For example, is there anything that a future user might need to know to avoid uses that could result in unfair treatment of individuals or groups (e.g., stereotyping, quality of service issues) or other undesirable harms (e.g., financial harms, legal risks) If so, please provide a description. Is there anything a future user could do to mitigate these undesirable harms?

### Tasks for which the dataset should not be used
- Are there tasks for which the dataset should not be used? If so, please provide a description.

## Distribution
### Third party distribution
Will the dataset be distributed to third parties outside of the entity (e.g., company, in- stitution, organization) on behalf of which the dataset was created? If so, please provide a description.

### Methods
How will the dataset will be distributed (e.g., tarball on website, API, GitHub)? Does the dataset have a digital object identifier (DOI)?

### Period
When will the dataset be distributed?

### License, intellectual property, or terms of use
Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)? If so, please describe this license and/or ToU, and provide a link or other access point to, or otherwise reproduce, any relevant licensing terms or ToU, as well as any fees associated with these restrictions.

### Third-party restrictions on data access
Have any third parties imposed IP-based or other restrictions on the data associated with the instances? If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any relevant licensing terms, as well as any fees associated with these restrictions.

### Export controls or regulartory restrictions
Do any export controls or other regulatory restrictions apply to the dataset or to individual instances? If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any supporting documentation.

## Maintenance
### Who is supporting/hosting/maintaining the dataset?

### Contact information
How can the owner/curator/manager of the dataset be contacted (e.g., email address)? Is there an erratum? If so, please provide a link or other access point.

### Update: plans and schedule
Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)? If so, please describe how often, by whom, and how updates will be communi- cated to users (e.g., mailing list, GitHub)?

### Applicable limits on the retention of the data
If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances (e.g., were individuals in question told that their data would be retained for a fixed period of time and then deleted)? If so, please describe these limits and explain how they will be enforced.

### Support for older versions of the dataset
Will older versions of the dataset continue to be supported/hosted/maintained? If so, please describe how. If not, please describe how its obsolescence will be communicated to users.

### Extrenal contribution to the dataset extention and augmentation: methods and validation
If others want to extend/augment/build on/contribute to the dataset, is there a mech- anism for them to do so? If so, please provide a description. Will these contributions be validated/verified? If so, please describe how. If not, why not? Is there a process for communicating/distributing these contributions to other users? If so, please provide a description.