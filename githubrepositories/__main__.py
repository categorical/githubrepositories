import sys
import argparse
import logging
import repositories as r
from client import printjsonserialise

def main(args):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-10s:%(message)s',
        datefmt='%d %b %Y %H:%M:%S (%z)')
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--delete',metavar='REPOSITORY_NAME')
    g.add_argument('--list',action='store_true')
    g.add_argument('--get',metavar='REPOSITORY_NAME')
    g.add_argument('--create',metavar='REPOSITORY_NAME')
    g.add_argument('--createprivate',metavar='REPOSITORY_NAME')
    g.add_argument('--setprivate',metavar='REPOSITORY_NAME')
    g.add_argument('--unsetprivate',metavar='REPOSITORY_NAME')
    parsed=p.parse_args(args)
    if parsed.list:printjsonserialise(r.userrepositories())
    elif parsed.get is not None:printjsonserialise(r.getrepository(parsed.get))
    elif parsed.create is not None:printjsonserialise(r.createrepository(parsed.create))
    elif parsed.createprivate is not None:
        printjsonserialise(r.createrepository(parsed.createprivate,True))
    elif parsed.delete is not None:printjsonserialise(r.deleterepository(parsed.delete))
    elif parsed.setprivate is not None:printjsonserialise(r.setprivate(parsed.setprivate))
    elif parsed.unsetprivate is not None:
        printjsonserialise(r.setprivate(parsed.unsetprivate,True))
    else: pass

if __name__=='__main__':
    main(sys.argv[1:])


