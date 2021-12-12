import os
import sqlite3 as lite
import officeTasks as OT
from lib.results import Results
from lib.stigs import Stig
from lib.mappings import Map
from lib.checklists import Checklist
from lib.shared import Shared
from lib.statistics import Stats

if __name__ == '__main__':
    print('[*] checkMate has started')

    ### Need to import Checklist logic at some point
    # if os.path.isdir('CHECKLISTs') and os.path.isdir('XCCDFs') and os.path.isdir('STIGs'):
    ## Lazy workaround
    try:
        os.mkdir('CHECKLISTs')
    except:
        pass
    if os.path.isdir('XCCDFs') and os.path.isdir('STIGs'):

        ## Needed objects
        sh = Shared()
        st = Stats(sh)

        ## fsprep
        OT.gnr.sweep('OUTPUTs', mkdir = True)
        OT.gnr.sweep('CSVs', mkdir = True)

        ## Map out the XMLs
        print('[+] Mapping XMLs')
        mp = Map(sh)

        ## Work around SCC and how it creates the title for XCCDFs
        tempDict = {}
        for k, v in mp.xccdfFile2Title.items():                                ## Adjust v[0]
            if v[0] == 'Windows 10 Security Technical Implementation Guide':
                newV = ('Microsoft Windows 10 Security Technical Implementation Guide', v[1])
            elif v[0] == 'Windows Firewall with Advanced Security Security Technical Implementation Guide':
                newV = ('Microsoft Windows Firewall with Advanced Security Security Technical Implementation Guide', v[1])
            else:
                newV = v
            tempDict.update({k: newV})
        mp.xccdfFile2Title = tempDict.copy()

        ## Pull in all results
        print('[+] Parsing XCCDF results')
        importsFile2Title = {}
        for k, v in mp.xccdfFile2Title.items():
            xmlName = k
            xmlTitle = v[0]
            xmlRip = v[1]

            ## Rip pertinent data from the XCCDF import
            resultsofRip = Results(xmlRip)

            ## Map it
            importsFile2Title.update({xmlName: (xmlTitle, resultsofRip)})

        ## Reverse the results
        importsTitle2File = sh.mapRev(importsFile2Title)

        ## Rip by file and sieve via the stig
        print('[+] Pulling STIG info and aligning with XCCDF results')
        stigSet = set()
        for k, v in importsFile2Title.items():
            xccdfName = k
            xccdfTitle = v[0]
            xccdfResults = v[1]
            theStig = mp.stigTitle2File.get(xccdfTitle)

            ### Important
            ## This method does not account for any STIG where no SCAP exists.
            ## To obtain all STIG, iterate all keys from mp.stigTitle2File
            ### Important
            stigSet.add(theStig)

            ## Store results
            headers = ['stig_title',
                       'hostname',
                       'rule_id',
                       'status',
                       'time']
            iList = []
            for k, v in xccdfResults.testResults.items():
                hostname = k

                for rule, stats in v.items():
                    rule_id = rule
                    rule_status = stats[0]
                    rule_time = stats[1]

                    ourTuple = (xccdfTitle, hostname, rule_id, rule_status, rule_time)
                    iList.append(ourTuple)

            OT.csv.csvGen(csvName = 'CSVs/tmp2.csv', headers = headers, rows = iList, encoding = 'UTF-8')
            con = OT.csv.csv2sql(fName = 'CSVs/tmp2.csv', tbName = 'results', dbName = sh.iDB, encoding = 'UTF-8')
            con.close()

        ## Parse the stigs
        print('[!] Parsing STIGs based on tested SCAP content, not all available STIGs')
        for sti in stigSet:
            stig = Stig(sti[1])

            ## SQL the stig rip
            headers = ['rule_id',
                       'stig_title',
                       'rule_name',
                       'v_id',
                       'rule_severity',
                       'rule_weight',
                       'rule_version',
                       'rule_title',
                       'rule_discussion',
                       'rule_fix',
                       'rule_check']
            OT.csv.csvGen(csvName = 'CSVs/tmp.csv', headers = headers, rows = stig.groupList, encoding = 'UTF-8')
            con = OT.csv.csv2sql(fName = 'CSVs/tmp.csv', tbName = 'stigs', dbName = sh.iDB, encoding = 'UTF-8')
            con.close()

        ## SCAP vs Manual testing
        c = lite.connect(sh.iDB)
        d = c.cursor()
        con = st.start(c, d)
        db = con.cursor()

        ## Stats work
        st.closeout(con, db)

        ## Cleanup
        con.close()
        OT.gnr.sweep('CSVs')
        print('[*] checkMate has finished')
