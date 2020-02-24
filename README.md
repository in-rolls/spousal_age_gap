## The Older Half: Spousal Age Gap in India

Using the Indian electoral roll data, we estimate gap between the ages of husband and wife, and how the age difference varies across states, and by the age of husband and wife. In particular, we use data from the following states and union territorries: Andaman and Nicobar, Andhra Pradesh, Arunachal Pradesh, Dadra and Nagar Haveli, Daman and Diu, Goa, Jammu and Kashmir, Manipur, Meghalaya, Mizoram, Nagaland, and Puducherry.

The average age gap between the couple is 5.5 years (the median is 5 and the 25th percentile is 2 years), with husbands generally older than their wives. The gap is more than double in the US, where the [average gap is 2.3 (538, CPS data)](https://fivethirtyeight.com/features/whats-the-average-age-difference-in-a-couple/). Compared to the US, where in 64% of the couples the man is older, in India, in ~90% of couples, the man is older.

The age gap between the spouses varies across states, with the median gap of about 3 years in jammu and kashmir, 4 years in Manipur, Mizoram, and Dadra and Nagar Haveli, and 6 years in Puducherry and Andaman and Nicobar Islands. The spread also varies by husband and wife age with the age gap being larger for older husbands.

* [Research design](#research-design)
* [Scripts for finding couples and python notebook for the analysis](#scripts)
    - [Finding Couples](#finding-couples)
    - [Analysis](#analysis)
* [Underlying data that can be downloaded](#data)

### Research Design

We exploit the fact that for married women, electoral rolls have the husband's name. The basic analysis is as follows: within each household, we find all married couples (where both the spouses are alive). For each married couple, we calculate the difference between their average. Our final dataset has the following fields: `husband_age, wife_age, household_id, state, electoral_roll_year`. We next normalize ages so that all ages are using current year as 2017. Next, we do a density plot of the differences, and present mean, median, and standard deviation. Next, we check whether the difference is statistically significant from 0. Next, we present boxplots by states. And lastly, we plot difference as a function of age of husband and wife. 

### Scripts

#### Finding Couples
    
    [gap_age.py](spousal_age_gap/finding-couples/gapage.py) takes path to CSV (output from pdfparser), maximum Levenshtein string distance (if 0, then only exact matching is done) and outputs a CSV with the following fields: ```household_id, wife_id, wife_name, wife_age, husband_name, husband_id, husband name, husband_age, state, electoral_roll_year``` Each couple is a separate row.

    **Functionality**

    For each state file, within each household (house_no), the script uses the household_no as key to find all members in a house and then finds all cases where `husband_name == elector_name`.

    If there is more than one match, it writes `id` to the file `state_name_more_than_one_match.csv`, and writes multiple rows to the final CSV--one for each husband match. For e.g., say there is an elector named Sita whose husband name is listed as Ram. And say in the household, there are 2 electors named Ram, one with id = 1234 and another with id = 2345. In this case, the script will add 2 rows to the final output: `..., sita, 1234, ram,...` and `..., sita, 2345, ram, ...`.

    If there is no exact match, the script checks all the names in the household within the maximum Levenshtein distance specified by the user. And again the script adds as many rows as there are matches and posts ids where more than 1 match is made to `state_name_more_than_one_match.csv`. 

    If no matches are found within the maximal Levenshtein distance, the script writes the wife id to file `state_name_no_match_found.csv`

    **Usage**

    Check out the usage information or help contents of `gapage.py` by command `gapage.py --help`. Requires `python-Levenshtein` library to be installed.

    ```
    $> cd /path/to/mining
    $> ./gapage.py --help
    usage: gapage.py [-h] [--ldcost LD_COST] [--version] [--releases] [FILE]

    Find gaps between the ages of husband and wife using parsed Electoral Roll
    data in CSV format created by "pdfparser" tool.

    positional arguments:
      FILE              a CSV file parsed by pdfparser

    optional arguments:
      -h, --help        show this help message and exit
      --ldcost LD_COST  maximum Levenshtein distance cost accepted for matching
                        husband name (default is 5)
      --version         show program's version number and exit
      --releases        display release notes and exit
    ```

    More help commands:

    ```
    # Check out current version
    $> ./gapage.py --version

    # Check out release notes of current version
    $> ./gapage.py --releases
    ```

    Examples:

    ```
    # Find gaps of a state in CSV using default settings
    $> ./gapage.py /path/to/electoral_rolls/state.csv

    # Specify maximum Levenshtein distance cost for name searching
    $> ./gapage.py /path/to/electoral_rolls/state.csv --ldcost 5
    ```

#### Analyses

* [Download Electoral Rolls](notebooks/01_download_in_rolls_age_gap.ipynb)
* [Prepare](notebooks/02_prepare_in_rolls_age_gap.ipynb)
* [Upload data to Dataverse](notebooks/03_upload_age_gap_dataverse.ipynb)
* [Analysis](notebooks/04_spousal_age_gap_analysis.ipynb)
    - To see plotly plots, check [this](https://nbviewer.jupyter.org/github/soodoku/spousal_age_gap/blob/master/notebooks/04_spousal_age_gap_analysis.ipynb)

### Data

The parsed electoral rolls can be found [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MUEGDT). 

Our final state-wise datasets with the the following fields are posted [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GFSVY8). Each state folder has 6 files---3 exact match files, `state_name_couples_exact_match_lev_0.csv`,  `state_name_more_than_one_match_lev_0.csv`, `state_name_no_match_found_lev_0.csv` and 3 files for Levenshtein distance of 1 (with lev_1 suffix).

### Authors

Suriyan Laohaprapanon and Gaurav Sood
