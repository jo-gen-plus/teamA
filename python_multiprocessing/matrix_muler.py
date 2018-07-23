from multiprocessing import Process, cpu_count,current_process, Array,Pool
import time
import random
import sys


##  テスト用行列  ###
t_arr1 = [[2, 55, 3, 0],[11, 7, 43, 6],[0, 8, 47, 1]]
t_arr2 = [[23, 2, 4, 23, 12],[3, 53, 39, 8, 10],[37, 39, 4, 9, 98],[3, 9, 7, 23, 87]]

###  実験用の n*n正方行列 を作成  ###
def make_sqrMatrix(n):
	a = [[0 for i in range(n)]for j in range(n)]

	for i in range(n):
		for j in range(n):
			a[i][j] = random.randint(-100,100)
	return a



###  直列計算  ###
def calc_serial(arr1,arr2):
    ar=len(arr1)
    ac=len(arr1[0])
    br=len(arr2)
    bc=len(arr2[0])

    c =[[0 for j in range(bc)] for j in range(ar)]

    for i in range(ar):
        for j in range(bc):
            for k in range(ac):
                c[i][j] += arr1[i][k] * arr2[k][j]
    
    return c


###  並列計算  ###
def calc_parallel(arr1,arr2,k):
    ar = len(arr1)
    ac = len(arr1[0])
    br = len(arr2)
    bc = len(arr2[0])
    
    ## 並列化して計算
    p = Pool(k)
    tutumimono = [[i, arr1, arr2, ac, bc] for i in range(ar)]
    result=p.map(wrapper_calc_PPart,tutumimono)
    p.close()
    return result


###  スレッドに食わせる処理１つ分  ###
def calc_PPart(i,a,b, ac, bc):
    c = [0 for i in range(bc)]
    for j in range(bc):
        part = 0
        for k in range(ac):
            part += a[i][k] * b[k][j]
        c[j] = part
    return c

def wrapper_calc_PPart(args):
    return calc_PPart(*args)


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
    
    #result = 0
    start = time.time()
    if k == 0:
        result = calc_serial(arr1, arr2)
    else:
        result = calc_parallel(arr1, arr2,k)

    process_time = time.time() - start
    print(process_time)#経過時間
    #print(result)


#テスト用A=[[3,0,0,3,3,5,2,2,4], [1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]

#テスト用B=[[3,0,0,3,3,5,2,2,4],[1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]


