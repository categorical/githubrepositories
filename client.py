
import urllib.request as urllib2
import urllib.error,urllib.parse
import simplejson as json
import base64
import os
import argparse
import sys
import logging

api='https://api.github.com'
githubusername='categorical'
githubpassword=os.getenv('githubpassword')

def basicauthentication():
    credentials='%s:%s'%(githubusername,githubpassword)
    credentials=base64.b64encode(credentials.encode('ascii'))
    header=('Authorization','Basic %s'%(credentials.decode('ascii'),))
    return header

def userrepositories():
    req=urllib2.Request(''.join([api,'/user/repos']))
    items=sendreq(req)
    items=pluck(items,repositorynormaliser())
    return items

def sendreq(req):
    req.add_header(*basicauthentication())
    logging.info('%s %s'%(req.get_method(),req.get_full_url()))
    
    try:
        res=urllib2.urlopen(req)
    except urllib.error.HTTPError as e:
        res=e
    except urllib.error.URLError as e:
        raise e
    else:
        pass

    logging.info('response status code: %s'%(res.getcode(),))
    logging.info('response Content-Type: %s'%(res.info().get('Content-Type'),))
    
    msg=res.read()
    try:
        msg=json.loads(msg)
    except json.errors.JSONDecodeError as e:
        pass
    
    return msg


def pluck(items,fields):
    items=[{k:i.get(k) for k in i if k in fields} for i in items]
    return items

def printjsonserialise(data):
    print(json.dumps(data,indent=4*' '))
    
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

   


def main(args):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-10s:%(message)s',
        datefmt='%d %b %Y %H:%M:%S (%z)')
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--delete',metavar='repositoryname')
    g.add_argument('--list',action='store_true')
    g.add_argument('--get',metavar='repositoryname')
    g.add_argument('--create',metavar='repositoryname')
    g.add_argument('--createprivate',metavar='repositoryname')
    parsed=p.parse_args(args)
    if parsed.list:printjsonserialise(userrepositories())
    elif parsed.get is not None:printjsonserialise(getrepository(parsed.get))
    elif parsed.create is not None:printjsonserialise(createrepository(parsed.create))
    elif parsed.createprivate is not None:printjsonserialise(createrepository(parsed.createprivate,True))
    elif parsed.delete is not None:printjsonserialise(deleterepository(parsed.delete))
    else: pass

if __name__=='__main__':
    main(sys.argv[1:])


