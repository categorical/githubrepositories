
import urllib.request as urllib2
import urllib.error
import simplejson as json
import base64
import logging
import os

api='https://api.github.com'
githubusername='categorical'
githubpassword=os.getenv('githubpassword')
# https://developer.github.com/changes/2020-02-14-deprecating-password-auth/
githubpat=os.path.join(os.getenv('HOME'),'.gitapitoken')

def tokenauthentication():
    with open(githubpat,'r') as f:
        for line in f:
            if line.strip():
                credentials='%s'%(line.strip(),)
                break
    header=('Authorization','token %s'%(credentials,))
    return header

def basicauthentication():
    credentials='%s:%s'%(githubusername,githubpassword)
    credentials=base64.b64encode(credentials.encode('ascii'))
    header=('Authorization','Basic %s'%(credentials.decode('ascii'),))
    return header

def sendreq(req):
    #req.add_header(*basicauthentication())
    req.add_header(*tokenauthentication())
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
    

