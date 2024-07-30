## The Older Half: Spousal Age Gap in India

Using the Indian electoral roll data, we estimate the age difference between the spouses. We also estimate how the age difference varies across states and by the age of the husband and the wife. In particular, we use data from nearly 70M couples from 31 states and union territories: Andaman and Nicobar Islands, Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chandigarh, Dadra, Daman, Delhi, Goa, Gujarat, Haryana, Himachal Pradesh, Jammu and Kashmir, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Puducherry, Punjab, Rajasthan, Sikkim, Tripura, Uttar Pradesh, and Uttaranchal.

The [average age gap between a (heterosexual) couple is 4.1 years (the median is three and the 25th percentile is two years)](notebooks/04_spousal_age_gap_analysis.ipynb), with husbands generally older than their wives. The gap is nearly 80% larger than in the US, where the [average gap is 2.3 (538, CPS data)](https://fivethirtyeight.com/features/whats-the-average-age-difference-in-a-couple/). Compared to the US, where the man is older 64% of the time, in India, the man is older nearly 90% of the time.

The age gap between the spouses varies across states, with a median gap of about three years in Bihar, Dadra and Nagar Haveli, Gujarat, Haryana, Jammu and Kashmir, Mizoram, Madhya Pradesh, Punjab, Rajasthan, Sikkim, and UP, and eight years in Assam. The spread also varies by husband and wife age, with the age gap being larger for older husbands.

* [Research design](#research-design)
* [Scripts for finding couples and python notebook for the analysis](#scripts)
    - [Finding Couples](#finding-couples)
    - [Analysis](#analysis)
* [Underlying data that can be downloaded](#data)

### Research Design

We exploit the fact that for married women, electoral rolls have the husband's name. Within each household, we find all married couples (where both the spouses are alive). (We try both an exact match on the name and with a Levenshtein distance of one.) For each married couple, we calculate the difference between their average. Our final dataset has the following fields: `husband_age, wife_age, household_id, state, electoral_roll_year.` Next, to account for the fact that not all electoral rolls are from the same year---they are from adjacent years---we normalize age so that it reflects what their age would be in 2017. Next, we `describe` the differences, and present mean, median, standard deviation, etc. Next, we check how often the difference is greater than 0. Next, we present boxplots by state. And lastly, we plot differences as a function of the age of husband and wife (by state). 

### Scripts

#### Finding Couples

[gapage.py](finding-couples/gapage.py) takes the path to CSV (output from pdfparser), maximum Levenshtein string distance (if 0, then only exact matching is done) and outputs a CSV with the following fields: ```household_id, wife_id, wife_name, wife_age, husband_name, husband_id, husband name, husband_age, state, electoral_roll_year``` Each couple is a separate row.

**Functionality**
For each state file, within each household (house_no), the script uses the household_no as the key for finding all members in a house and then finds all cases where `husband_name == elector_name`.

If there is more than one match, it writes `id` to the file `state_name_more_than_one_match.csv` and writes multiple rows to the final CSV--one for each husband match. E.g., say there is an elector named Sita whose husband's name is listed as Ram. And say in the household, there are two electors named Ram, one with id = 1234 and another with id = 2345. In this case, the script will add two rows to the final output: `..., sita, 1234, ram,...` and `..., sita, 2345, ram, ...`.

If there is no exact match, the script checks all the names in the household within the maximum Levenshtein distance specified by the user. And again, the script adds as many rows as there are matches and posts ids where more than one match is made to `state_name_more_than_one_match.csv`.

If no matches are found within the maximal Levenshtein distance, the script writes the wife id to file `state_name_no_match_found.csv`

**Usage**

Check out the usage information or help contents of `gapage.py` by command `gapage.py --help.` Requires `python-Levenshtein` library to be installed.

```
cd finding-couples/
python gapage.py --help
usage: gapage.py [-h] [--ldcost LD_COST] [--extra-ld] [--version] [--releases]
                 [FILE]

Find gaps between the ages of husband and wife using parsed Electoral Roll
data in CSV format created by "pdfparser" tool.

positional arguments:
  FILE              a CSV file parsed by pdfparser

optional arguments:
  -h, --help        show this help message and exit
  --ldcost LD_COST  maximum Levenshtein distance cost accepted for matching
                    husband name (default is 0)
  --extra-ld        +1 Levenshtein distance if husband name length longer than
                    10
  --version         show program's version number and exit
  --releases        display release notes and exit

```

Examples:

```
# Find gaps of a state in CSV using default settings
python gapage.py /path/to/electoral_rolls/state.csv

# Specify maximum Levenshtein distance cost for name searching
python gapage.py /path/to/electoral_rolls/state.csv --ldcost 1
```

#### Analysis

* [Download Electoral Rolls](notebooks/01_download_in_rolls_age_gap.ipynb)
* [Prepare](notebooks/02_prepare_in_rolls_age_gap_v2.ipynb)
* [Upload data to Dataverse](notebooks/03_upload_age_gap_dataverse.ipynb)
* Analysis
  * [Levenshtein Distance 1. Population.](notebooks/04_spousal_age_gap_analysis-lev-1-sol1.ipynb)
  * [Levenshtein Distance 1. Stratified Random Sample (to enable plotly graphs).](https://nbviewer.jupyter.org/github/soodoku/spousal_age_gap/blob/master/notebooks/04_spousal_age_gap_analysis-lev-1-sol2.ipynb)
  * [Levenshtein Distance 0 or exact match. Population.](notebooks/04_spousal_age_gap_analysis-sol1.ipynb)
  * [Levenshtein Distance 0 or exact match. Stratified Random Sample (to enable plotly graphs).](https://nbviewer.jupyter.org/github/soodoku/spousal_age_gap/blob/master/notebooks/04_spousal_age_gap_analysis-sol2.ipynb)

### Data

The parsed electoral rolls can be found [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MUEGDT). 

Our final state-wise datasets with the following fields are posted [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GFSVY8). Each state folder has six files---3 exact match files, `state_name_couples_exact_match_lev_0.csv`,  `state_name_more_than_one_match_lev_0.csv`, `state_name_no_match_found_lev_0.csv`, and three files for Levenshtein distance of 1 (with lev_1 suffix).

### Authors

Suriyan Laohaprapanon and Gaurav Sood
