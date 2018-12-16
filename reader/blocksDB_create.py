#!/usr/bin/env python3
"""
@summary: query all blocks of the whole chain, to get historical TPS, etc

@version: v40 (28/November/2018)
@since:   16/May/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates

@attention: MOST of code in here (all multi-threaded stuff) is actually obsolete
            as surprisingly the fastest way to read from (parity) RPC is ... 
            ... single-threaded!
@todo:      kick out all obsolete stuff, perhaps into obsolete/ folder?
"""

# some preliminary speed comparisons:
#
# 10 worker threads Queue:
# multi-threaded into DB:     1000 blocks took 6.02 seconds
# multi-threaded into file:   1000 blocks took 2.46 seconds
#                            execute & commit 1000 SQL statements into DB took 0.01 seconds
#
# single threaded into file: 1000 blocks took 2.09 seconds
#
# big surprise multi-threaded slower than single-threaded !!!
#
# multi-threaded but 1 worker into file: 1000000 blocks took 1892.22 seconds
# manyBlocks_singlethreaded into file:  1970342 blocks took 4237.88 seconds
#
# execute & commit 4392280 SQL statements into DB took 37.91 seconds


global DBFILE
DBFILE = "temp.db"

# obsolete: hard coded DB file names:
"""
DBFILE = "allblocks-quorum-raft.db"
DBFILE = "allblocks-tobalaba.db"
DBFILE = "allblocks-istanbul-gas40mio.db"
DBFILE = "allblocks-istanbul-gas20mio.db"
DBFILE = "allblocks-istanbul-gas10mio.db"
DBFILE = "allblocks-istanbul-2s-gas10mio.db"
DBFILE = "allblocks-istanbul-1s-gas10mio.db"
DBFILE = "allblocks-istanbul-2s-gas10mio_run2.db"
DBFILE = "allblocks-istanbul-1s-gas10mio_run2.db"
DBFILE = "allblocks-istanbul-1s-gas20mio_run2.db"
DBFILE = "allblocks-istanbul-crux-docker-1s-gas20mio.db"
DBFILE = "allblocks-istanbul-crux-docker-1s-gas20mio-RPC_run8.db" # 13 workers
DBFILE = "allblocks-istanbul-crux-docker-1s-gas20mio-RPC_run10.db" # 13 workers, repeated
DBFILE = "allblocks-geth-clique-2s-gas40mio-RPC_run1.db"
DBFILE = "allblocks-parity-poa-playground_run1.db"  
"""

### now instead call with a parameter, e.g.
# ./blocksDB_create.py allblocks_clientX_runY.db


################
## Dependencies:

# python standard library:
import sys, time, os
import sqlite3
from pprint import pprint
from queue import Queue
from threading import Thread

# pypi:
from web3 import Web3, HTTPProvider # pip3 install web3

# chainhammer
# extend sys.path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from hammer.config import RPCaddress
from hammer.clienttools import web3connection
from hammer.tps import timestampToSeconds

###############################################################################


def DB_createTable():
    """
    creates a table with the needed columns  
    """
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS 
                 blocks(
                     blocknumber INTEGER UNIQUE,
                     timestamp DECIMAL,
                     size INTEGER,
                     gasUsed INTEGER,
                     gasLimit INTEGER,
                     txcount INTEGER
                 )''')
    conn.commit()
    conn.close()


def DB_dropTable():
    """
    removes the table
    """
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS blocks''')
    conn.commit()
    conn.close()


def DB_writeRow_SQL(block):
    """
    takes in Ethereum block, creates sql INSERT statement 
    """
    valuesstring = "({number},{timestamp},{size},{gasUsed},{gasLimit},{txcount})"

    b = dict(block)
    b["txcount"] = len(block["transactions"])
    b["timestamp"] = timestampToSeconds( b["timestamp"], NODENAME, CONSENSUS)
    
    values = valuesstring.format(**b)
    
    return "INSERT INTO blocks VALUES " + values + ";"


