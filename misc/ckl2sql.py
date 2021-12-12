# -*- coding: utf-8 -*-
"""
Take CKL(s) and change them over to a SQLite3 format

Useful if CKLs are done 1:1 versus 1:many
"""

import officeTasks as OT
from collections import OrderedDict
from lxml import etree

## CSV Headers
cHeaders = ['ROLE',
            'ASSET_TYPE',
            'HOST_NAME',
            'HOST_IP',
            'HOST_MAC',
            'HOST_FQDN',
            'TECH_AREA',
            'TARGET_KEY',
            'WEB_OR_DATABASE',
            'WEB_DB_SITE',
            'WEB_DB_INSTANCE',
            'Vuln_Num',
            'Severity',
            'Group_Title',
            'Rule_ID',
            'Rule_Ver',
            'Rule_Title',
            'Vuln_Discuss',
            'IA_Controls',
            'Check_Content',
            'Fix_Text',
            'False_Positives',
            'False_Negatives',
            'Documentable',
            'Mitigations',
            'Potential_Impact',
            'Third_Party_Tools',
            'Mitigation_Control',
            'Responsibility',
            'Security_Override_Guidance',
            'Check_Content_Ref',
            'Weight',
            'Class',
            'STIGRef',
            'TargetKey',
            'STIG_UUID',
            'CCI_REF',
            'STATUS',
            'FINDING_DETAILS',
            'COMMENTS',
            'SEVERITY_OVERRIDE',
            'SEVERITY_JUSTIFICATION']

## fsPrep
OT.gnr.sweep('results.csv')
OT.gnr.sweep('results.sqlite3')

## Grab CKL names
fList = OT.gnr.fileMenu(fileType='ckl')

## Rip through CKLs
all_vulnTables = []
all_vDicts = []
for i in fList[1]:
    vulnTable = []
    vDict = OrderedDict()
    cklName = i.split('_')[0]

    ## Grab the base
    tree = etree.parse(i)
    root = tree.getroot()

    ## Iterate contents
    fullRoot = [i for i in root.iter()]

    ## Grab node vitals
    for i in fullRoot[0:30]:
        if i.tag == 'ROLE':
            vDict.update({'ROLE': i.text})
        if i.tag == 'ASSET_TYPE':
            vDict.update({'ASSET_TYPE': i.text})
        if i.tag == 'HOST_NAME':
            vDict.update({'HOST_NAME': i.text})
        if i.tag == 'HOST_IP':
            vDict.update({'HOST_IP': i.text})
        if i.tag == 'HOST_MAC':
            vDict.update({'HOST_MAC': i.text})
        if i.tag == 'HOST_FQDN':
            vDict.update({'HOST_FQDN': i.text})
        if i.tag == 'TECH_AREA':
            vDict.update({'TECH_AREA': i.text})
        if i.tag == 'TARGET_KEY':
            vDict.update({'TARGET_KEY': i.text})
        if i.tag == 'WEB_OR_DATABASE':
            vDict.update({'WEB_OR_DATABASE': i.text})
        if i.tag == 'WEB_DB_SITE':
            vDict.update({'WEB_DB_SITE': i.text})
        if i.tag == 'WEB_DB_INSTANCE':
            vDict.update({'WEB_DB_INSTANCE': i.text})

    ## Grab vulns
    for i in fullRoot:
        if i.tag == 'VULN':
            vulnTable.append(i)

    ## Rip through vulnTable
    for vuln in vulnTable:

        ## Load up stig data into dict format
        stigDict = {}
        stigData = [i for i in vuln.findall('STIG_DATA')]
        for info in stigData:
            stigDict.update({info.find('VULN_ATTRIBUTE').text: info.find('ATTRIBUTE_DATA').text})

        ## Grab artifacts
        _status = vuln.find('STATUS').text
        _findingDetails = vuln.find('FINDING_DETAILS').text
        _comments = vuln.find('COMMENTS').text
        _severity_override = vuln.find('SEVERITY_OVERRIDE').text
        _severity_justification = vuln.find('SEVERITY_JUSTIFICATION').text

        ## Add in artifacts
        stigDict.update({'STATUS': _status})
        stigDict.update({'FINDING_DETAILS': _findingDetails})
        stigDict.update({'COMMENTS': _comments})
        stigDict.update({'SEVERITY_OVERRIDE': _severity_override})
        stigDict.update({'SEVERITY_JUSTIFICATION': _severity_justification})

        ## Add node vitals
        tDict = vDict.copy()
        tDict.update(stigDict)

        all_vDicts.append(tDict)

## Create list of all stigs with node info included
stigList = []
for v in all_vDicts:
    tmpList = []
    for hdr in cHeaders:
        tmpList.append(v.get(hdr))
    stigList.append(tuple(tmpList))

## Lazy csv & sql
OT.csv.csvGen('ckl2sql_results.csv', headers = cHeaders, rows = stigList, encoding = 'utf-8')
con = OT.csv.csv2sql('ckl2sql_results.csv', 'results', 'ckl2sql_results.sqlite3')
db = con.cursor()
db.execute("""
           CREATE TABLE 'vuln_per_stig' AS
           SELECT COUNT(*) AS 'Qty', stigREF
           FROM results
           GROUP BY stigREF
           ORDER BY 1 DESC;
           """)
con.commit()
con.close()

## Cleanup
OT.gnr.sweep('ckl2sql_results.csv')
