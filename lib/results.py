class Results(object):
    """Expects an instantiated scap results obj from the Xml class"""

    def __init__(self, rTuple):

        ## Rip through results
        self.resDict = {}
        self.resBreakout = {}

        ## Naming conventions
        res = rTuple
        self.testResults = {}
        for child in res.rootList:
            if child.tag == '{http://checklists.nist.gov/xccdf/1.2}TestResult':
                testResult = list(child)

                ## Get target name
                target = None
                for test in testResult:
                    if test.tag == '{http://checklists.nist.gov/xccdf/1.2}target':
                        target = test.text.lower()

                ## Get target results
                tgtResults = {}
                for test in testResult:
                    if test.tag == '{http://checklists.nist.gov/xccdf/1.2}rule-result':

                        ## rule-id, time and score
                        rID = '_'.join(test.attrib.get('idref').split('_')[3:])
                        sTime = test.attrib.get('time')
                        score = test.find('{http://checklists.nist.gov/xccdf/1.2}result').text

                        ## Update the inner dict
                        tgtResults.update({rID: (score, sTime)})

                ## Update the outer dict
                self.testResults.update({target: tgtResults})
