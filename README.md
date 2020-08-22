### What is checkMate
STIG, SCAP and ATO work can be difficult if you do not possess the monies to purchase third party toolsets.  checkMate aims to solve that issue for the public good.

### How to use the code
1. rpmCompare.py against "rpm -qa" output
    - ```<hostname>_rpm-qa << Output filename```

2. Open rpms.sqlite3
    - Notate out templates in `template_choice`
    - Ensure that for each applicable rpm, you fill in the following columns:
      - stig_template (with available choices -- misc/lib/stigs.py)
        - rhel7
        - jre8
        - db
        - apache
        - asd
        - mongo
      - notes
    - If you find an instance of a needed STIG, but cannot find it on DISA, leave the `notes` column NULL

3. Using the template CKLs needed for the engagement, run ckl2sql.py

4. Using tempDrop.py we will generate CKLs based on the mapping in rpms.sqlite3 `template_choice` table.
    - hosts.lst is required for tempDrop.py to create the given checklists

5. Remove all CKLs in misc/ directory.  Take CKLs from misc/output and place in misc/.

6. Run cklVitals.py to obtain the host information from the Base OS CKL and update the other CKLs accordingly

7. Run ckl2csv.py
    - This will overwrite the original results.sqlite3 created earlier
        - Generates results.sqlite3
            - `results`        --> All v-IDs from the given CKLs
            - `vuln_per_stig`  --> Qty of V-IDs per STIG * Qty of applicable Hosts

8. You may now import SCAP XCCDF and run cklMod.py for non-SCAP imports against
   the given checklist

9. cklMod.py uses the contents of finalResults created by the runString wrapper
    - Acts as a force multiplier for non SCAP work
    - NEEDS FINAL VERIFICATION CHECKS BEFORE PLACED INTO PRODUCTION
        - The issue is not the code for the v-IDs, but the methodology to import, will provide a patch or verification email when able.

### Things left to be done
    - The ability to push; execute; and pull back results
    - Add ability to import SCAP xccdf results
