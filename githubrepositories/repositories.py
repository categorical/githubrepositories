
import urllib.request as urllib2
import simplejson as json
from client import api,sendreq,pluck,githubusername

def userrepositories():
    req=urllib2.Request(''.join([api,'/user/repos']))
    items=sendreq(req)
    items=pluck(items,repositorynormaliser())
    return items
   
def repositorynormaliser():
    return ['id','full_name','private','size','ssh_url','clone_url']

def deleterepository(name):
    req=urllib2.Request('/'.join([api,'repos',githubusername,name]),method='DELETE')
    return sendreq(req)

def getrepository(name):
    req=urllib2.Request('/'.join([api,'repos',githubusername,name]))
    items=[sendreq(req)]
    items=pluck(items,repositorynormaliser())
    return items[0]

def createrepository(name,private=False):
    msg={'name':name,'private':private}
    msg=json.dumps(msg)
    msg=msg.encode('ascii')
    req=urllib2.Request('/'.join([api,'user','repos']),data=msg)
    items=[sendreq(req)]
    items=pluck(items,repositorynormaliser())
    return items[0]

def setprivate(name,b=False):
    msg={'private':not b}
    msg=json.dumps(msg).encode('ascii')
    req=urllib2.Request(
            '/'.join([api,'repos',githubusername,name])
            ,data=msg
            ,method='PATCH')
    items=pluck([sendreq(req)],repositorynormaliser())
    return items[0]
