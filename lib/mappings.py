import officeTasks as OT
from lib.xmls import Xml

class Map(object):
    """Create the mappings between checklists, stigs and xccdfs"""

    def __init__(self, sh):
        ## Dir it out
        x, checklistDir = OT.gnr.fileMenu(fileType = 'ckl', mDir = 'CHECKLISTs')
        x, stigDir = OT.gnr.fileMenu(fileType = 'xml', mDir = 'STIGs')
        x, xccdfDir = OT.gnr.fileMenu(fileType = 'xml', mDir = 'XCCDFs')

        ## Create mappings (title 2 file)
        self.checklistTitle2File = {}
        self.stigTitle2File = {}
        self.mergeDict = {}

        ## File to title is all we can use here since multiple same STIGs   
        self.xccdfFile2Title = {}

        ## Notate checklists
        for checklist in checklistDir:
            ourXml = Xml()
            ourXml.rootGrabber('CHECKLISTs/{0}'.format(checklist))

            ## Get title of checklist
            siTags = None
            for child in ourXml.rootList:
                if child.tag == 'STIGS':
                    siTags = child
            siList = None
            if siTags is not None:
                siList = siTags.find('iSTIG').find('STIG_INFO')
            theTitle = None
            if siList is not None:
                for si in siList:
                    if si.find('SID_NAME').text == 'title':
                        theTitle = si.find('SID_DATA').text
            try:
                self.checklistTitle2File.update({theTitle: (checklist, ourXml)})
            except Exception as E:
                print(E)

        ## Notate stigs
        for stig in stigDir:
            ourXml = Xml()
            ourXml.rootGrabber('STIGs/{0}'.format(stig))

            ## Get title of stig
            theTitle = None
            for root in ourXml.rootList:
                if root.tag == '{http://checklists.nist.gov/xccdf/1.1}title':
                    theTitle = root.text
            try:
                self.stigTitle2File.update({theTitle: (stig, ourXml)})
            except Exception as E:
                print(E)

        ## Notate XCCDFs
        for xccdf in xccdfDir:
            ourXml = Xml()
            ourXml.rootGrabber('XCCDFs/{0}'.format(xccdf))

            ## Get title of xccdf
            theTitle = None
            for root in ourXml.rootList:
                if root.tag == '{http://checklists.nist.gov/xccdf/1.2}title':
                    theTitle = root.text

            ## Overwrite tracing abilities --> who won the dict update race
            try:
                self.xccdfFile2Title.update({xccdf: (theTitle, ourXml)})
            except Exception as E:
                print(E)

        ## Reverse the mappings
        self.checklistFile2Title = sh.mapRev(self.checklistTitle2File)
        self.stigFile2Title = sh.mapRev(self.stigTitle2File)
