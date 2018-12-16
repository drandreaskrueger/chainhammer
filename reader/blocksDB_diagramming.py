#!/usr/bin/env python3
"""
@summary: for the jupyter notebooks: tools, column creators, diagramming routines, etc. 

@version: v40 (29/November/2018)
@since:   26/June/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates

@TODO:    this needs usage comments; not every function has a docstring yet 
"""

#global DBFILE, NAME_PREFIX
#DBFILE = "temp.db"
#NAME_PREFIX = "TEMP"

################
## Dependencies:

# standard library
import sys, os
import sqlite3
from pprint import pprint

# pypi:
import pandas
import numpy
import matplotlib

################


def DB_query(SQL, conn):
    """
    any SQL query, with many answers 
    """
    cur = conn.cursor()
    cur.execute(SQL)
    result = cur.fetchall()
    return result


def DB_tableSize(tablename, conn):
    """
    prints number of rows
    """
    count = DB_query("SELECT COUNT(*) FROM %s" % tablename, conn)
    print ("TABLE %s has %d rows" % (tablename, count[0][0]))
    return count[0][0]


def maxBlockNumber(conn):
    """
    what is the first & last block we have?
    """
    result = DB_query("SELECT MIN(blocknumber), MAX(blocknumber) FROM blocks", conn)
    print ("MIN(blocknumber), MAX(blocknumber) = %s " % (result) )
    return result


def check_whether_complete(blocknumbers):
    """
    do we have consecutive blocks, none missing?
    """
    start = min(blocknumbers)[0]
    last = max(blocknumbers)[0]
    old = start-1
    total=0
    for bn in blocknumbers:
        bn = bn[0]
        missing=bn-old-1
        if missing>0:
            print ("from ", old+1, "to", bn - 1, "there are ", missing, " missing")
            total+=missing
        old = bn
    print()
    complete = (not total)
    print ("complete" if complete else "some %d blocks missing" % total, end=" ")
    print ("between blocks %d and %d." %(min(blocknumbers)[0], max(blocknumbers)[0]))

    return complete

##################
## add columns


def add_blocktime(df):
    """
    blocktime = timestamp[n] - timestamp[n-1]
    """
    df['blocktime'] = df['timestamp'] - df['timestamp'].shift()
    df.loc[1, "blocktime"] = numpy.nan


def add_TPS(df, numBlocks):
    """
    transactions per second
    with differently sized (rectangular) windows
    """
    name = 'TPS_%dblks'%numBlocks if numBlocks>1 else 'TPS_%dblk'%numBlocks
    df[name]=df['txcount'].rolling(numBlocks).sum() / df['blocktime'].rolling(numBlocks).sum()
    

def add_GUPS(df, numBlocks):
    """
    gasUsed per second
    """
    name = 'GUPS_%dblks'%numBlocks if numBlocks>1 else 'GUPS_%dblk'%numBlocks
    df[name]=df['gasUsed'].rolling(numBlocks).sum() / df['blocktime'].rolling(numBlocks).sum()

def add_GLPS(df, numBlocks):
    """
    gasLimit per second
    """
    name = 'GLPS_%dblks'%numBlocks if numBlocks>1 else 'GLPS_%dblk'%numBlocks
    df[name]=df['gasLimit'].rolling(numBlocks).sum() / df['blocktime'].rolling(numBlocks).sum()


##################################################
## diagramming stand-alone
## does the same as the jupyter notebook
## but more convenient for cloud server 
## ... on the command line
##
##################################################
## TODOs: 
##     * also get the simpler single diagrams ? 
##       from the original blocksDB_analyze.ipynb
##     * doc strings for the following routines:
##################################################

def load_dependencies():
    
    import sqlite3; print("sqlite3 version", sqlite3.version)
    import pandas; print("pandas version", pandas.__version__)
    import numpy; print("numpy version", numpy.__version__)
    import matplotlib; print("matplotlib version", matplotlib.__version__)
    from matplotlib import pyplot as plt
    
    # get_ipython().run_line_magic('matplotlib', 'inline')
    
    # https://github.com/matplotlib/matplotlib/issues/5907#issuecomment-179001811
    matplotlib.rcParams['agg.path.chunksize'] = 10000
    
    # my own routines are now all in separate .py file:
    # from blocksDB_diagramming import DB_query, DB_tableSize, maxBlockNumber, check_whether_complete
    # from blocksDB_diagramming import add_blocktime, add_TPS, add_GUPS, add_GLPS


def load_db_and_check_complete(DBFILE):
    print ("\nReading blocks table from", DBFILE)
    
    # open database connection
    conn = sqlite3.connect(DBFILE)
    
    print ("DB table names: ", DB_query("SELECT name FROM sqlite_master WHERE type='table';", conn)[0])
    
    # number of rows?
    _=DB_tableSize("blocks", conn)
    
    # what is the first & last block we have?
    minblock, maxblock = maxBlockNumber(conn)[0]
    
    blocknumbers = DB_query("SELECT blocknumber FROM blocks ORDER BY blocknumber", conn) 
    print ("len(blocknumbers)=", len(blocknumbers))
    
    # do we have consecutive blocks, none missing?
    check_whether_complete(blocknumbers)
    print ()

    return conn, blocknumbers


