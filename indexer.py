import xml.sax
# import nltk

# xml.sax = Simple API for XML
# in SAX, we never load the full xml file into the RAM, but only pieces we need in the moment
# in DOM - document object model to load entire xml file into RAM and create hierarchical structure


# -------------------------------------------------------------------------------------- #
#                                       XML Parsing                                      #
# -------------------------------------------------------------------------------------- #

class WikiDumpXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
      self.current = ""
      self.title = ""
      self.text = ""

    # Call when an element starts
    def startElement(self, page, attrs):
        self.current = page
        if page == "page":
            print(f"--- Page ---")
    
    # Call when a character is read
    def characters(self, content):
        if self.current == "title":
            self.title += content
            # self.title is the current content we are reading
        elif self.current == "text":
            self.text += content

    # Call when an elements ends
    def endElement(self, page):
        if self.current == "title":
            print(f"title: {self.title}")
        elif self.current == "text":
            print(f"text : {self.text}")

        # if page == "page":
        #     self.current = ""
        #     self.title = ""
        #     self.text = ""


Handler = WikiDumpXMLHandler()
parser = xml.sax.make_parser()
parser.setContentHandler(Handler)
# parser for phase 1:
parser.parse("enwiki-20220720-pages-articles-multistream15.xml-p15824603p17324602")