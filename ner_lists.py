import csv
with open('data/country.csv') as csvfile:
    data = csv.reader(csvfile)
    country_names = ['Europe', 'North America', 'South America', 'Antarctica', 'Asia']
    for row in data:
        country_names.extend(row)
with open('data/nationalities.csv') as csvfile:
    data = csv.reader(csvfile)
    nationalities = ['Asian', 'European', 'North American', 'South American']
    for row in data:
        nationalities.extend(row)

all_location_names = nationalities + country_names