def simple_stats(conn):
    
    # simple statistics
    
    size_max = DB_query("SELECT MAX(size) FROM blocks", conn); print ("(block)size_max", size_max[0][0])
    txcount_max = DB_query("SELECT MAX(txcount) FROM blocks", conn); print ("txcount_max", txcount_max[0][0])
    txcount_av = DB_query("SELECT AVG(txcount) FROM blocks", conn); print ("txcount_av", txcount_av[0][0])
    txcount_sum = DB_query("SELECT SUM(txcount) FROM blocks", conn); print ("txcount_sum", txcount_sum[0][0])
    blocks_nonempty_count = DB_query("SELECT COUNT(blocknumber) FROM blocks WHERE txcount != 0", conn); print ("blocks_nonempty_count", blocks_nonempty_count[0][0])
    print ("av tx per nonempty blocks = ", txcount_sum[0][0] / blocks_nonempty_count[0][0] )
    print ()
    
    
def read_whole_table_into_dataframe(conn):
    
    # SQL="SELECT * FROM blocks WHERE 48500<blocknumber and blocknumber<49000 ORDER BY blocknumber"
    SQL="SELECT * FROM blocks ORDER BY blocknumber"
    df = pandas.read_sql(SQL, conn)

    return df
    

def check_timestamp_format(df):
    """
    some clients report absolute blocktime as epochtime in seconds, 
    some in nanoseconds
    that should have been handled already, in the timestampToSeconds() function
    but if it hasn't, the problem would show up here.
    """
    # print ("example- first 4 rows:")
    # print (df[0:4])
    # better come up with an automated test, not just visual inspection: 
    # print ("             is timestamp in seconds?")
    # ### `geth` based clients have a nanosecond timestamp
    # not anymore?
    # transform nanoseconds to seconds
    # df["timestamp"]=df["timestamp"]/1000000000

    problematic = []
    for ts in df["timestamp"]:
        #        year 2001         year 2255      testrpc-py issue https://github.com/pipermerriam/eth-testrpc/issues/117
        if not ((1000000000 < ts < 9000000000) or (6000000 < ts < 8000000)):   
            problematic.append(ts)
            
    if problematic:
        print ("%d problematic timestamps = probably not in unit of seconds" % len(problematic))
        try:# try, for the case that the list is short
            problematic = problematic[:3] + problematic[-3:]
            problematic = sorted(list(set(problematic))) # remove duplicates
        except:
            pass
        print ("examples:", problematic)
    
    # hello year 2255, you might have a Y2286 problem 
    # when epochtime goes from 9999999999 to 10000000000
    # someone warned you 30 years earlier. Hahaha :-)
    return not problematic


def add_columns(df):

    # blocktime = timestamp[n] - timestamp[n-1]
    add_blocktime(df)
    
    
    #df["TPS_1"]=df['txcount']/df['blocktime']
    #df
    
    
    # transactions per second
    # with differently sized (rectangular) windows
    add_TPS(df, numBlocks=1)
    add_TPS(df, numBlocks=3)
    add_TPS(df, numBlocks=5)
    add_TPS(df, numBlocks=10)
    
    
    # gasUsed and gasLimit per second
    add_GUPS(df, numBlocks=1)
    add_GUPS(df, numBlocks=3)
    add_GUPS(df, numBlocks=5)
    
    add_GLPS(df, numBlocks=1)
    add_GLPS(df, numBlocks=3)
    add_GLPS(df, numBlocks=5)

    print ("\nColumns added. Now: ", df.columns.tolist() )
    print ()
    
    
def show_peak_TPS(df):
    
    columns = ['blocknumber', 
               'TPS_1blk', 'TPS_3blks', 'TPS_5blks', 'TPS_10blks',
               'txcount', 'size', 'gasUsed', 'gasLimit', 'timestamp', 'blocktime']  

    print ("peak TPS single block:")
    df1 = df.sort_values(by=['TPS_1blk'], ascending=False)[0:10]
    max1 = max(df1['TPS_1blk'])
    pprint (df1[columns])
    
    
    print ("\npeak TPS over ten blocks:")
    df10 = df.sort_values(by=['TPS_10blks'], ascending=False)[0:10]
    max10 = max(df10['TPS_10blks'])
    pprint (df10[columns])

    print ("\nSingle block, vs averaged over 10 blocks:")
    print ("peak( TPS_1blk) = %.2f \npeak(TPS_10blk) = %.2f" % (max1,max10))
    return max1, max10
    

