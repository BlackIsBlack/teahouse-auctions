def getListContents(file):
    # Create the file name
    fileName = 'auction/choicesText/'+file+'.txt'
    # Read the contents of the file
    items = open(fileName, 'r').read()
    # Create a list of items from the file.
    itemList = items.split('\n')
    finalList = []
    # Append to the array
    for listNum in range(len(itemList)):
        finalList.append((itemList[listNum],itemList[listNum]))
    return finalList

def getURLParams(request):
    ##################### FILTER DEFINITIONS #####################
    # Get a list of oxides
    oxideList = open('auction/choicesText/oxides.txt','r').read().split('\n')
    oxideFilterList = []
    filterOxide = False

    # Get a list of packing types
    packingList = open('auction/choicesText/packing.txt','r').read().split('\n')
    packingFilterList = []
    filterPacking = False

    filterCountry = ""
    ##################### END OF FILTER DEFINITIONS #####################

    # The string that will hold the final query
    queryString = ""

    # Looping through the arguments
    for arg in request.args:
        # If the argument is contained within the list of oxidation types, it is added to the oxide filter list.
        if(arg in oxideList):
            filterOxide = True
            oxideFilterList.append(arg)

        # If the argument is contained within the list of packing types, it is added to the packing filter list.
        if(arg in packingList):
            filterPacking = True
            packingFilterList.append(arg)

        # If there is an origin input that isn't null set the origin filter.
        if(arg == 'originInput'):
            if(request.args.get('originInput') != 'null'):
                filterCountry = request.args.get('originInput')
    
    # Check that the fields have information within them, and if they do create the query.
    if(filterOxide):
        queryString += f".filter(auctionListing.oxidation.in_({oxideFilterList}))"
    if(filterCountry != ""):
        queryString += f".filter(auctionListing.origin_country=='{filterCountry}')"
    if(filterPacking):
        queryString += f".filter(auctionListing.packing.in_({packingFilterList}))"
    # Return the final query to be evaluated.
    return(queryString)

def getSortOrder(request):
    # Get the sort order field
    sortOrder = request.args.get('sortBy')

    # Depending on the selection, return a different query
    if(sortOrder == '1'):
        return "desc(auctionListing.start_time)"
    if(sortOrder == '2'):
        return "asc(auctionListing.start_time)"
    if(sortOrder == '3'):
        return "desc(auctionListing.total_bids)"
    if(sortOrder == '4'):
        return "asc(auctionListing.total_bids)"
    if(sortOrder == '5'):
        return "desc(auctionListing.current_bid"
    if(sortOrder == '6'):
        return "asc(auctionListing.current_bid"
    # If for some reason the sort order isn't one of these option, return the newst option.
    return "desc(auctionListing.start_time)"
    