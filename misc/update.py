import requests

fName = 'cmUpdate.tgz'
uName = 'https://tbd/{0}'.format(fName)

def go():
    f = requests.get(uName, verify = False)
    with open(fName, 'wb') as oFile:
        oFile.write(f.content)

if __name__ == '__main__':
    go()
