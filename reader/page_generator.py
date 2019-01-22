#!/usr/bin/env python3
"""
@summary:  human-readable page after each experiment
            incl tps.py outputs
            incl diagrams
            incl (e.g. network) start parameters

@version: v50 (13/January/2019)
@since:   13/January/2019
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

################################################################################
## Dependencies:

# standard library:
import sys, os, json, time
from pprint import pprint, pformat

# pypi:

# chainhammer
# extend sys.path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from hammer.config import FILE_LAST_EXPERIMENT

################################################################################

def read_infofile(fn=FILE_LAST_EXPERIMENT):
    """
    reads in json formatted file, returns dict
    """
    with open(fn, "r") as f:
        data = json.load(f)
    return data


def format_infofile_content(info):
    """
    presents content of infofile as text block
    """
    
    T=""
    
    i=info['node']
    T+="NODE: %s on %s\n" % (i['web3.version.node'], i['rpc_address'])
    T+="      consensus=%s chain_name=%s chain_id=%s network_id=%s\n"
    T=T % (i['consensus'], i['chain_name'], i['chain_id'], i['network_id'])
    
    i=info['send']
    T+="SEND: %d transactions in blocks %d-%d with %d empty blocks following.\n"
    T=T % (i['num_txs'], i['block_first'], i['block_last'], i['empty_blocks'])
    T+="      A sample of transactions looked as if they: "
    T+="succeeded." if i['sample_txs_successful'] else "failed (at least partially)."
    T+="\n"
    
    i=info['tps']
    T+="TPS:  The stopclock watcher measured a final TPS of %.1f since contract deploy,\n" % i['finalTpsAv']
    T+="      and in between saw values as high as %.1f TPS.\n" % i['peakTpsAv'] 
    
    i=info['diagrams']
    T+="DIAG: The whole experiment was prefixed '%s'.\n" % i['prefix']
    T+="      The diagrams were saved into '%s'.\n" % i['filename']
    T+="      Looking only at the experiment block-timestamps, the overall TPS was ~%.1f.\n" % i['blocktimestampsTpsAv']
    
    return T


def readTpsLog(fn):
    """
    read in a file, line by line
    """
    T = ""
    with open(fn, "r") as f:
        lines = f.readlines()
        # print ("log len:", len(lines))
        for line in lines:
            T += line
    return T


def title(info):
    """
    concatenate page title from info dict
    """
    version = info['node']['version']
    
    try: # perhaps cut away "-stable-316fc7ec"
        version = version.split("-")[0]
    except:
        pass
    
    T = "(%s) %s %s with %d txs: %.1f TPS"
    T = T % (info['diagrams']['prefix'],
        info['node']['name'], version, 
             info['send']['num_txs'], 
             info['diagrams']['blocktimestampsTpsAv'])  
    return T


def createElements(info, TPSLOG):
    """
    make title, infoblock, log, diagram-location
    """
    
    txt_info = format_infofile_content(info)
    #print (txt_info); print()
    
    txt_tpslog = readTpsLog(TPSLOG)
    # print (txt_tpslog)
    
    txt_title = title(info)
    # print (txt_title)
    
    image_location = info['diagrams']['filename']
    
    return txt_title, txt_info, txt_tpslog, image_location 


def save_page(body, fn, folder="../results/runs/"):
    """
    saves text to file
    """
    target = os.path.join(folder, fn)
    with open(target, "w") as f:
        f.write(body)
    return target


def timestamp_humanreadable(epoch):
    """
    epoch 0 <=> 1970-01-01
    """
    return time.strftime("%Y%m%d-%H%M", time.localtime(epoch))


def filename(info):
    """
    filename, ~unique because it contains the experiment start minute
    """
    epoch = info['tps']['start_epochtime']
    #print (epoch)
    ts = timestamp_humanreadable(epoch)
    fn = "%s_%s_txs%s" % (info['node']['name'], ts, info['send']['num_txs'])
    return fn



template01 = '''
## %s

### information:
```
%s
```

### log:
```
%s```

### diagrams:
![%s](%s)

### info raw:
%s
'''

def makeAndSave_MarkdownPage(infodict, title, info, tpslog, image_location,
                             runs_folder="../results/runs/"):
    """
    using the above template01, save a markdown page
    """
    
    img_path = "../../reader/" + image_location
    page = template01 % (title, info, tpslog, image_location, img_path,  pformat(infodict))
    # print(); print (page)
    return save_page(page, filename(infodict)+".md", folder=runs_folder)

    
template02 = '''
<html>
<head><title>%s</title></head>
<body>

<h2>%s</h2>

<h3>information:</h3>
<PRE>%s</PRE>

<h3>log:</h3>
<PRE>%s</PRE>

<h3>diagrams:</h3>
%s
<img src="%s"/>
<h3>info raw</h3>
<small>%s</small>
</body>
</html>
'''

def makeAndSave_HTMLPage(infodict, title, info, tpslog, image_location,
                         runs_folder="../results/runs/"):
    """
    using the above template02, save an HTML page
    """
    img_path = "../../reader/" + image_location
    page = template02 % (title,title, info, tpslog, image_location, img_path, pformat(infodict))
    # print(); print (page)
    return save_page(page, filename(infodict)+".html", folder=runs_folder)


def CLI_params():
    """
    paths&files are handed over via CLI argument
    """
    if len(sys.argv)!=3:
        print ("Please give two arguments, the filename of the experiment-infofile, and the tps.py logfile.")
        exit()
    else:
        INFOFILE=sys.argv[1]
        TPSLOG  =sys.argv[2] 
        print ("Reading from INFOFILE %s and from TPSLOG %s" % (INFOFILE, TPSLOG))
    return INFOFILE, TPSLOG


if __name__ == '__main__':
    
    INFOFILE, TPSLOG = CLI_params()
    
    info = read_infofile(INFOFILE)
    # pprint (info); print(); exit()
    
    elem = createElements(info, TPSLOG)
    
    fn = makeAndSave_MarkdownPage(info, *elem)
    print ("Page saved to: ", fn)
    fn = makeAndSave_HTMLPage(info, *elem)
    print ("Page saved to: ", fn)
    
    