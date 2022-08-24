import subprocess
import sys
import os
from multiprocessing import Process, Pool
import multiprocessing
import time
from functools import partial

def eiger2cbf_pooled(_frame, _master, _output_stem):
    """
    Runs eiger2cbf for the specified frame.
    """
    #print("Starting {}".format(_frame))
    
    subprocess.run(args=['eiger2cbf.exe', _master, '{}'.format(_frame), '{}{:06d}.cbf'.format(_output_stem, _frame)],
                   stdout=subprocess.DEVNULL, 
                   stderr=subprocess.STDOUT) #stdout=subprocess.PIPE)
    
    #return subprocess.PIPE
    #print("Finished {}".format(_frame))
    return True

def eiger2cbf_get_span(_master):
    """
    Gets the _span from the master h5 file.
    """
    
    output = subprocess.run(args=['eiger2cbf.exe',_master], capture_output=True)
    try:
        _span = int(output.stdout.strip())
        print('Frames found: ', _span)
        return output.stdout.strip()
    except TypeError:
        
        print((output.stderr).decode('utf-8', 'ignore'))
        print((output.stdout).decode('utf-8', 'ignore'))
        return False
    except ValueError:
        print((output.stderr).decode('utf-8', 'ignore'))
        print((output.stdout).decode('utf-8', 'ignore'))
        return False    
    
if __name__ == "__main__":
    
    _master = sys.argv[1]
    
    try: 
        _t =  sys.argv[4] 
        if _t.lower()== 'test':
            _test=True
        else: _test = False
    except IndexError:
        _test=False    
    
    _pools = int(sys.argv[2])
        
    _output_stem = sys.argv[3]
        
    _span = eiger2cbf_get_span(_master)    
    
    _args_list = []
    
    for i in range(int(_span)):
        _args_list.append(i+1)
        
        
    if _test:
        print("You have {} cpu cores apparently.".format(multiprocessing.cpu_count()))
        _times = []
        if _pools < 6:
            _pstart = 1
        else:
            _pstart = _pools - 5     
        print("Testing {} to {} parallel processes with 10 frames in each pool:".format(_pstart, (_pools+5)))
        _times = []
        for i in range(_pstart, _pools+6):
            print("Testing {} processes...".format(i))
            _t1 = time.time()
            with Pool(processes=i) as p:
                _partial_pool = _args_list[:i*10]
                #print(_partial_pool)
                p.map(partial(eiger2cbf_pooled, _master=_master, _output_stem=_output_stem), _partial_pool)
                
            _t2 = time.time()
            _times.append(_t2-_t1)
        
        for i in range(len(_times)):
            print("For {} concurrent processes,\t {} total time,\t {} per frame".format(_pstart+i,_times[i], _times[i]/((_pstart+i)*10)))
        
    else:
        with Pool(processes=_pools) as p:
            p.map(partial(eiger2cbf_pooled, _master=_master, _output_stem=_output_stem), _args_list)
        
            
        