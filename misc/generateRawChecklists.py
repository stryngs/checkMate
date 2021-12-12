# -*- coding: utf-8 -*-
"""
Create hostnamed and stigged themed ckls from a template
"""

import officeTasks as OT
import sqlite3 as lite
from lib.stigs import Stig
from lxml import etree

## fsPrep
OT.gnr.sweep('output', mkdir = True)

## Grab template
sg = Stig()

## Grab DBs
resCon = lite.connect('results.sqlite3')
rpmCon = lite.connect('rpms.sqlite3')
resDB = resCon.cursor()
rpmDB = rpmCon.cursor()

## Get list of template ckls
fMenu = OT.gnr.fileMenu(fileType = 'ckl')

## Get list of hosts
with open('hosts.lst') as iFile:
    hostList = iFile.read().splitlines()

## Results query
q = resDB.execute("""
                  SELECT * FROM vuln_per_stig;
                  """)
resROWS = q.fetchall()

## Deal with char lims for windows
shorthandCost = {}
for row in resROWS:
    shorthandCost.update({row[1].split(' :: ')[0]: row[0]})

## Grab our STIGs -- Right now based only on RPMs...
q = rpmDB.execute("""
                  SELECT stig_template, Qty
                  FROM template_choice
                  WHERE stig_template IS NOT NULL;
                  """)
rpmROWS = q.fetchall()
rpmDict = {}
for rpm in rpmROWS:
    rpmDict.update({rpm[0]: rpm[1]})

## Grab numbers for CKL creation
q = rpmDB.execute("""
                  SELECT hosts, stig_template FROM template_choice WHERE rpm IN(
                  SELECT DISTINCT(rpm) FROM rpms R WHERE rpm IN (
                  SELECT rpm FROM template_choice WHERE stig_template IS NOT NULL AND notes IS NOT NULL
                  ));
                  """)
rows = q.fetchall()

vX = []
for k, v in sg.templateDict.items():
    vX.append((v, k))

mList = []

## Rip through and generate CKLs
print ('Generating CKLs in generatedCKLs/')
for k, v in sg.templateDict.items():
    ourKey = v

    for row in rows:
        sType = row[1]
        ourHosts = row[0].split(',')
        for host in ourHosts:
            for v in vX:
                if sType in v[0]:
                    ourLong = v[1]
#                    print('-'.join(host.split('-')[1:5]) + '-' + ourLong) ## Observer hostname and checklist corelations
                else:
                    ourLong = None

                if ourLong is not None:
                    tree = etree.parse(ourLong + '.ckl')
                    root = tree.getroot()

                    ## Deal with httpd key fun
                    if ourLong == 'Apache Server 2.4 UNIX Server Security Technical Implementation Guide':
                        suffix = '-server'
                    elif ourLong == 'Apache Server 2.4 UNIX Site Security Technical Implementation Guide':
                        suffix = '-site'
                    else:
                        suffix = ''

                    tree.write('generatedCKLs/' + host + '_' + sType + suffix + '.ckl')
print('Done!\n')

## Cleanup
rpmCon.close()
resCon.close()
