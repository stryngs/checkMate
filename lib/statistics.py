import officeTasks as OT

class Stats(object):
    """
    results.sqlite3 should be intermediary to another DB which is more permanent


    Interesting query stat
    SELECT COUNT(DISTINCT(hostname)), COUNT(stig_title), GROUP_CONCAT(DISTINCT(hostname)) AS hosts, stig_title FROM haves GROUP BY stig_title;
    ^^^ Of the missing numbers added, now get totaled

    Flip below to final and we're done.


    SELECT stig_title, COUNT(*) AS 'quantity', rule_severity, 'total count' AS 'status' FROM final GROUP BY stig_title, rule_severity ORDER BY 1, 2 ASC;

    -- All
    DROP TABLE IF EXISTS totals;
    DROP TABLE IF EXISTS pass;
    DROP TABLE IF EXISTS fail;
    DROP TABLE IF EXISTS nt;
    CREATE TABLE totals AS SELECT COUNT(*) AS 'quantity', rule_severity, 'total count' AS 'status' FROM final GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE pass AS SELECT COUNT(*) AS 'quantity', rule_severity, 'pass' AS 'status' FROM final WHERE status = 'pass' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE fail AS SELECT COUNT(*) AS 'quantity', rule_severity, 'fail' AS 'status' FROM final WHERE status = 'fail' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE nt AS SELECT COUNT(*) AS 'quantity', rule_severity, 'not tested' AS 'status' FROM final WHERE status = '' GROUP BY rule_severity ORDER BY 2 ASC;
    SELECT * FROM totals UNION ALL SELECT * FROM pass UNION ALL SELECT * FROM fail UNION ALL SELECT * FROM nt;


    -- CAT I
    DROP TABLE IF EXISTS totals;
    DROP TABLE IF EXISTS pass;
    DROP TABLE IF EXISTS fail;
    DROP TABLE IF EXISTS nt;
    CREATE TABLE totals AS SELECT COUNT(*) AS 'quantity', rule_severity, 'total count' AS 'status' FROM final WHERE rule_severity = 'high' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE pass AS SELECT COUNT(*) AS 'quantity', rule_severity, 'pass' AS 'status' FROM final WHERE status = 'pass' AND rule_severity = 'high' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE fail AS SELECT COUNT(*) AS 'quantity', rule_severity, 'fail' AS 'status' FROM final WHERE status = 'fail' AND rule_severity = 'high' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE nt AS SELECT COUNT(*) AS 'quantity', rule_severity, 'not tested' AS 'status' FROM final WHERE status = '' AND rule_severity = 'high' GROUP BY rule_severity ORDER BY 2 ASC;
    SELECT * FROM totals UNION ALL SELECT * FROM pass UNION ALL SELECT * FROM fail UNION ALL SELECT * FROM nt;


    -- CAT II
    DROP TABLE IF EXISTS totals;
    DROP TABLE IF EXISTS pass;
    DROP TABLE IF EXISTS fail;
    DROP TABLE IF EXISTS nt;
    CREATE TABLE totals AS SELECT COUNT(*) AS 'quantity', rule_severity, 'total count' AS 'status' FROM final WHERE rule_severity = 'medium' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE pass AS SELECT COUNT(*) AS 'quantity', rule_severity, 'pass' AS 'status' FROM final WHERE status = 'pass' AND rule_severity = 'medium' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE fail AS SELECT COUNT(*) AS 'quantity', rule_severity, 'fail' AS 'status' FROM final WHERE status = 'fail' AND rule_severity = 'medium' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE nt AS SELECT COUNT(*) AS 'quantity', rule_severity, 'not tested' AS 'status' FROM final WHERE status = '' AND rule_severity = 'medium' GROUP BY rule_severity ORDER BY 2 ASC;
    SELECT * FROM totals UNION ALL SELECT * FROM pass UNION ALL SELECT * FROM fail UNION ALL SELECT * FROM nt;


    -- CAT III
    DROP TABLE IF EXISTS totals;
    DROP TABLE IF EXISTS pass;
    DROP TABLE IF EXISTS fail;
    DROP TABLE IF EXISTS nt;
    CREATE TABLE totals AS SELECT COUNT(*) AS 'quantity', rule_severity, 'total count' AS 'status' FROM final WHERE rule_severity = 'low' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE pass AS SELECT COUNT(*) AS 'quantity', rule_severity, 'pass' AS 'status' FROM final WHERE status = 'pass' AND rule_severity = 'low' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE fail AS SELECT COUNT(*) AS 'quantity', rule_severity, 'fail' AS 'status' FROM final WHERE status = 'fail' AND rule_severity = 'low' GROUP BY rule_severity ORDER BY 2 ASC;
    CREATE TABLE nt AS SELECT COUNT(*) AS 'quantity', rule_severity, 'not tested' AS 'status' FROM final WHERE status = '' AND rule_severity = 'low' GROUP BY rule_severity ORDER BY 2 ASC;
    SELECT * FROM totals UNION ALL SELECT * FROM pass UNION ALL SELECT * FROM fail UNION ALL SELECT * FROM nt;
    """

    def __init__(self, sh):
        self.sh = sh


    def closeout(self, con, db):
        """queries ran prior to the end"""
        print('[+] Creating stig_summary')
        db.execute("""
                   CREATE TABLE stig_summary AS
                   SELECT COUNT(*) AS `qty`, stig_title FROM stigs GROUP BY stig_title
                   UNION
                   SELECT COUNT(*), 'TOTAL' AS `stig_title` FROM stigs ORDER BY 1 DESC;
                   """)
        con.commit()
        print('[+] Drafting theorem')
        db.execute("""
                    CREATE TABLE theorem AS
                    SELECT
                    	COUNT(DISTINCT(hostname)) AS `qty of hosts`,
                    	'--' AS `qty of stig`,
                    	COUNT(stig_title) AS `qty of scap`,
                        GROUP_CONCAT(DISTINCT(hostname)) AS hosts,
                    	stig_title,
                    	'scap content' AS `thoughts`
                    FROM
                    	haves
                    GROUP BY
                    	stig_title
                    UNION

                    SELECT
                    	'--', qty, '--', '--', stig_title, 'rules per stig' FROM stig_summary WHERE stig_title != 'TOTAL'
                    UNION

                    SELECT '--', count(*), '--', '--', stig_title, 'rules not tested' FROM final WHERE status = ''  OR status IS NULL GROUP BY stig_title
                    ORDER BY 5, 6 ASC;
                    """)
        con.commit()


    def start(self, con, db):
        print('[+] Generating the table of tested STIG content')
        db.execute("""
                   CREATE TABLE haves AS SELECT S.*, R.hostname, R.status, R.time FROM stigs S INNER JOIN results R ON S.stig_title = R.stig_title AND S.rule_id = R.rule_id;
                   """)
        con.commit()
        print('[+] Fetching hosts and associated STIGs')
        q = db.execute("""
                       SELECT GROUP_CONCAT(DISTINCT(hostname)) AS hosts, stig_title FROM haves GROUP BY stig_title;
                       """)
        r = q.fetchall()

        ### This is our bottleneck for large iterations.
        print ('[+] Creating UNION of SCAP and Manuals')
        rList = []
        for row in r:
            hosts = row[0]
            title = row[1]
            hostList = hosts.split(',')
            hList = []
            hCount = 1
            for host in hostList:
                print('[~] {0} - {1} - {2}/{3}'.format(host, title, hCount, len(hostList)))
                q = db.execute("""
                               SELECT *, '{0}' AS `hostname`, NULL AS `status`, NULL AS `time` FROM stigs S WHERE stig_title = '{1}' AND rule_id NOT IN
                                   (
                                   SELECT rule_id FROM haves WHERE hostname = '{0}' and stig_title = '{1}'
                                   )
                               UNION SELECT * FROM haves WHERE stig_title = '{1}' AND hostname = '{0}';
                               """.format(host, title))
                rList.append(q.fetchall())
                hCount += 1
        con.close()

        ## Generate a SQL table for statistics
        print('[+] Generating final table')
        needs = []
        for r in rList:
            for row in r:
                ourTuple = row
                needs.append(ourTuple)
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
                   'rule_check',
                   'hostname',
                   'status',
                   'time']
        OT.csv.csvGen('CSVs/tmp3.csv', headers = headers, rows = needs, encoding = 'UTF-8')
        con = OT.csv.csv2sql('CSVs/tmp3.csv', tbName = 'final', dbName = self.sh.iDB, encoding = 'UTF-8')
        return con
