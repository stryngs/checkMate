class Checklist(object):
    """
    Expects an instantiated stig checklist obj from the Xml class
    Consists of the (instantiatedObject, hostname_type string)

    Currently in beta as it still needs to grab things like <ASSET> and such

    Will replace/merge with ckl2sql.py
    """

    def __init__(self, cklObj, htStr):

        ## Rip through checklists
        self.cklDict = {}
        self.cklBreakout = {}

        ## Naming conventions
        ckl = cklObj
        fullStr = htStr
        cklName = fullStr.split('_')[0]
        cType = fullStr.split('_')[1].split('.')[0]

        rootList = list(ckl.root)
        self.vulnList = []
        for child in rootList:

            if child.tag == 'STIGS':
                stigsList = list(child)

        for stig in stigsList:
            if stig.tag == 'iSTIG':

                vList = list(stig)
                for v in vList:

                    if v.tag == 'VULN':
                        self.vulnList.append(v)

        ## Breakout stig datas referencing the rule as the key
        for vuln in self.vulnList:
            vInfo = list(vuln)

            ## Parent breakout
            vDict = {}
            for v in vInfo:
                vStatus = None
                vFindingDetails = None
                vComments = None
                vSeverityOverride = None
                vSeverityJustification = None

                ## Expand the datas


                ## Iterate through knowns -- discount unknowns
                if v.tag == 'STIG_DATA':

                    ## transport to the dict
                    breakout = list(v)
                    vAttrib = None
                    aData = None

                    for b in breakout:
                        if b.tag == 'VULN_ATTRIBUTE':
                            vAttrib = b.text
                        if b.tag == 'ATTRIBUTE_DATA':
                            aData = b.text

                    ## Quick sanity check
                    if vAttrib is not None:
                        if aData is not None:
                            vDict.update({vAttrib: aData})                         ## Overwrites LEGACY_ID by way of duplicate?

                if v.tag == 'STATUS':
                    vStatus = v.text

                if v.tag == 'FINDING_DETAILS':
                    vFindingDetails = v.text

                if v.tag == 'COMMENTS':
                    vComments = v.text

                if v.tag == 'SEVERITY_OVERRIDE':
                    vSeverityOverride = v.text

                if v.tag == 'SEVERITY_JUSTIFICATION':
                    vSeverityJustification = v.text


            ## Get rule id
            rID = vDict.get('Rule_ID')

            ## Update dict for vulns
            self.cklDict.update({rID: (vStatus,
                                       vFindingDetails,
                                       vComments,
                                       vSeverityOverride,
                                       vSeverityJustification,
                                       vDict)})

        ## Update vuln breakout
        self.cklBreakout.update({ckl: self.cklDict})
