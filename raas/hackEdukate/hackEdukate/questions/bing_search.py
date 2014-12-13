import json
import urllib, urllib2
from nytimesarticle import articleAPI
api = articleAPI('00cc3abde644a36b3e10a27189ae1a45%3A11%3A70234304')

def run_query(search_terms):
    # Specify the base
    root_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    source = 'Web'

    # Specify how many results we wish to be returned per page.
    # Offset specifies where in the results list to start from.
    # With results_per_page = 10 and offset = 11, this would start from page 2.
    results_per_page = 10
    offset = 0

    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stored within variable query.
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    # Construct the latter part of our request's URL.
    # Sets the format of the response to JSON and sets other properties.
    search_url = "{0}q={1}&api-key=00cc3abde644a36b3e10a27189ae1a45%3A11%3A70234304".format(
        root_url,
        query)

    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''
    bing_api_key = 'kdiorLyLAkjJpJOhWxPWI55D9fan9H1bHXn6kxWxlJw'

    # Create a 'password manager' which handles authentication for us.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bing_api_key)

    # Create our results list which we'll populate.
    results = []

    try:
        # Prepare for connecting to Bing's servers.
        articles = api.search( q = query , page=1)

        # Convert the string response to a Python dictionary object.
        json_response = articles
        print ("articles")
        print(json_response)
        # Loop through each page returned, populating out results list.
        for result in json_response['response']['docs']:
            print(result)
            print(result['web_url'])
            results.append({
                'title': result['snippet'],
                'link': result['web_url'],
                'summary': ''})

    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e

    # Return the list of results to the calling function.
    return results