# College Crime Map

<b>View live project here:</b>
https://dan-dewitz.github.io/college_crime_map.github.io/

Code wrangles data from raw extract from the department of education's website.
This dataset did not provide the lat and long coordinates for each school.
Therefore, each school needed to be geocoded prior to mapping.  

After geocoding, most other wrangling tasks are for structure the data
and formatting the hover text for the bubble map.

Bubble map is built using Python and Plotly.


## Main Python Programs
* preprocess.py: includeds data wrangling from raw extract to final dataset
* build_college_crime_map.py: this file build the bubble map from clean dataset and contains all of the Plotly code

## Custom Modules / tools
* custom_geocode.py: contains my geocoding function, using Google geocoder
* standardize.py: my function to standardize the crime rates
* unit_tests.py: all unit tests, mostly checking for dropped or missing rows during data wrangling
* geocode_tricky_addresses: hacking to get all schools to pass the Google geocoder

## Data
Data are made publically available through the Clearly Act
and can be downloaded from the the Department of Education's website.
They have a couple different ways of downloading data -- this is the tool I used:
https://ope.ed.gov/campussafety/#/datafile/list

* oncampuscrime141516.csv: raw data file
* final_geocoded_data.csv: clean dataset ready to map
