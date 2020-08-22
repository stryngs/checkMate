# -*- coding: utf-8 -*-
"""
Modify CKLs based on contents of finalResults
"""

import officeTasks as OT
from lxml import etree

## Grab contents of testing
with open('finalResults', 'r') as iFile:
    fResults = iFile.read().splitlines()
fDict = {}
for f in fResults:
    fDict.update({f.split(':')[1]: (f.split(':')[0], f.split(':')[2], f.split(':')[3])})

## Grab CKL names
fList = OT.gnr.fileMenu(fileType = 'ckl')

## Rip through CKLs
all_vulnTables = []
all_foundDicts = []
all_vDicts = []
for i in fList[1]:
    vulnTable = []
    foundDict = {}
    vDict = {}
    cklName = i.split('_')[0]

    tree = etree.parse(i)
    root = tree.getroot()

    ## Iterate contents
    fullRoot = [i for i in root.iter()]

    ## Grab vulns
    for i in fullRoot:
        if i.tag == 'VULN':
            vulnTable.append(i)

    ## Rip through vulnTable and notate findings we found
    for vuln in vulnTable:
        ourIter = vuln.iter()
        for iter in ourIter:
            if iter.tag == 'VULN_ATTRIBUTE':
                if iter.text == 'Vuln_Num':
                    vID = [i for i in iter.itersiblings()][0].text

                    ## Check vID against our work
                    if vID.lower() in fDict.keys():
                        if cklName == fDict.get(vID.lower())[0]:
                            foundDict.update({vID.lower(): vuln})

    ## Modify found vulns
    mark = False
    for k, v in foundDict.items():
        mark = True
        ourVuln = k
        ourIter = v.iter()
        for iter in ourIter:
            if iter.tag == 'STATUS':
                iter.text = fDict.get(k.lower())[1]
            if iter.tag == 'FINDING_DETAILS':
                iter.text = fDict.get(k.lower())[2]

    if mark is True:
        tree.write(cklName + '_NEW')
