import os, sqlite3, pytest

import chainreader.blocksDB_diagramming as DBdiagram

###############################################################
# web3 connection 

from config import RPCaddress
from clienttools import web3connection
answer = web3connection(RPCaddress=RPCaddress)
global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID 
w3, chainInfos  = answer
NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

# current path one up?
# unfortunately path if different depending on how py.test is called
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 

###############################################################
# for the example database with 20k transactions

def connect_example_DB():
    DBFILE = os.path.join("tests", "testing_EXAMPLE-DB.db") 
    conn = sqlite3.connect(DBFILE)
    # N.B.: Remember to 'conn.close()' afterwards!
    return conn
 
###############################################################
# tests:

def test_DB_query():
    conn = connect_example_DB()
    SQL="SELECT COUNT(*) FROM blocks"
    answer = DBdiagram.DB_query(SQL, conn)
    conn.close()
    print (answer)
    assert answer[0][0] >= 0
    

     
