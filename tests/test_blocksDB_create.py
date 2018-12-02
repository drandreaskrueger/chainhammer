import os, sqlite3, pytest
import chainreader.blocksDB_create as DBcreate

# current path one up?
# unfortunately path if different depending on how py.test is called
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 

###############################################################
# fixtures for the temporary throwaway database
def set_DB_throwaway():
    DBcreate.DBFILE = os.path.join("tests", "testing_TEMP.db") 
    DBcreate.DB_dropTable()
    
def delete_DB_and_SQL_file():
    for fn in (DBcreate.DBFILE, DBcreate.DBFILE+".sql"):
        try:
            os.remove(fn)
        except FileNotFoundError:
            pass
        
    
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
    DBcreate.writeRowIntoFile(block_example)
    
    assert True # no return value; just check that it raised no exception

    
def test_SQLfileIntoDB():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    
    DBcreate.DB_createTable()
    DBcreate.writeRowIntoFile(block_example)
    
    conn = sqlite3.connect(DBcreate.DBFILE)
    DBcreate.SQLfileIntoDB(conn)
    conn.close()


def test_SQLfileIntoDB_duplicates_caught():
    set_DB_throwaway()
    delete_DB_and_SQL_file()
    
    DBcreate.DB_createTable()
    DBcreate.writeRowIntoFile(block_example)
    DBcreate.writeRowIntoFile(block_example)
    
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


# unready
















    
def test_CLI_params():
    DBcreate.CLI_params()
        