# Project Scenario:

---

1. Dataset Information:
    This wildfire dataset contains data on fire activities in Australia starting from 2005. Additional information can be found here.
    The dataset includes the following variables:

2. Description:
    - Region: the 7 regions
    - Date: in UTC and provide the data for 24 hours ahead
    - Estimated_fire_area: daily sum of estimated fire area for presumed vegetation fires with a confidence > 75% for a each region in km2
    - Mean_estimated_fire_brightness: daily mean (by flagged fire pixels(=count)) of estimated fire brightness for presumed vegetation fires with a confidence level > 75% in Kelvin
    - Mean_estimated_fire_radiative_power: daily mean of estimated radiative power for presumed vegetation fires with a confidence level > 75% for a given region in megawatts
    - Mean_confidence: daily mean of confidence for presumed vegetation fires with a confidence level > 75%
    - Std_confidence: standard deviation of estimated fire radiative power in megawatts
    - Var_confidence: Variance of estimated fire radiative power in megawatts
    - Count: daily numbers of pixels for presumed vegetation fires with a confidence level of larger than 75% for a given region
    - Replaced: Indicates with an Y whether the data has been replaced with standard quality data when they are available (usually with a 2-3 month lag). Replaced data has a slightly higher quality in terms of locations

### Part 1 : Analyzing the wildfire activities in Australia
- Objective:
    The objective of this part is to analyze and visualize the wildfire activities in Australia using the provided dataset. You will explore patterns and trends, and create visualizations to gain insights into the behavior of wildfires in different regions of Australia.

---

### Part 2 : Dashboard to display charts based on selected Region and Year
#### To Do:

#### Setup
    1. Import required libraries
    2. Read the dataset

#### Layout Design
    3. Create an application layout
    4. Add a title using an HTML H1 component

#### Components
    5. Add a radio item using `dcc.RadioItems`
    6. Add a dropdown using `dcc.Dropdown`
    7. Add pie chart and bar chart core graph components

#### Final Steps
    8. Run the app