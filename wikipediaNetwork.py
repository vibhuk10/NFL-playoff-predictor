'''
This notebook creates an adjacency matrix from a root Wikipedia page. 

It returns the adjacency matrix and a list of the URLs in the adjacency matrix. 
 
Created by Tim Chartier, July 2020. 

'''

def scrapeWikiLinks(url):
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    import re
    import numpy as np
    
    html_page = urlopen(url)
    # Pull the HTML of that webpage down
    soup = BeautifulSoup(html_page,features="lxml")
    # Get all the links that start with "/wiki" so the network is contained within Wikipedia
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^/wiki/")}):
        links.append(link.get('href'))

    # For testing: Here is how to find the length of the list
    # print('The original list has ',len(links),' links.')
    
    # Now clean the list of links
    # What tags do we want to remove? 
    tagsToRemove =['jpg','png','Template:','Category:','Wikipedia:','Special:','Template_talk:','Portal:','Help:','Talk:']
    cleanLinks = np.copy(links)
    for i in range(len(tagsToRemove)):
        linksToRemove = list(filter(lambda x: tagsToRemove[i] in x, cleanLinks)) 
        cleanLinks = list(set(cleanLinks) - set(linksToRemove))
    # For testing
    # print('The filtered list has ',len(cleanLinks),' links.')
    return cleanLinks
    
def wikipediaNetwork(rootURL='https://en.wikipedia.org/wiki/Davidson_College',sizeOfNetwork=50,baseURL = 'https://en.wikipedia.org'):

    # import needed libraries
    import numpy as np

    wikiLinks = scrapeWikiLinks(rootURL)
    if (len(wikiLinks) > sizeOfNetwork):
        wikiLinks = wikiLinks[:sizeOfNetwork]

    # Search page by page until you get the upper limit and then add only the existing pages
    # Create the adjacency matrix as you go. 

    G = np.zeros([sizeOfNetwork,sizeOfNetwork]) # create a matrix of zeros
    # Build the list first 
    i = 0
    while (i < len(wikiLinks)):
        currentURL = baseURL + wikiLinks[i]
        currentWikiLinks = scrapeWikiLinks(currentURL)  
        if len(wikiLinks) == sizeOfNetwork:   # there are no more links to add so remove new links
            currentWikiLinks = list(set(currentWikiLinks).intersection(wikiLinks))
        for j in range(len(currentWikiLinks)):
            if currentWikiLinks[j] not in wikiLinks and len(wikiLinks) < sizeOfNetwork:
                wikiLinks.append(currentWikiLinks[j])
            if currentWikiLinks[j] in wikiLinks:
                currentIndex = wikiLinks.index(currentWikiLinks[j]) 
                G[i,currentIndex] = 1
        i += 1    

    return G,wikiLinks