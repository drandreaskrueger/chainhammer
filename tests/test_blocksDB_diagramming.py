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

import matplotlib.pyplot as plt

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


def example_experiment():
    df = get_as_dataframe()
    # print (df)
    FROM_BLOCK, TO_BLOCK = 26, 82
    
    return df, FROM_BLOCK, TO_BLOCK


def test_experiment_slice():
    df, FROM_BLOCK, TO_BLOCK = example_experiment()
    dfs, index_from, index_to = DBdiagram.experiment_slice(df, FROM_BLOCK, TO_BLOCK, emptyBlocks=10)
    assert len(dfs) == 67
    assert max(dfs["blocknumber"]) == 92
    assert index_from == 26
    assert index_to == 92


def example_experiment_slice():
    df, FROM_BLOCK, TO_BLOCK = example_experiment()
    emptyBlocks=10
    dfs, index_from, index_to = DBdiagram.experiment_slice(df, FROM_BLOCK, TO_BLOCK, emptyBlocks)
    return dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks

def test_averageTps_wholeExperiment():
    dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice()
    avg, avgTxt = DBdiagram.averageTps_wholeExperiment(dfs, FROM_BLOCK, TO_BLOCK)
    print (avg, avgTxt)
    assert 176 < avg < 177
    assert avgTxt == "176.1"
    
    
def test_averager():
    dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice()
    av, avTxt = DBdiagram.averager(dfs, 'size', emptyBlocks, fmt="%d")
    assert 51478 < av < 51479
    assert avTxt == "51479"


def test_avgLine():
    dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice()
    fig, ax = plt.subplots(1, 1)
    avg, avgTxt = 1, "1"
    DBdiagram.avgLine(ax, dfs, emptyBlocks, avg, avgTxt)


def test_axes_simplifier():
    fig, ax = plt.subplots(1, 1)
    DBdiagram.axes_simplifier(ax, logYscale=False)
    

def example_experiment_slice_plot():
    dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice()
    DBdiagram.add_columns(dfs)
    fig, ax = plt.subplots(1, 1)
    return ax, dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks


def test_tps_plotter():
    ax, dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice_plot()
    DBdiagram.tps_plotter(ax, dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks)


def test_blocktimes_plotter():
    ax, dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice_plot()
    DBdiagram.blocktimes_plotter(ax, dfs)
    

def test_blocksizes_plotter():
    ax, dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice_plot()
    DBdiagram.blocksizes_plotter(ax, dfs, emptyBlocks)       


def test_gas_plotter():
    ax, dfs, FROM_BLOCK, TO_BLOCK, emptyBlocks = example_experiment_slice_plot()
    DBdiagram.gas_plotter(ax, dfs)       


# no single test for diagrams() because tested in composite test_load_prepare_plot_save()
# no single test for savePlot() because tested in composite test_load_prepare_plot_save()


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
    
    
    