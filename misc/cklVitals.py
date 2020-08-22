# -*- coding: utf-8 -*-
"""
Take host vital information and pass it to other CKLs

Useful for when there is no SCAP content for XCCDF import.  As typically there
is always one base OS SCAP to run, we will call this our vHolder as it has the
info needed to populate non SCAPd STIGs.
"""

import officeTasks as OT
from lxml import etree

## Grab CKL names
fList = OT.gnr.fileMenu(fileType='ckl')

## Create list of vital info holder ckls
rDict = {}
vHolder = 'rhel7'
needUpdated = {}
for i in fList[1]:
    ## Grab naming
    cklName = i.split('_')[0]
    cType = i.split('_')[1].split('.')[0]

    ## Grab the base
    tree = etree.parse(i)
    root = tree.getroot()

    ## Iterate contents
    fullRoot = [i for i in root.iter()]
    if cType == vHolder:
        ## Grab node vitals
        for i in fullRoot[0:30]:
            if i.tag == 'HOST_NAME':
                hostName = i.text
            if i.tag == 'HOST_IP':
                hostIP = i.text
            if i.tag == 'HOST_MAC':
                hostMAC = i.text
            if i.tag == 'HOST_FQDN':
                hostFQDN = i.text
        rDict.update({cklName: (hostName, hostIP, hostMAC, hostFQDN)})
    else:
        needUpdated.update({i: (tree, root, fullRoot)})

## Rip through need updates
for k, v in needUpdated.items():
    ## Grab parent info
    hInfos = rDict.get(k.split('_')[0])

    ## Update node vitals
    for i in v[2][0:30]:
        if i.tag == 'HOST_NAME':
            i.text = hInfos[0]
        if i.tag == 'HOST_IP':
            i.text = hInfos[1]
        if i.tag == 'HOST_MAC':
            i.text = hInfos[2]
        if i.tag == 'HOST_FQDN':
            i.text = hInfos[3]
    v[0].write(k)