def diagrams(df, blockFrom, blockTo, prefix="", gas_logy=True, bt_logy=True, imgpath="img"):
    
    from matplotlib import pyplot as plt
    
    # https://github.com/matplotlib/matplotlib/issues/5907#issuecomment-179001811
    matplotlib.rcParams['agg.path.chunksize'] = 10000
        
    ###################################################
    # prepare 2x2 subplots
    # plt = matplotlib.pyplot
    fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(15,10))
    plt.tight_layout(pad=6.0, w_pad=6.0, h_pad=7.5)
    title = prefix + " blocks %d to %d" % (blockFrom, blockTo)
    plt.suptitle(title, fontsize=16)
    
    ####################################
    # TPS
    
    # TPS averages --> legend
    cols=['TPS_1blk', 'TPS_3blks', 'TPS_5blks', 'TPS_10blks']
    averages=df[cols][blockFrom:blockTo].mean()
    legend = [col + " (av %.1f)" % averages[col] for col in cols]
    # print (legend)
    
    # TPS diagram
    cols = ['blocknumber'] + cols
    ax=df[cols][blockFrom:blockTo].plot(x='blocknumber', rot=90, ax=axes[0,0])
    ax.set_title("transactions per second")
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.legend(legend);
    
    ###########################################
    # bar charts or line charts
    
    # bar charts are too expensive when too many blocks
    numBlocks =  blockTo - blockFrom
    kind = 'bar' if numBlocks<2000 else 'line'
        
    #############################################
    # BT
    ax=df[['blocknumber', 'blocktime']][blockFrom:blockTo].plot(x='blocknumber', kind=kind, ax=axes[0,1],
                                                               logy=bt_logy)
    ax.set_title("blocktime since last block")
    ax.locator_params(nbins=1, axis='x')  # TODO: matplotlib's ticks - how to autoselect few? Any idea welcome
        
    #############################################
    # blocksize
    ax=df[['blocknumber', 'size']][blockFrom:blockTo].plot(x='blocknumber', rot=90, kind=kind, ax=axes[1,0])
    # ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.set_title("blocksize in bytes")
    ax.locator_params(nbins=1, axis='x')  # TODO: matplotlib's ticks - how to autoselect few? Any idea welcome
    
    ####################################
    # gas
    ax=df[['blocknumber', 'GLPS_1blk', 'GUPS_1blk']][blockFrom:blockTo].plot(x='blocknumber', 
                                                                             rot=90, ax=axes[1,1], 
                                                                             logy=gas_logy)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    if not gas_logy:
        ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.set_title("gasUsed and gasLimit per second")
    
    ##############################################
    # save diagram to PNG file
    filename = "%s_tps-bt-bs-gas_blks%d-%d.png" % (prefix,blockFrom,blockTo)
    filepath = os.path.join(imgpath, filename)
    fig.savefig(filepath)
    
    return filepath




###############################################################################

def load_prepare_plot_save(DBFILE, NAME_PREFIX, FROM_BLOCK, TO_BLOCK, imgpath="img"):
    
    load_dependencies()
    conn, blocknumbers = load_db_and_check_complete(DBFILE)
    simple_stats(conn)
    df = read_whole_table_into_dataframe(conn)
    conn.close()
    assert check_timestamp_format(df)
    add_columns(df)
    show_peak_TPS(df)
    
    if FROM_BLOCK==-1: FROM_BLOCK = min(blocknumbers)[0]
    if TO_BLOCK==-1: TO_BLOCK = max(blocknumbers)[0]
    # print (FROM_BLOCK, TO_BLOCK); exit()
    
    fn = diagrams(df, FROM_BLOCK, TO_BLOCK, NAME_PREFIX, gas_logy=True, bt_logy=True, imgpath=imgpath)
    print ("\ndiagrams saved to: ", fn)
    return fn

###############################################################################

def CLI_params():

    if len(sys.argv)not in (3, 5):
        print ("Please give FOUR arguments, \n"
               "the filename DBFILE ___.db, \n"
               "a PREFIX for characterising the diagram output files; \n"
               "and FROM_BLOCK and TO_BLOCK for where to zoom,\n"
               "or\n"
               "give only the first TWO arguments, for the whole chain\n\n"
               "examples:\n"
               "%s temp.db TEMP 115 230\n"
               "%s temp.db TEMP\n" % (sys.argv[0], sys.argv[0]))
        exit(1)
        
    DBFILE=sys.argv[1]
    NAME_PREFIX=sys.argv[2]
    print ("using  DBFILE=%s  NAME_PREFIX=%s" % (DBFILE, NAME_PREFIX))

    if len(sys.argv)==3:
        FROM_BLOCK=-1
        TO_BLOCK=-1
        print ("for the whole chain, first to last block")
    else:
        FROM_BLOCK=int(sys.argv[3])
        TO_BLOCK  =int(sys.argv[4])
        print ("from block %d to block %d" % (FROM_BLOCK, TO_BLOCK) )        

    print ()
    return DBFILE, NAME_PREFIX, FROM_BLOCK, TO_BLOCK

if __name__ == '__main__':
    
    params = CLI_params(); 

    load_prepare_plot_save(*params)

    print ("Done.")
    
        