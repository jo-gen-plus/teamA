from joblib import Parallel, delayed
from time import time
import sys
import random

t_arr1 = [[2, 55, 3, 0],[11, 7, 43, 6],[0, 8, 47, 1]]

t_arr2 = [[23, 2, 4, 23, 12],[3, 53, 39, 8, 10],[37, 39, 4, 9, 98],[3, 9, 7, 23, 87]]


def make_sqrMatrix(n):

    a = [[0 for i in range(n)]for i in range(n)]

    for i in range(n):
        
        for j in range(n):
            a[i][j] = random.randint(-100,100)

    return a




def calc_serial(arr1, arr2):
     ar = len(arr1)
     ac = len(arr1[0])
     br = len(arr2)
     bc = len(arr2[0])
     if ac != br:
          print("wrong type")
          return 

     c = [[0 for j in range(bc)]for i in range(ar)]

     for i in range(ar):
          
          for j in range(bc):
               for k in range(ac):
                    c[i][j] += arr1[i][k] * arr2[k][j]


     return c


def calc_parallel(arr1, arr2):
     # 計算可能かを確認
    ar = len(arr1)
    ac = len(arr1[0])
    br = len(arr2)
    bc = len(arr2[0])
    if ac != br:
         print("計算不可能な行列です。")
         return
     #result = make(ar)
    #print()
    return Parallel(n_jobs=-1)( [delayed(calc_PPart)(i, arr1, arr2) for i in range(ar)] )


def calc_PPart(i, a, b):
     #  １スレッドが行う計算  */
     # 今回は、「i 行目の計算」
    ac = len(a[0])
    bc = len(b[0])
    c = [0 for i in range(bc)]
    for j in range(bc):
         part = 0
         for k in range(ac):
              part += a[i][k] * b[k][j]
         c[j] = part
    return c



if __name__ == '__main__':
    # -*- coding: utf-8 -*-
    args = sys.argv

    #print(args)
    n = int(args[1])
    k = int(args[2])

    #print('第１引数：' + args[1])
    #print('第２引数：' + args[2])

    if n == 0:
    # テスト用の行列
        arr1 = t_arr1
        arr2 = t_arr2
    else:
        # ランダムに行列を作成。
        arr1 = make_sqrMatrix(n)
        arr2 = make_sqrMatrix(n)

    start = time()

    #result = [[]]
    if k == 0:
         print(calc_serial(arr1, arr2))
    else:
         print(calc_parallel(arr1, arr2))


    # 繰り返し計算 (並列化)
    #print(sum(result))

    print('{}秒かかりました'.format(time() - start))
