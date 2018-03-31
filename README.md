## Spousal Age Gap

Using the Indian electoral roll data, we estimate gap between the ages of husband and wife, and how the age difference varies across states, and by the age of husband and wife. 

On average, the husbands are XX years older than their wives. The difference is highly variable and systematically varies across states and by age of the husband and wife. The age gap is larger for older husbands.

### Research Design

We exploit the fact that for married women, electoral rolls have the husband's name. The basic analysis is as follows: within each household, we find all married couples (where both the spouses are alive). For each married couple, we calculate the difference between their average. Our final dataset has the following fields: `husband_age, wife_age, household_id, state, electoral_roll_year`. We next normalize ages so that all ages are using current year as 2017. Next, we do a density plot of the differences, and present mean, median, and standard deviation. Next, we check whether the difference is statistically significant from 0. Next, we present boxplots by states. And lastly, we plot difference as a function of age of husband and wife. 

### Data and Scripts

The parsed electoral rolls can be found [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MUEGDT). The [jupyter notebook](spousal_age_gap.py) has the analysis. 

### Authors

Gaurav Sood and Atul Dhingra

