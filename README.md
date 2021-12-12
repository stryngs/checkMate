# What is checkMate
STIG, SCAP and ATO work can be difficult if you do not possess the monies to purchase third party toolsets.  checkMate aims to solve that issue for the public good.

Given at least one STIG and the associated XCCDF created by SCC, map out everything needed for:
    - CKL generation without need for the manual creation thereof using the STIG Viewer
    - Seamless interaction between CKLs, XCCDFs and STIGs via SQL queries
    - Create statistics for higher level presentations
    - Break apart the code as needed for niche work

# Expected workflow
    - Create a directory called XCCDFs and place all XCCDF results in this directory
    - Create a directory called STIGs and place all tested STIGs in this directory
    - Run checkMate.py

# Expected outcome
To create a SQLite3 database consisting of the essential information for an ATO
    - The final table is the intersection of tested STIG rules -vs- not tested STIG rules
    - The haves table is the tested STIG rules
    - The results table is a breakout of the associated XCCDFs from SCC
    - The stig_summary table represents how many rules are within a given STIG
    - The stig table is a unique view of all available rules for all tested STIGs
    - The theorem table consists of spot figures to aid in crafting higher level summaries

## Miscellaneous features
These are concepts which are useful for niche scenarios when dealing with STIGs

### ckl2sql.py
Takes a directory of checklists and creates SQL

### generateRawChecklists.py
Create hostnamed and stigged themed ckls from a template
    - Useful if testing individual nodes by way of the STIG viewer
    - Deprecated if SCAP scans are ran remotely
    - Currently under revision to remove the prior requirements for generation
    - Check back soon*

### cklMod.py
Uses the contents of finalResults created by the scripts/runString wrapper, acting as a force multiplier for non SCAP testing
