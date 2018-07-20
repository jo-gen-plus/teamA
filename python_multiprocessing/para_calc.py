from multiprocessing import Process, cpu_count,current_process, Array,Pool
import time
import random
import sys


t_arr1=[[1,1,1,1],[1,1,1,1],[1,1,1,1]]
t_arr2=[[3, 3, 3, 3, 3],[3, 3, 3, 3, 3],[3, 3, 3, 3, 3],[3, 3, 3, 3, 3]]

def make_sqrMatrix(n):
	a = [[0 for i in range(n)]for j in range(n)]

	for i in range(n):
		for j in range(n):
			a[i][j] = random.randint(0,100)
	return a



def calc_serial(arr1,arr2):

    ar=len(arr1)
    ac=len(arr1[0])
    br=len(arr2)
    bc=len(arr2[0])

    if ac != br:
        print("計算不可能な行列です。")
        return

    c =[[0 for j in range(bc)]for j in range(ar)]

    for i in range(ar):
        for j in range(bc):
            for k in range(ac):
                c[i][j] = arr1[i][k] * arr2[k][j]
    return c


def calc_parallel(arr1,arr2,k):

    ar = len(arr1)
    br = len(arr2)
    p = Pool(k)
    tutumimono = [[i, arr1, arr2] for i in range(ar)]

    result=p.map(wrapper_calc_PPart,tutumimono)
    p.close()
    return result


def calc_PPart(i,a,b):

    ac = len(a[0])
    bc = len(b[0])
    c = [0 for i in range(bc)]
    for j in range(bc):
        part = 0
        for k in range(ac):
            part += a[i][k] * b[k][j]

            #print(a[i][k] * b[k][j])

        c[j] = part
    return c

def wrapper_calc_PPart(args):
    return calc_PPart(*args)




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

    start = time.time()
    #calc_serial(t_arr1,t_arr2)

    if k == 0:
        result=calc_serial(arr1, arr2)
    else:
        result=calc_parallel(arr1, arr2,k)

   # print(result)

    #result=calc_parallel(arr1,arr2)#並列計算

    process_time = time.time() - start

    print(process_time)#経過時間


#テスト用A=[[3,0,0,3,3,5,2,2,4], [1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]

#テスト用B=[[3,0,0,3,3,5,2,2,4],[1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]


