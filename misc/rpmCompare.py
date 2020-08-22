# -*- coding: utf-8 -*-
"""
Compare "rpm -qa" across multiple hosts
"""

import officeTasks as OT

## fs prep
OT.gnr.sweep('results.csv')
OT.gnr.sweep('rpms.sqlite3')

## Get a list of our rpms by host
ourObj = OT.gnr.fileMenu(fileType = 'internal_rpm-qa')

## Rip and store
fList = []
for i in ourObj[1]:
    hostName = i.split('_rpm-qa')[0]

    ## Rip the file
    with open(i) as iFile:
        rpms = iFile.read().splitlines()

    ## make a hostnamed tuple
    for rpm in rpms:
        fList.append((hostName, rpm))

## lazy sql
OT.csv.csvGen('results.csv', headers = ['host', 'rpm'], rows = fList)
con = OT.csv.csv2sql('results.csv', 'rpms', 'rpms.sqlite3')
db = con.cursor()
db.execute("""
           CREATE TABLE 'template_choice' AS
           SELECT
               COUNT(*) AS 'Qty',
               rpm,
               GROUP_CONCAT(host) AS 'hosts',
               NULL AS 'stig_template',
               NULL as 'notes'
           FROM rpms
           GROUP BY rpm
           ORDER BY 1 DESC;
           """)
con.commit()
con.close()
OT.gnr.sweep('results.csv')
