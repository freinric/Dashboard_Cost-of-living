# Global Cost of Living
Kaggle data scraped: https://www.kaggle.com/datasets/mvieira101/global-cost-of-living?select=cost-of-living_v2.csv

Original dashboard: https://www.numbeo.com/cost-of-living/
( need to give appropriate credit; didn’t check for the other ones ) 

### Columns:
city/country, cost of 50 items

### Pros:
- Data updated dec 2022 it looks like (2nd version)
- Lots of data points
- Could drop down by country and by city
- Sliding scale of price point, controls which city is included in plot?

### Cons:
- Crowd sourced?
- Currency probably not CAD

Idea:
- Limit data to only canadian info to make easier / cleaner
- Audience: people who want to decide where to live based off of cost of living of different things
- Plot by province (extra work to sort cities by province, could find way to scrape automate it (probably can find city wikipedia page then scrape province))
- Interactive visualizations: slider of range of cost for specific item, only includes cities that meet criteria
- Drop down by province if manage
- Could plot cost of item vs item (scatter plot) by city, see if trendlines
- Either include all columns or choose which ones to make cleaner experience
- Interactive choose which cities to compare
- provincial averages top down aggregation
