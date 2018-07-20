from multiprocessing import Process, cpu_count,current_process, Array,Pool
import time
import random

#r1=random.randrange(2000)#2000までのN

t_arr1=[[2,55,3,0],[11,7,43,6],[0,8,47,1]]
t_arr2=[[23, 2, 4, 23, 12],[3, 53, 39, 8, 10],[37, 39, 4, 9, 98],[3, 9, 7, 23, 87]]

def make_sqrMatrix(n):
	a = [[0 for i in range(n)]for j in range(n)]

	for i in range(n):
		for j in range(n):
			a[i][j] = random.randint(100)
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
                print(c)
                c[i][j] = arr1[i][k] * arr2[k][j]
    return c


def calc_parallel(arr1,arr2):

    ar = len(arr1)
    p = Pool(4)
    p.map(calc_PPart,range(ar))

    p.close()


def calc_PPart(i,a,b,c):

	ac = len(a[0])
	bc = len(b[0])

    c = [0 for i in range(bc)]

	for j in range(bc):
		part = 0
		for k in range(ac):
			part += a[i][k] * b[k][j]
		c[i] = part
    return c


if __name__ == '__main__':
    args = sys.argv
    start = time.time()
    calc_serial(t_arr1,t_arr2)
    calc_parallel(t_arr1,t_arr2)#並列計算
    process_time = time.time() - start





    print('計算時間'.format(process_time))#経過時間


#テスト用A=[[3,0,0,3,3,5,2,2,4], [1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]

#テスト用B=[[3,0,0,3,3,5,2,2,4],[1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]


