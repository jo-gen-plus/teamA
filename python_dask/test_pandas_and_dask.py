import pandas as pd
import dask.dataframe as dd
from dask.multiprocessing import get
import sys
from time import time
import warnings


def mysum(row):
    return row["x"] + row["y"] 


if __name__ == '__main__':
    # -*- coding: utf-8 -*-
    args = sys.argv
    
    #print(args)
    n = int(args[1])
    k = int(args[2])
    

    df = pd.DataFrame({"x": range(100000), "y": range(0, -100000, -1)})
    
    #warnings.filterwarnings('ignore')
    start = time()
    #result = [[]]
    if k == 0:
        sums = df.apply(mysum, axis=1)
    else:
        ddf = dd.from_pandas(df, npartitions=k)
        sums = ddf.apply(mysum, axis=1, meta=('int')).compute(scheduler='processes')
    print(time() - start)
    #print('{}秒かかりました'.format(time() - start))
    #print(result)

