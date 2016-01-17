#!/usr/bin/python

# Imports modules used to handle command line interface
import sys, getopt
# Imports module used to read in URLS
import urllib2
# Imports module used to write the data out to a csv file
import csv
# Imports webscraping library
from bs4 import BeautifulSoup as bs

def main(argv) :
    """
    @brief      { Function used to build a CSV with URLs for State Education Agencies in the US }
    
    @param      argv  { Function has a single parameter which is the fully qualified filepath name where the data will be written as a .csv }
    
    @return     { No value is returned, but a file named in the parameter is used to store the data in a .csv file }
    """
    filepath = ''
    try:
        opts, args = getopt.getopt(argv, "hf:")
    except getopt.GetoptError:
        print 'seaWebsites.py -f <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'seaWebsites.py -f <outputfile>'
            sys.exit()
        elif opt in ("-f"):
            filepath = arg 
    # The list of FIPS State Codes
    fips = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    # List of full State names
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", 
		 "Colorado", "Connecticut", "District of Columbia", "Deleware",
		 "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
		 "Iowa", "Kansas", "Kentucky", "Lousianna", "Maine", "Maryland", 
		 "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
		 "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
		 "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
		 "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
		 "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
		 "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    # US Department of Education Root path  for SEA contact info
    sea = "http://www2.ed.gov/about/contacts/state/"
    # Initializes the dictionary object used to create the columns
    entry = {'State' : None, 'FIPS': None, 'URL': None}
    # Open the file name passed to the function with write permissions
    with open(filepath, 'wb') as f:
    	# Create variable used for calling DictWriter methods
        w = csv.DictWriter(f, entry)
        # Writes the Keys from the dictionary as the file headers
        w.writeheader()
        # Loop over the array elements of the FIPS codes
        for i in range(0, len(fips)):
        	# Reassign values to the dictionary variable.
	        entry = {'State': states[i], 'FIPS': fips[i].lower(), 'URL': bs(urllib2.urlopen(sea + fips[i].lower() + '.html')).find("p", {'class': 'smallindent'}).findAll('a')[0]['href']}
	        # Write the value for this state to the file
	        w.writerow(entry)


# Avoid calling function on load
if __name__ == "__main__":
	main(sys.argv[1:])
