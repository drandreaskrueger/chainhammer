#!/usr/bin/env python3
"""
@summary: testing blocksDB_create.py

@version: v42 (4/December/2018)
@since:   2/December/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import os, sqlite3, pytest

import reader.blocksDB_create as DBcreate
from .test_tps import sendMoney_andWaitForReceipt

###############################################################
# web3 connection and nodetype 

from hammer.config import RPCaddress
from hammer.clienttools import web3connection
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
# for the temporary throwaway database
# TODO: how to delete at the end of all tests?

def set_DB_throwaway():
    DBcreate.DBFILE = os.path.join("tests", "testing_TEMP.db") 
    DBcreate.DB_dropTable()
    
    
def delete_DB_and_SQL_file():
    for fn in (DBcreate.DBFILE, DBcreate.DBFILE+".sql"):
        try:
            os.remove(fn)
        except FileNotFoundError:
            pass
        
        
@pytest.fixture(scope="session", autouse=True)
def do_something(request):
    # prepare something ahead of all tests:
    pass
    # prepare something to be run after all tests:
    request.addfinalizer(delete_DB_and_SQL_file)
    
###############################################################
# tests:

def test_DB_createTable():
    set_DB_throwaway()
    DBcreate.DB_createTable() 
    
    assert True # no return value; just check that it raised no exception


def test_DB_createTable_ifAlreadyThere():
    set_DB_throwaway()
    DBcreate.DB_createTable()
    DBcreate.DB_createTable()  # the IF NOT EXISTS solves that problem
    
    assert True # no return value; just check that it raised no exception

    
def test_DB_dropTable():
    set_DB_throwaway()
    DBcreate.DB_createTable()
    DBcreate.DB_dropTable() 
    assert True # no return value; just check that it raised no exception
    
    
def test_DB_dropTable_whatIfNotThere():
    set_DB_throwaway()
    DBcreate.DB_createTable()
    DBcreate.DB_dropTable()
    DBcreate.DB_dropTable() # no problem, the IF EXISTS solves that
    
    assert True # no return value; just check that it raised no exception
    
    
# fixture: example block
block_example = {"number":1,"timestamp":2,"size":3,"gasUsed":4,"gasLimit":5,
                 "transactions":[1,2,3,4,5,6]
                }
block_example_SQL = "INSERT INTO blocks VALUES (1,2.0,3,4,5,6);"

    
def test_DB_writeRow_SQL():
    DBcreate.NODENAME, DBcreate.CONSENSUS = "?", "?"
    answer = DBcreate.DB_writeRow_SQL(block_example)
    print (answer)
    assert answer == block_example_SQL
    
    
def test_DB_writeRow():
    set_DB_throwaway()
    DBcreate.DB_createTable()
    
    conn = sqlite3.connect(DBcreate.DBFILE)
    DBcreate.DB_writeRow(block_example, conn)
    conn.close()
    
    assert True # no return value; just check that it raised no exception
    
    
def test_DB_writeRow_duplicate():
    set_DB_throwaway()
    # DBcreate.DB_dropTable() # get rid of previous test's row 
    DBcreate.DB_createTable()
    
    conn = sqlite3.connect(DBcreate.DBFILE)
    DBcreate.DB_writeRow(block_example, conn)
    # duplicate violates blocknumber UNIQUE constraint:
    with pytest.raises(sqlite3.IntegrityError):
        DBcreate.DB_writeRow(block_example, conn)
    conn.close()
    
    
def test_writeRowIntoFile():
    set_DB_throwaway()
    DBcreate.writeRowSQLIntoFile(block_example)
    
    assert True # no return value; just check that it raised no exception

    
def test_SQLfileIntoDB():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    
    DBcreate.DB_createTable()
    DBcreate.writeRowSQLIntoFile(block_example)
    
    conn = sqlite3.connect(DBcreate.DBFILE)
    DBcreate.SQLfileIntoDB(conn)
    conn.close()


def test_SQLfileIntoDB_duplicates_caught():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    
    DBcreate.DB_createTable()
    DBcreate.writeRowSQLIntoFile(block_example)
    DBcreate.writeRowSQLIntoFile(block_example)
    
    conn = sqlite3.connect(DBcreate.DBFILE)
    DBcreate.SQLfileIntoDB(conn)
    conn.close()


# fixture for simple SQL tests:

def dummyDBconnection():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    DBcreate.DB_createTable()
    conn = sqlite3.connect(DBcreate.DBFILE)
    DBcreate.DB_writeRow(block_example, conn)
    return conn


def test_DB_query():
    conn = dummyDBconnection()
    
    SQL = "SELECT * FROM blocks"
    answer = DBcreate.DB_query(SQL, conn)
    print (answer)
    assert answer == [(1, 2, 3, 4, 5, 6)]

    SQL = "SELECT COUNT(*) FROM blocks"
    answer = DBcreate.DB_query(SQL, conn)
    print (answer)
    assert answer[0][0] == 1

    conn.close()    
    
    
def test_DB_readTable():
    conn = dummyDBconnection()
    
    answer = DBcreate.DB_readTable(conn)
    print (answer)
    assert answer == [(1, 2, 3, 4, 5, 6)]

    conn.close()    
        
        
def test_DB_tableSize():
    conn = dummyDBconnection()
    
    answer = DBcreate.DB_tableSize(conn)
    print (answer)
    assert answer == 1

    conn.close()    



def test_DB_blocknumberMinMax():
    conn = dummyDBconnection()
    
    answer = DBcreate.DB_blocknumberMinMax(conn)
    print (answer)
    assert answer == [(1, 1)]
    
    block_example["number"]=2
    print (block_example)
    DBcreate.DB_writeRow(block_example, conn)
    answer = DBcreate.DB_blocknumberMinMax(conn)
    print (answer)
    assert answer == [(1, 2)]
    
    conn.close()    


def test_getBlock():
    DBcreate.w3 = w3
    blockNumber = 0
    answer = DBcreate.getBlock(blockNumber)
    print (answer)
    assert answer["number"] == blockNumber
    assert 'gasLimit' in answer
    assert 'difficulty' in answer
    

def test_getBlock_then_store():
    blockNumber = 0
    DBcreate.getBlock_then_store(blockNumber)
    assert True # no return value; just check that it raised no exception


def test_multithreadedQueue_block0():
    DBcreate.multithreadedQueue(0, 1, 10)
    assert True # no return value; just check that it raised no exception


def createBlocks():
    sendMoney_andWaitForReceipt(10)
    
    currentBlockNumber = w3.eth.blockNumber
    print ("currentBlockNumber", currentBlockNumber)
    # return either toBlock=20 or if chain shorter then =chain_tip
    toBlock = 8 if currentBlockNumber>=8 else currentBlockNumber
    print ("toBlock", toBlock)
    return toBlock
  

def test_multithreadedQueue_blocks():
    set_DB_throwaway()
    delete_DB_and_SQL_file()

    toBlock = createBlocks()
    DBcreate.multithreadedQueue(0, toBlock, 10)
    assert True # no return value; just check that it raised no exception


def test_manyBlocks_multithreaded():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    
    toBlock = createBlocks()
    DBcreate.manyBlocks_multithreaded(0, toBlock)
    assert True # no return value; just check that it raised no exception


def test_manyBlocks_singlethreaded():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    
    toBlock = createBlocks()
    DBcreate.manyBlocks_singlethreaded(0, toBlock)
    assert True # no return value; just check that it raised no exception
    

def test_DB_newFromFile():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    
    toBlock = createBlocks()
    DBcreate.manyBlocks_singlethreaded(0, toBlock)
    
    DBcreate.DB_newFromFile()
    assert True # no return value; just check that it raised no exception
    
    
def test_CLI_params():
    DBcreate.CLI_params()
    assert True # How to test this, any idea?
    
    