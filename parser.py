import requests
from lxml import html
import unicodecsv




class DomParser(object):

    def __init__(self, dom, selector=None, data=None):
        self.dom = dom
        self.selector = selector
        self.data = data
        self.links = self.getLinks()

    def getLinks(self):
        linkstuff = []
        links = self.dom.cssselect('a')
        for url_stuff in links:
            text = url_stuff.text_content()
            url = url_stuff.get('href')
            linkstuff.append((text, url))
            #else:
            #    linkstuff.append((text.strip(), site + url))

        return set(linkstuff)


    def parser(self):
        """
         assumes the selector chosen pulls a single entity - or a list
         self.data --> is what we're pulling
         returns {self.data: objList}
        """

        domObj = self.dom.cssselect(self.selector)

        return domObj

    def parserText(self):
        """
         assumes the selector chosen pulls a single entity - or a list
         self.data --> is what we're pulling
         returns {self.data: objList}
        """

        domObj = self.parser()
        objList = []
        for dom_stuff in domObj:
            text = dom_stuff.text_content()
            objList.append(text)
        objList = [x.strip() for x in objList]
        if len(objList) > 1:
            return {self.data: objList}
        else:
            return {self.data: objList[0]}

    def parserTable(self, table_headers):
        """
        headers must be actual table headers
        """
        self.selector = 'tr'
        domObj = self.parser()
        data = []
        for tr in domObj:
            tds = tr.cssselect("td")
            if len(tds)==len(table_headers):
                row = []
                for td in tds:
                    row.append(td.text_content())
                    possible_url = td.cssselect('a')
                    if possible_url:
                        row.append(possible_url[0].get('href'))

                    data.append(row)
        return data
        
