import numpy as np
import time
from numpy.random import *

from multiprocessing import Process, cpu_count,current_process, Array


"""
行列の積
C = A B
"""

#行列
a = np.array([[3,0,0,3,3,5,2,2,4], [1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]])
b = np.array([[3,0,0,3,3,5,2,2,4], [1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]])



start = time.time()#時間計測スタート
np.dot(a, b)#行列積の逐次計算



process_time = time.time() - start#時間計測終わり
print(process_time)#時間計測出力

print(np.dot(a, b))#行列積計算結果



