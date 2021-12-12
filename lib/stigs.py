class Stig(object):
    """Get pertinent information from a stig"""

    def __init__(self, stigObj):

        self.stigTitle = stigObj.root.find('{http://checklists.nist.gov/xccdf/1.1}title').text
        theGroups = stigObj.root.findall('{http://checklists.nist.gov/xccdf/1.1}Group')

        ## None if nothing pops
        ruleName = None
        vId = None
        ruleId = None
        ruleSeverity = None
        ruleWeight = None
        ruleVersion = None
        ruleTitle = None
        ruleDiscussion = None
        ruleFix = None
        ruleCheck = None

        ## Rip through groups
        self.groupDict = {}
        self.groupList = []
        for group in theGroups:

            ## Get rule name
            ruleName = group.find('{http://checklists.nist.gov/xccdf/1.1}title').text

            ## Get vid
            vId = group.attrib.get('id')

            ## Grab rule info and break it out
            ruleInfos = group.find('{http://checklists.nist.gov/xccdf/1.1}Rule')

            ## Get rule information
            ruleId = ruleInfos.attrib.get('id')
            ruleSeverity = ruleInfos.attrib.get('severity')
            ruleWeight = ruleInfos.attrib.get('weight')
            ruleVersion = ruleInfos.find('{http://checklists.nist.gov/xccdf/1.1}version').text
            ruleTitle = ruleInfos.find('{http://checklists.nist.gov/xccdf/1.1}title').text
            ruleFix = ruleInfos.find('{http://checklists.nist.gov/xccdf/1.1}fixtext').text
            rC = ruleInfos.find('{http://checklists.nist.gov/xccdf/1.1}check')
            ruleCheck = rC.find('{http://checklists.nist.gov/xccdf/1.1}check-content').text

            ## patch ruleDiscussion to deal with unwanted/unseen chars in STIG Viewer
            ruleDiscussion = ruleInfos.find('{http://checklists.nist.gov/xccdf/1.1}description').text.split('<VulnDiscussion>')[1].split('</VulnDiscussion>')[0]

            ## Create the tuple and update
            theTuple = (ruleId,
                        self.stigTitle,
                        ruleName,
                        vId,
                        ruleSeverity,
                        ruleWeight,
                        ruleVersion,
                        ruleTitle,
                        ruleDiscussion,
                        ruleFix,
                        ruleCheck)
            self.groupDict.update({theTuple[0]: theTuple[1:]})
            self.groupList.append(theTuple)
