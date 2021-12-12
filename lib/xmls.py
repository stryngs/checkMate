from lxml import etree

class Xml(object):
    """Work with XML"""

    def rootGrabber(self, xml):
        """Return root and tree for a given XML
        Optionally return blah if list"""

        ## Grab the base
        self.tree = etree.parse(xml)
        self.root = self.tree.getroot()

        ## Iterate contents
        self.iterList = [i for i in self.root.iter()]
        self.iterSet = set(self.iterList)

        ## List out root
        self.rootList = list(self.root)
