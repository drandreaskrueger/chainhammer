#!/usr/bin/env python3
"""
@summary: testing blocksDB_diagramming.py

@version: v42 (4/December/2018)
@since:   3/December/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import os, sqlite3, pytest
from pprint import pprint

import reader.blocksDB_diagramming as DBdiagram

###############################################################
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
 
def get_as_dataframe():
    conn = connect_example_DB()
    df = DBdiagram.read_whole_table_into_dataframe(conn)
    conn.close()
    return df
 
###############################################################
# tests:

def test_DB_query():
    conn = connect_example_DB()
    SQL="SELECT COUNT(*) FROM blocks"
    answer = DBdiagram.DB_query(SQL, conn)
    conn.close()
    print (answer)
    assert answer[0][0] >= 0
    
    
def test_DB_tableSize():
    conn = connect_example_DB()
    answer = DBdiagram.DB_tableSize("blocks", conn)
    conn.close()
    print (answer)
    assert answer >= 0
    

def test_check_whether_complete():
    SQL="SELECT blocknumber FROM blocks ORDER BY blocknumber"
    conn = connect_example_DB()
    blocknumbers = DBdiagram.DB_query(SQL, conn)
    conn.close()
    assert DBdiagram.check_whether_complete(blocknumbers)


def test_add_colums():
    df = get_as_dataframe()
    DBdiagram.add_columns(df)
    columns = ['blocknumber', 'timestamp', 'size', 'gasUsed', 'gasLimit', 
               'txcount', 'blocktime', 'TPS_1blk', 'TPS_3blks', 'TPS_5blks', 
               'TPS_10blks', 'GUPS_1blk', 'GUPS_3blks', 'GUPS_5blks', 
               'GLPS_1blk', 'GLPS_3blks', 'GLPS_5blks']
    dfcolumns = df.columns.tolist()
    for c in columns:
        assert c in dfcolumns
        
        
def test_load_dependencies():
    DBdiagram.load_dependencies()
    assert True # no return value; just check that it raised no exception
    
    
def test_load_db_and_check_complete():
    DBFILE = os.path.join("tests", "testing_EXAMPLE-DB.db") 
    conn, blocknumbers = DBdiagram.load_db_and_check_complete(DBFILE)
    print (conn, blocknumbers)
    assert type(conn) == sqlite3.Connection
    conn.close()
    assert type(blocknumbers) == list
    assert len(blocknumbers) > 0
    
    
def test_simple_stats():
    conn = connect_example_DB()
    DBdiagram.simple_stats(conn)
    conn.close()
    assert True # no return value; just check that it raised no exception
    
    
def test_read_whole_table_into_df():
    conn = connect_example_DB()
    df = DBdiagram.read_whole_table_into_dataframe(conn)
    conn.close()
    columns=['blocknumber', 'timestamp', 'size', 'gasUsed', 'gasLimit', 'txcount']
    dfcolumns = df.columns.tolist()
    print (dfcolumns)
    for c in columns:
        assert c in dfcolumns
    
    
def test_check_timestamp_format():
    df = get_as_dataframe()
    answer = DBdiagram.check_timestamp_format(df)
    assert answer
    
    
def test_show_peak_TPS():
    df = get_as_dataframe()
    DBdiagram.add_columns(df)
    max1, max10 = DBdiagram.show_peak_TPS(df)
    assert max1>=0
    assert max10>=0
    
    
def test_load_prepare_plot_save():
    DBFILE = os.path.join("tests", "testing_EXAMPLE-DB.db")
    imgpath="tests/img"
    os.mkdir(imgpath)
    fn = DBdiagram.load_prepare_plot_save(DBFILE, "TEST", 0, 10, imgpath=imgpath)
    os.remove(fn)
    os.rmdir(imgpath)
    print ("\nremoved path %s and file %s" % (imgpath, fn))
    assert True # just check that it raised no exception
    
    
def test_CLI_params():
    try:
        DBdiagram.CLI_params()
    except SystemExit:
        pass
    
    
    
    