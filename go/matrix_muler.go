package main

import (
	"fmt"
	"math/rand"
	"os"
	"runtime"
	"strconv"
	"time"
)

//
var intRange = 100

/**  テスト用の行列  */
var t_arr1 = [][]int{ // 3*4
	{2, 55, 3, 0},
	{11, 7, 43, 6},
	{0, 8, 47, 1},
}
var t_arr2 = [][]int{ // 4*1
	{23, 2, 4, 23, 12},
	{3, 53, 39, 8, 10},
	{37, 39, 4, 9, 98},
	{3, 9, 7, 23, 87},
}

/**  ランダムに行列を作成。  */
func make_sqrMatrix(n int) [][]int {
	a := make([][]int, n)
	for i := 0; i < n; i++ {
		a[i] = make([]int, n)
		for j := 0; j < n; j++ {
			a[i][j] = rand.Intn(intRange)
		}
	}
	return a
}

//type Matrix [][]int

/**  直列に計算  */
func calc_serial(arr1, arr2 [][]int) [][]int {
	ar := len(arr1)
	ac := len(arr1[0])
	br := len(arr2)
	bc := len(arr2[0])

	c := make([][]int, ar)
	for i := 0; i < ar; i++ {
		c[i] = make([]int, bc)
		for j := 0; j < bc; j++ {
			for k := 0; k < ac; k++ {
				c[i][j] += arr1[i][k] * arr2[k][j]
			}
		}
	}
	return c
}

/**  並列に計算  */
func calc_parallel(arr1, arr2 [][]int) [][]int {
	// 計算可能かを確認
	ar := len(arr1)
	ac := len(arr1[0])
	br := len(arr2)
	bc := len(arr2[0])

	result := make([][]int, ar)
	for i := 0; i < ar; i++ {
		result[i] = make([]int, bc)
	}

	// 並列化の際のおまじない
	ch := make(chan int)
	// それぞれの行を並列処理させる
	for i := 0; i < ar; i++ {
		// 並列化して実行。
		go calc_PPart(i, arr1, arr2, result, ch)
	}
	// 終わるまで待つ
	for i := 0; i < ar; i++ {
		<-ch
	}
	return result
}
func calc_PPart(i int, a, b, c [][]int, ch chan int) {
	/**  １スレッドが行う計算  */
	// 今回は、「i 行目の計算」
	ac := len(a[0])
	bc := len(b[0])
	for j := 0; j < bc; j++ {
		part := 0
		for k := 0; k < ac; k++ {
			part += a[i][k] * b[k][j]
		}
		c[i][j] = part
	}
	ch <- 1
}

// 行列の掛け算が計算可能かを調べる
func isCalculableMatrix(arr1, arr2 [][]int) bool {
	// 計算可能かを確認
	ac := len(arr1[0])
	br := len(arr2)
	if ac != br {
		fmt.Println("計算不可能な行列です。")
		return false
	}
	return true
}

/**
【引数】
	Args[1] :
		行列の大きさ（正方行列の一辺。nなら n*n 正方行列になる。）
	Args[2] :
		並列度（多分、スレッド数？）
*/
func main() {
	// 正方行列の一辺の大きさ(0の場合は、テスト用の配列の計算をする。)
	n, _ := strconv.Atoi(os.Args[1])
	// 並列度（スレッド数？）
	k, _ := strconv.Atoi(os.Args[2])
	runtime.GOMAXPROCS(k) //

	var arr1 [][]int
	var arr2 [][]int
	if n == 0 {
		// テスト用の行列
		arr1 = t_arr1
		arr2 = t_arr2
	} else {
		// ランダムに行列を作成。
		arr1 = make_sqrMatrix(n)
		arr2 = make_sqrMatrix(n)
	}

	// 計算可能かを確認
	if !isCalculableMatrix(arr1, arr2) {
		return
	}

	//計算結果
	//var result [][]int
	//fmt.Println("===Start===")
	bf_t := time.Now()
	if k == 0 {
		//result =
		calc_serial(arr1, arr2)
	} else {
		//result =
		calc_parallel(arr1, arr2)
	}
	af_t := time.Now()
	fmt.Println(af_t.Sub(bf_t).Seconds())
	//fmt.Println(strconv.FormatInt(af_t.Sub(bf_t).Nanoseconds(), 10))

	//fmt.Println(result)
}
