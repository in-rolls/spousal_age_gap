## Spousal Age Gap

Using the Indian electoral roll data, we estimate gap between the ages of husband and wife, and how the age difference varies across states, and by the age of husband and wife. 

On average, the husbands are XX years older than their wives. The difference is highly variable and systematically varies across states and by age of the husband and wife. The age gap is larger for older husbands.

* [Research Design](#)
* [Script for Finding Couples]()
* [Data](data/)
* [Analyses]()
    - [] and []
    - 
---

### Research Design

We exploit the fact that for married women, electoral rolls have the husband's name. The basic analysis is as follows: within each household, we find all married couples (where both the spouses are alive). For each married couple, we calculate the difference between their average. Our final dataset has the following fields: `husband_age, wife_age, household_id, state, electoral_roll_year`. We next normalize ages so that all ages are using current year as 2017. Next, we do a density plot of the differences, and present mean, median, and standard deviation. Next, we check whether the difference is statistically significant from 0. Next, we present boxplots by states. And lastly, we plot difference as a function of age of husband and wife. 

### Scripts

1. **Finding Couples**
    
    [gap_age.py](gap_age.py) takes path to CSV (output from pdfparser), maximum Levenshtein string distance (if 0, then only exact matching is done) and outputs a CSV with the following fields: ```household_id, wife_id, wife_name, wife_age, husband_name, husband_id, husband name, husband_age, state, electoral_roll_year``` Each couple is a separate row.

    **Functionality**

    For each state file, within each household (house_no), the script uses the household_no as key to find all members in a house and then finds all cases where `husband_name == elector_name`.

    If there is more than one match, it writes `id` to the file `state_name_more_than_one_match.csv`, and writes multiple rows to the final CSV--one for each husband match. For e.g., say there is an elector named Sita whose husband name is listed as Ram. And say in the household, there are 2 electors named Ram, one with id = 1234 and another with id = 2345. In this case, the script will add 2 rows to the final output: `..., sita, 1234, ram,...` and `..., sita, 2345, ram, ...`.

    If there is no exact match, the script checks all the names in the household within the maximum Levenshtein distance specified by the user. And again the script adds as many rows as there are matches and posts ids where more than 1 match is made to `state_name_more_than_one_match.csv`. 

    If no matches are found within the maximal Levenshtein distance, the script writes the wife id to file `state_name_no_match_found.csv`

2. **Analyses**

### Data

The parsed electoral rolls can be found [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MUEGDT). 

Our final state-wise datasets with the the following fields are posted [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MUEGDT). Each state folder has 6 files---3 exact match files, `state_name_couples_exact_match_lev_0.csv`,  `state_name_more_than_one_match_lev_0.csv`, `state_name_no_match_found_lev_0.csv` and 3 files for Levenshtein distance of 1 (with lev_1 suffix).

