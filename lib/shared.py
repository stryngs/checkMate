class Shared(object):

    def __init__(self):
        self.oDir = 'OUTPUTs/'
        self.iDB = self.oDir + 'results.sqlite3'

    def mapRev(self, theDict):
        """Reverse the dictionary mappings for the XMLs"""
        revDict = {}
        for k, v in theDict.items():
            newKey = v[0]
            newTuple = (k, v[1])
            revDict.update({newKey: newTuple})
        return revDict
