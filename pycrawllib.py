#Python Library for PyCrawl
#By Tom Peters
#tom@tjpeters.org

import urllib2
from urlparse import urljoin
from HTMLParser import HTMLParser

class Crawler():
    """Crawls through webpages recursively using URL Links and retrieves
    URLs which have the defined search string on their webpage

    Usage:

    CrawlObject = Crawler(baseURL, searchString, depth, verbose=False)
        #Create Crawler Object
    CrawlObject.startCrawl() #Starts web crawl, prints results if verbose=True
    CrawlObjct.getResultURLList() #Returns final list of URLs
    """

    def __init__(self, baseURL, searchString, depth, verbose=False):
        "Crawler Constructor"
	if baseURL.find("://")==-1: baseURL = "http://" + baseURL
        self.baseURL = baseURL
        self.depth = depth
        self.searchString = searchString
        self.verbose=verbose
	if verbose == True:
		print "Crawler started with the following arguments:"
		print "Base URL = " + self.baseURL
		print "Crawl Depth = ", depth
		print "Search String = " + searchString
		print "Verbosity = ", verbose
        self.URLList = [] #Here to stop errors from getResultURLList before startCrawl has been used
        
    def processURL(self, URL):
        """Private, Downloads and parses the HTML file corresponding to URL

        Returns a tuple (URLList, ContainsString)
        URLList is a list of all urls on the html page
        containsString is a boolean True if the html page contains the search string
        """
        #private
        try:
            #Open
            URLObj = urllib2.urlopen(URL)
            content = URLObj.read()
            #parse
            parser = URLLinkParser(URL, self.searchString)
            parser.feed(content)
            return self.uniqueURLs(parser.getURLList()), parser.getContainsString()
        except:
            #TODO Better error checking, perhaps replace parser with a better one
            print "Error with retrieving HTML or parsing HTML"
            return [], False

    def depthCrawl(self, URL, depth):
        """
        Private, This is a recursive function that adds URLs to self.URLList

        This function shoudl not be called directly
        Adds URLs to the object's URL list if the URL's HTML contains the
        search string. Also recursively does this to all URLs on the webpage's
        URL List.
        """
        if self.verbose== True: print URL, "Depth =",depth
        #parse and return URLs on the page and bool if contains searchString
        newURLList, containsString = self.processURL(URL)

        #Add it to the list if it contains the search string
        if self.verbose==True: print "Contains Search String =", containsString
        if containsString == True: self.URLList.append(URL)
        
        #Note that this has been checked at a certain depth
        self.checkURLs[URL] = depth

        #Return after checking for the string but before processing sub-URLs
        if depth == 0: return
        
        #Recursively check all linked URLs
        for curURL in newURLList:
            searchCheck = True
            if curURL in self.checkURLs:
                if self.checkURLs[curURL] >= depth:
                    searchCheck = False
            if searchCheck == True:
                #Recursive call if hasn't been checked at this depth yet
                self.depthCrawl(curURL, depth-1)
        return
        
    def uniqueURLs(self, URLList):
        """Uniquify a list"""
        #private
        seen = set()
        seen_add = seen.add
        return [ x for x in URLList if x not in seen and not seen_add(x)]
    
    def startCrawl(self):
        """Function to initiate the web crawl. Uses internal 'private' function
        depthCrawl. Starts the crawl based on objects defined in constructor
        """
        #public interface
        self.checkURLs = {}
        self.URLList = []
        self.depthCrawl(self.baseURL, self.depth)
        self.URLList = self.uniqueURLs(self.URLList)
        
    def getResultURLList(self):
        """Retrieves the result list from the crawling process"""
        #public
        return self.URLList
        

class URLLinkParser(HTMLParser):
    """Parses HTML content with the intention of retrieving all URLs on the page
    and determining whether the page contains a search string
    """
    def __init__(self, baseURL, searchString):
        self.baseURL = baseURL
        self.URLList = []
        self.searchString = searchString
        self.containsString = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        """Records a URL if the tag is a link"""
        if tag == 'a':
            if attrs[0][0] == 'href':
                newURL = attrs[0][1]
                if newURL.find("://") == -1:
                    #Relative URL
                    newURL = urljoin(self.baseURL, newURL)
                self.URLList.append(newURL)

    def getURLList(self):
        """Return all URLs on the web page"""
        return self.URLList
    
    def handle_data(self, data):
        """Searches for the search string on the web page"""
        if data.find(self.searchString) != -1:
            self.containsString = True

    def getContainsString(self):
        "Returns True if the page contains the string, otherwise False"
        return self.containsString
