from joblib import Parallel, delayed
from time import time

t_arr1 = [[2, 55, 3, 0],[11, 7, 43, 6],[0, 8, 47, 1]]

t_arr2 = [[23, 2, 4, 23, 12],[3, 53, 39, 8, 10],[37, 39, 4, 9, 98],[3, 9, 7, 23, 87]]


def make_sqrMatrix(n):
	a = make(n)
	for i in range(n):
		a[i] = make(n)
		for j in range(n):
			a[i][j] = rand.Intn(100)

	return a


def calc_serial(arr1, arr2):
	ar = len(arr1)
	ac = len(arr1[0])
	br = len(arr2)
	bc = len(arr2[0])
	if ac != br:
		panic("wrong type")

	c = make(ar)

	for i in range(ar):
		c[i] = make(bc)
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
		panic("計算不可能な行列です。")
	#result = make(ar)
    print()
    return Parallel(n_jobs=-1)( [delayed(calc_PPart)(i, arr1, arr2, result, ch) for i in range(ar)] )


def calc_PPart(i, a, b, c, ch, chan):
	#  １スレッドが行う計算  */
	# 今回は、「i 行目の計算」
	ac = len(a[0])
	bc = len(b[0])
	for j in range(bc):
		part = 0
		for k in range(ac):
			part += a[i][k] * b[k][j]

		c[i][j] = part

	ch <- 1

if __name__ == '__main__':
    # -*- coding: utf-8 -*-


    start = time()

# 繰り返し計算 (並列化)
result = Parallel(n_jobs=-1)( [delayed(calc_PPart)(i) for i in range(10000)] )
print(sum(r))

print('{}秒かかりました'.format(time() - start))
