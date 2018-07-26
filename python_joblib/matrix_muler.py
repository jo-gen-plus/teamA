#165724B 喜納　滉大

# -*- coding: utf-8 -*-
# $ pip install joblib
# または anaconda に切り替え
from joblib import Parallel, delayed
from time import time
import sys
import random


##  テスト用行列  ###
t_arr1 = [[2, 55, 3, 0],[11, 7, 43, 6],[0, 8, 47, 1]]
t_arr2 = [[23, 2, 4, 23, 12],[3, 53, 39, 8, 10],[37, 39, 4, 9, 98],[3, 9, 7, 23, 87]]


###  実験用の n*n正方行列 を作成  ###
def make_sqrMatrix(n):
    a = [[0 for i in range(n)]for i in range(n)]

    for i in range(n):
        for j in range(n):
            a[i][j] = random.randint(-100,100)

    return a



###  直列計算  ###
def calc_serial(arr1, arr2):
     ar = len(arr1)
     ac = len(arr1[0])
     br = len(arr2)
     bc = len(arr2[0])

     c = [ [0 for j in range(bc)] for i in range(ar) ]

     for i in range(ar):
          for j in range(bc):
               for k in range(ac):
                    c[i][j] += arr1[i][k] * arr2[k][j]

     return c


###  並列計算  ###
def calc_parallel(arr1, arr2,k):
    ar = len(arr1)
    ac = len(arr1[0])
    br = len(arr2)
    bc = len(arr2[0])
    
    ## 並列化して計算
    # マルチ プロセスで
    #return Parallel(n_jobs=k)( [delayed(calc_PPart)(i, arr1, arr2, ac, bc) for i in range(ar)] )
    # マルチ スレッドで
    return Parallel(n_jobs=k, backend="threading")( [delayed(calc_PPart)(i, arr1, arr2, ac, bc) for i in range(ar)] )


###  スレッドに食わせる処理１つ分  ###
def calc_PPart(i, a, b, ac, bc):
     #  １スレッドに行わせる計算  */
     # 今回は、「i 行目の計算」
    c = [0 for i in range(bc)]
    for j in range(bc):
         part = 0
         for k in range(ac):
              part += a[i][k] * b[k][j]
         c[j] = part
    return c


# 行列の掛け算が計算可能かを調べる
def isCalculableMatrix(arr1, arr2):
    # 計算可能かを確認
    ac = len(arr1[0])
    br = len(arr2)
    if ac != br:
         print("計算不可能な行列です。")
         return False
    return True


if __name__ == '__main__':
    args = sys.argv
    #print(args)
    #print('第１引数：' + args[1])
    #print('第２引数：' + args[2])
    n = int(args[1])
    k = int(args[2])


    if n == 0:
        # テスト用の行列
        arr1 = t_arr1
        arr2 = t_arr2
    else:
        # ランダムに行列を作成。
        arr1 = make_sqrMatrix(n)
        arr2 = make_sqrMatrix(n)

    ## 計算可能かを確認
    if not isCalculableMatrix(arr1, arr2):
        sys.exit()

    #result = [[]]
    start = time()
    if k == 0:
         result = calc_serial(arr1, arr2)
    else:
         result = calc_parallel(arr1, arr2,k)

    print(time() - start)
    #print('{}秒かかりました'.format(time() - start))
    #print(result)