def DB_writeRow(block, conn):
    """
    given an Ethereum block, directly INSERT into DB as row
    """
    
    SQL = DB_writeRow_SQL(block)

    c = conn.cursor()
    c.execute(SQL)
    conn.commit()


def writeRowSQLIntoFile(block):
    """
    write sql INSERT command as row into textfile
    (because DB concurrency slowed it down much)
    """
    SQL = DB_writeRow_SQL(block)
    with open(DBFILE + ".sql", "a") as f:
        f.write(SQL + "\n")


def SQLfileIntoDB(conn, commitEvery=100000):
    """
    read sql commands text file and execute into DB
    """
    
    before = time.clock()
    
    c = conn.cursor()
    
    numRows, duplicates = 0, 0
    with open(DBFILE + ".sql", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            try:
                c.execute(line)
            except Exception as e:
                print ("\n", type(e), e, line)
                duplicates += 1
            numRows += 1
            if numRows % commitEvery == 0:
                conn.commit()
                print (numRows, end=" "); sys.stdout.flush()
            lastline=line
    conn.commit()
    print ()
    print ("last one was: ", lastline)
    duration = time.clock() - before
    print ("\nexecute & commit %d SQL statements (where %d duplicates) into DB took %.2f seconds\n" % (numRows, duplicates, duration))



def DB_query(SQL, conn):
    """
    execute any SQL query, fetchall, return result
    """
    cur = conn.cursor()
    cur.execute(SQL)
    result = cur.fetchall()
    return result
    

def DB_readTable(conn):
    """
    prints the whole table
    """
    table = DB_query("SELECT * FROM blocks ORDER BY blocknumber", conn)
    pprint (table)
    return table


def DB_tableSize(conn):
    """
    prints number of rows
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM blocks")
    count = cur.fetchone()[0]
    print ("TABLE blocks has %d rows" % count)
    return count
    

def DB_blocknumberMinMax(conn):
    result = DB_query("SELECT MIN(blocknumber), MAX(blocknumber) FROM blocks", conn)
    print ("MIN(blocknumber), MAX(blocknumber) = %s " % (result) )
    return result
   
 
# TODO: obsolete?
'''
def start_web3connection(RPCaddress=None, 
                         IPCpath="TODO"): # how to enable IPC in parity ???
    """
    # get a global web3 object
    """
    global w3
    w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    
    print ("web3 connection established, blockNumber =", w3.eth.blockNumber, end=", ")
    print ("node version string = ", w3.version.node)
    
    return w3
'''

def getBlock(blockNumber):
    """
    Query web3 for block with this number
    """
    global w3
    b = w3.eth.getBlock(blockNumber)
    # pprint (dict(b))
    return b
    

def getBlock_then_store(blockNumber, conn=None, ifPrint=True, printEvery=500):
    """
    query web3 block, 
    (do NOT immediately write into DB but) 
    write INSERT statement into text file, for later processing
    """
    b = getBlock(blockNumber)
    
    # DB_writeRow(b, conn) # no,  concurrent DB writes slow it down much
    writeRowSQLIntoFile(b) # yes, simply dump into a text file first
    
    if ifPrint:
        print ("*", end="")
        if blockNumber % printEvery == 0:
            print ("\n", blockNumber, end=" ") # newline
            sys.stdout.flush()  
    
    
def multithreadedQueue(blockNumberFrom, blockNumberTo, num_worker_threads=10):
    """
    query blocks from to, via a queue of a small number of multithreading workers 
    """
    
    q = Queue()
    
    def worker():
        # connection must be thread-local:
        conn = sqlite3.connect(DBFILE, timeout=15)
        # TODO: how to close DB connection again?? Infinite loop:
        while True:
            try:
                item = q.get()
            except Exception as e:            
                print (type(e), e)
            getBlock_then_store(item, conn)
            q.task_done()

    for i in range(num_worker_threads):
         t = Thread(target=worker)
         t.daemon = True
         t.start()
    print ("%d worker threads created." % num_worker_threads)

    for i in range(blockNumberFrom, blockNumberTo):
        q.put (i)
    print ("%d items queued." % (blockNumberTo - blockNumberFrom) )
    
    print ("\n", blockNumberFrom, end=" ")

    q.join()
    print ("\nall items - done.")


def manyBlocks_multithreaded(blockNumberFrom=0, numBlocks=1000):
    """
    multithreaded block information downloader
    """
    DB_dropTable()
    DB_createTable()
    
    before = time.clock()
    multithreadedQueue(blockNumberFrom = blockNumberFrom, 
                       blockNumberTo = blockNumberFrom + numBlocks)
    duration = time.clock() - before
    print ("\n%d blocks took %.2f seconds\n" % (numBlocks, duration))


# interestingly, the above turned out to be fastest for num_worker_threads=1
# so instead of multi-threading, just go for super simple manyBlocks_singlethreaded loop:


def manyBlocks_singlethreaded(blockNumberFrom=1000001, numBlocks=3391848):
    """
    iterate through blocks, write SQL statements into text file
    """
    before = time.clock()
    print ("\n", blockNumberFrom, end=" ")
    for i in range(blockNumberFrom, blockNumberFrom+numBlocks):
        getBlock_then_store(i)
    duration = time.clock() - before
    print ("\n%d blocks took %.2f seconds\n" % (numBlocks, duration))  



def tests():
    """
    sequence of function calls used during development
    """
    DB_dropTable()
    DB_createTable()
        
    conn = sqlite3.connect(DBFILE)
    
    b=getBlock(blockNumber=2385641)
    DB_writeRow(b, conn)
    
    getBlock_then_store(blockNumber=2385642, conn=conn)
    print ()
    DB_readTable(conn)
        
    before = time.clock()
    numBlocks=1000
    blockNumberFrom=2386000
    blockNumberTo=blockNumberFrom + numBlocks 
    multithreadedQueue(blockNumberFrom=blockNumberFrom, blockNumberTo=blockNumberTo, 
                       num_worker_threads=1)
    duration = time.clock() - before
    print ("\n%d blocks took %.2f seconds\n" % (numBlocks, duration))

    before = time.clock()
    SQLfileIntoDB(conn)
    duration = time.clock() - before
    print ("\n%d SQL statements into DB took %.2f seconds\n" % (numBlocks, duration))
    
    DB_tableSize(conn)
    
    conn.close()    


def DB_newFromFile():
    """
    drop and create table, read textfile into DB 
    
    if you have many duplicates in allblocks.db.sql then this helps 
        sort allblocks.db.sql | uniq > allblocks_.db.sql; wc allblocks_.db.sql 
    """
    print ("Creating new DB", DBFILE)
    conn = sqlite3.connect(DBFILE)
    DB_dropTable()
    DB_createTable()
    SQLfileIntoDB(conn)
    DB_tableSize(conn)
    DB_blocknumberMinMax(conn)
    conn.close()


def CLI_params():
    global DBFILE
    if len(sys.argv)>2:
        print ("Please give one argument, the filename DBFILE, or zero to choose the default ", DBFILE)
    if len(sys.argv)==2:
        DBFILE=sys.argv[1]
        print ("changed DBFILE to ", DBFILE)
        

if __name__ == '__main__':
    
    global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
    w3, chainInfos = web3connection(RPCaddress=RPCaddress, account=None)
    NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

    CLI_params(); 
    print ("Writing blocks information into", DBFILE)

    # tests(); exit()
    # manyBlocks_multithreaded(); exit()
    # manyBlocks_singlethreaded(); exit()
    
    # DB_newFromFile(); exit()
    
    # N.B.: perhaps manually delete the existing "allblocks.db.sql" before 
    blockNumberFrom=0
    # blockNumberFrom=5173723
    manyBlocks_singlethreaded(blockNumberFrom=blockNumberFrom, # numBlocks=1)
                              numBlocks=w3.eth.blockNumber - blockNumberFrom + 1)
                              
    DB_newFromFile()
    print ("done.")
    
