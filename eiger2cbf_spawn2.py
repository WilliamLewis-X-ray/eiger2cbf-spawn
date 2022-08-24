import subprocess
import sys
import os
from multiprocessing import Process, Pool
import time
from functools import partial

def eiger2cbf_pooled(_frame, _master, _output_stem):
    """
    Runs eiger2cbf for the specified frame.
    """
    subprocess.run(args=['eiger2cbf.exe', _master, '{}'.format(_frame), '{}{:06d}.cbf'.format(_output_stem, _frame)])#,
                   #stdout=subprocess.DEVNULL, 
                   #stderr=subprocess.STDOUT) #stdout=subprocess.PIPE)
    print(_frame)
    #return subprocess.PIPE
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
        print(output.stderr)
        print(output.stdout)
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
    
    if _test:
        if _pools < 6:
            _pstart = 1
        else:
            _pstart = _pools - 5     
        print("Testing {} to {} parallel processes with 10 frames in each pool:".format(_pstart, (_pools+5)))
        _times = []
        for i in range(_pstart, _pools+6):
            _t1 = time.time()
            with Pool(processes=i) as p:
                p.map(partial(eiger2cbf_pooled, _master=_master, _output_stem=_output_stem), range(1,(i*10)))
        pass
        #for i range(_pstart, (_pools+6)):
         #   t1 = 
          #  with Pool(processes=i) as pool:
    
    else:
        with Pool(processes=_pools) as p:
            p.map(partial(eiger2cbf_pooled, _master=_master, _output_stem=_output_stem), range(1,(int(_span)+1)))
            #for i in range(int(_span)):
             #   print(i)
              #  p.apply_async(eiger2cbf_pooled, args=(_master, (i+1), _output_stem,))
            #results = [p.apply_async(eiger2cbf_pooled, args=(_master, (i+1), _output_stem,)) for i in range(int(_span))]
            
        