# -*- coding: utf-8 -*-
"""
When finished, do this to stat it up:
    CREATE TABLE scap_breakdown AS SELECT  stig, scap, COUNT(*) AS 'qty' FROM stigs GROUP BY stig, scap ORDER BY 1,2 DESC,3 desc;
"""

import officeTasks as OT
from lxml import etree

dList, tgtList = OT.gnr.fileMenu('xml')
print('\n' + dList)
xccdf = tgtList[int(input('XCCDF XML to parse?\n'))]
bench = tgtList[int(input('Benchmark XML to parse?\n'))]
xTree = etree.parse(xccdf)
xRoot = xTree.getroot()
xTitle = xRoot.find('{http://checklists.nist.gov/xccdf/1.1}title').text
if bench != xccdf:
    bTree = etree.parse(bench)
    bRoot = bTree.getroot()

## Get our groups
xGroup = [i for i in xRoot.iter('{http://checklists.nist.gov/xccdf/1.1}Group')]
if bench != xccdf:
    bGroup = [i for i in bRoot.iter('{http://checklists.nist.gov/xccdf/1.2}Group')]

## Get our severities
xDict = {}
bDict = {}
for i in xGroup:
   xDict.update({i.attrib.get('id'): i.find('{http://checklists.nist.gov/xccdf/1.1}Rule').attrib.get('severity')})
if bench != xccdf:
    for i in bGroup:
        bDict.update({i.attrib.get('id').split('_')[-1]: i.find('{http://checklists.nist.gov/xccdf/1.2}Rule').attrib.get('severity')})

## Set our work
xSet = set([i.attrib.get('id') for i in xGroup])
if bench != xccdf:
    bSet = set([i.attrib.get('id').split('_')[-1] for i in bGroup])

## Show what is not SCAP
sDict = {}
nsDict = {}

if bench != xccdf:
    for i in xSet.intersection(bSet):
        sDict.update({i: xDict.get(i)})
    scap = xSet.intersection(bSet)
if bench != xccdf:
    noScap = xSet - bSet
else:
    noScap = xSet
for i in noScap:
    nsDict.update({i: xDict.get(i)})

## CSV prep
rList = []
for k, v in sDict.items():
    rList.append((xTitle, k, v, 'yes'))
for k, v in nsDict.items():
    rList.append((xTitle, k, v, 'no'))

## CSV Gen
headers = ['stig', 'v-id', 'severity', 'scap']
OT.csv.csvGen(xTitle + '.csv', headers, rList)

## SQL Gen
con = OT.csv.csv2sql(xTitle + '.csv', 'stigs', 'stigs.sqlite3')
con.close()
OT.gnr.sweep(xTitle + '.csv')
