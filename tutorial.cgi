#!/usr/bin/env python

from sys import path as sys_path
from os.path import join as path_join
from os.path import dirname, isdir
from shutil import copytree
from os import environ, makedirs, errno
from cgi import FieldStorage
import re

sys_path.append(path_join(dirname(__file__), 'server/src'))
from session import init_session, get_session

from config import DATA_DIR

TUTORIAL_BASE = '.tutorials'
TUTORIAL_START = "000-introduction"
TUTORIAL_DATA_DIR = DATA_DIR
TUTORIAL_SKELETON = 'example-data/tutorials/'
DEFAULT_TUTORIAL_TYPE = 'news'

def mkdir_p(path):
    try:
        makedirs(path)
    except OSError, x:
        if x.errno == errno.EEXIST and isdir(path):
            pass
        else:
            raise

try:
    remote_addr = environ['REMOTE_ADDR']
except KeyError:
    remote_addr = None
try:
    cookie_data = environ['HTTP_COOKIE']
except KeyError:
    cookie_data = None

params = FieldStorage()

if 'type' in params:
    tutorial_type = unicode(params.getvalue('type'))
else:
    tutorial_type = DEFAULT_TUTORIAL_TYPE
if 'overwrite' in params:
    overwrite = unicode(params.getvalue('overwrite'))
else:
    overwrite = False
# security check; don't allow arbitrary path specs for copytree
assert re.match(r'^[a-zA-Z0-9_-]+$', tutorial_type)

init_session(remote_addr, cookie_data=cookie_data)
sid = get_session().get_sid()
reldir = path_join(TUTORIAL_BASE, '.' + sid)
userdir = path_join(TUTORIAL_DATA_DIR, reldir)
dir = path_join(userdir, tutorial_type)

if not isdir(dir) or overwrite:
    mkdir_p(userdir)    
    copytree(path_join(TUTORIAL_SKELETON, tutorial_type), dir)

start = path_join(reldir, tutorial_type, TUTORIAL_START)

print "Content-Type: text/plain"
print "Refresh: 0; url=index.xhtml#/%s" % start
print "\n"
