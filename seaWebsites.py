#!/usr/bin/python

# Imports modules used to handle command line interface
import sys, getopt
# Imports module used to read in URLS
import requests
# Imports module used to write the data out to a csv file
import csv
#imports module for regular expressions
import re
# Imports webscraping library
from bs4 import BeautifulSoup as bs

def main(argv) :
    """
    @brief      { Function used to build a CSV with URLs for State Education Agencies in the US }
    
    @param      argv  { Function has a single parameter which is the fully qualified filepath name where the data will be written as a .csv }
    
    @return     { A list of dictionary objects containing the link elements from SEA homepages }
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
    entry = {'SEABase': None, 'State' : None, 'FIPS': None, 'Link': None, 'Raw': None}
    # Create a list of sites
    sites = list()
    # Open the file name passed to the function with write permissions
    with open(filepath, 'wb') as f:
        # Create variable used for calling DictWriter methods
        w = csv.DictWriter(f, entry)
        # Writes the Keys from the dictionary as the file headers
        w.writeheader()
        # Loop over the array elements of the FIPS codes
        for i in range(0, len(fips)):
            # Store new website address
            seaAddress = bs(requests.get(sea + fips[i].lower() + '.html').text).find("p", {'class': 'smallindent'}).findAll('a')[0]['href']
            # Tries to execute the code in the next block
            try:
                # Site contains an individual SEA's homepage links
                site = bs(requests.get(seaAddress).text).findAll('a')
                # Initializes an empty list object
                stateList = []
                # Loops over the link attributes from the home page
                for j in range(0, len(site)):
                    # Tries to execute the code in the block below
                    try:
                        try:
                            # Parses the tag argument to retrieve the text element and force it into the ASCII character set
                            hrefText = site[j].get_text(' ', strip = True).encode('ascii', 'backslashreplace')
                            # Reassign values to the dictionary variable.
                            entry = {'SEABase': seaAddress, 'State': states[i], 'FIPS': fips[i], 'Link' : site[j]['href'], 'Raw' : hrefText }
                            # Append within state entries to state list variable
                            stateList.append(entry)
                            # Write the data to the file
                            w.writerow(entry)
                        except IndexError:
                            hrefText = ""    
                    # Catch KeyError exceptions    
                    except KeyError:
                        # Prints location where error occurred to the console
                        print "Key Error with value " + str(j) + " at state ID " + str(i)
                # Appends the links from the state page to the sites variable
                sites.append(stateList)
                # empties site variable
                site = None
                # empties stateList variable
                stateList = None
            # Catches connection error exceptions    
            except requests.exceptions.ConnectionError:
                # Prints where in the loop the error occurred to the console
                print "Connection error occurred at state ID " + str(i)  

    # Returns the list of websites
    return sites

# Avoid calling function on load
if __name__ == "__main__":
    main(sys.argv[1:])
