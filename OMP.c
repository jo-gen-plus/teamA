#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "mpi.h"
#include <time.h>
//#include <unistd.h>

// ここ以前に n の値を確保しておくこと


int t_arr1[3][4] =
{
    {2, 55, 3, 0},
    {11, 7, 43, 6},
    {0, 8, 47, 1},
};

int t_arr2[4][5] =
{
    {23, 2, 4, 23, 12},
    {3, 53, 39, 8, 10},
    {37, 39, 4, 9, 98},
    {3, 9, 7, 23, 87},
};

// add

int main (int argc, char *argv[])
{
    // 行列の生成
    
    int** arr1;
    int** arr2;
    int** result;
    
    int ar, ac, br, bc;
    
    int nnnn = atoi(argv[1]);
    int kkkk = atoi(argv[2]);
    
    if (nnnn == 0)
    {
        ar = sizeof    t_arr1 / sizeof t_arr1[0];
        ac = sizeof t_arr1[0] / sizeof t_arr1[0][0];
        br = sizeof    t_arr2 / sizeof t_arr2[0];
        bc = sizeof t_arr2[0] / sizeof t_arr2[0][0];
        
        arr1   = malloc(sizeof(int *) * ar);
        arr2   = malloc(sizeof(int *) * br);
        result = malloc(sizeof(int *) * ar);
        
        for (int i = 0; i < ar; i++)
        {
            arr1[i] = malloc(sizeof(int) * ac);
        }
        for (int i = 0; i < br; i++)
        {
            arr2[i] = malloc(sizeof(int) * bc);
        }
        for (int i = 0; i < ar; i++)
        {
            result[i] = malloc(sizeof(int) * bc);
        }
    }
    else
    {
        arr1   = malloc(sizeof(int *) * nnnn);
        arr2   = malloc(sizeof(int *) * nnnn);
        result = malloc(sizeof(int *) * nnnn);

        for (int i = 0; i < nnnn; i++)
        {
            arr1[i]   = malloc(sizeof(int) * nnnn);
            arr2[i]   = malloc(sizeof(int) * nnnn);
            result[i] = malloc(sizeof(int) * nnnn);
        }
    }

    if (nnnn == 0)
    {
        ar = sizeof    t_arr1 / sizeof t_arr1[0];
        ac = sizeof t_arr1[0] / sizeof t_arr1[0][0];
        br = sizeof    t_arr2 / sizeof t_arr2[0];
        bc = sizeof t_arr2[0] / sizeof t_arr2[0][0];
        
        for (int i = 0; i < ar; i++)
        {
            for (int j = 0; j < ac; j++)
            {
                arr1[i][j] = t_arr1[i][j];
            }
        }
        for (int i = 0; i < br; i++)
        {
            for (int j = 0; j < bc; j++)
            {
                arr2[i][j] = t_arr2[i][j];
            }
        }
    }
    else
    {
        //make_sqrMatrix
        
        srand(time(NULL));
        
        for (int i = 0; i < nnnn; i++)
        {
            for (int j = 0; j < nnnn; j++)
            {
                arr1[i][j] = rand() % 100;
                arr2[i][j] = rand() % 100;
            }
        }
        
        //arr1 = make_sqrMatrix(nnnn);
        //arr2 = make_sqrMatrix(nnnn);
    }
    
    if (kkkk == 0)
    {
        // calc_serial
        ar = sizeof    arr1 / sizeof arr1[0];
        ac = sizeof arr1[0] / sizeof arr1[0][0];
        br = sizeof   arr2 / sizeof arr2[0];
        bc = sizeof arr2[0] / sizeof arr2[0][0];
        
        printf("%d %d %d %d",ar,ac,br,bc);
        
        if (ac != br)
        {
            //printf("%d %d",ac ,br);
            
            printf("error");
        }
        
        for (int i = 0; i < ar; i++)
        {
            for (int j = 0; j < bc; j++)
            {
                result[i][j] = 0;
                
                for (int k = 0; k < ac; k++)
                {
                    result[i][j] += arr1[i][k] * arr2[k][j];
                }
            }
        }
    }
    else
    {
        //result = calc_parallel(arr1, arr2);
    }
    
    if (nnnn == 0)
    {
        int ar = sizeof    t_arr1 / sizeof t_arr1[0];
        int bc = sizeof t_arr2[0] / sizeof t_arr2[0][0];
        
        for (int i = 0; i < ar; i++)
        {
            for (int j = 0; j < bc; j++)
            {
                printf("%d ", result[i][j]);
            }
            
            printf("\n");
        }
    }
    else
    {
        for (int i = 0; i < nnnn; i++)
        {
            for (int j = 0; j < nnnn; j++)
            {
                printf("%d ", result[i][j]);
            }
            
            printf("\n");
        }
    }
    
    /*
    // malloc free
    
    for (int i = 0; i < nnnn; i++)
    {
        free(aaaa[i]);
    }
    
    free(aaaa);
     */
     
    return 0;
}

int make_sqrMatrix(int n)
{
    int** aaaa = malloc(sizeof(int *) * n);
    
    for (int i = 0; i < n; i++)
    {
        aaaa[i] = malloc(sizeof(int) * n);
    }
    
    srand(time(NULL));
    
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            aaaa[i][j] = rand() % 100;
        }
    }
    
    return (aaaa);
}

/* ちがうよ ひきすうとか
int calc_serial (int size1_1, int size1_2, int size2_1, int size2_2, int arr1[size1_1][size1_2], int arr2[size2_1][size2_2])
{
    int ar = sizeof    arr1 / sizeof arr1[0];
    int ac = sizeof arr1[0] / sizeof arr1[0][0];
    int br = sizeof    arr2 / sizeof arr2[0];
    int bc = sizeof arr2[0] / sizeof arr2[0][0];
    
    if (ac != br)
    {
        return 0;
    }
    
    int** cccc = malloc(sizeof(int *) * ar);
    
    for (int i = 0; i < ar; i++)
    {
        cccc[i] = malloc(sizeof(int) * bc);
    }
    
    for (int i = 0; i < bc; i++)
    {
        for (int j = 0; j < ar; j++)
        {
            cccc[i][j] = 0;
            
            for (int k = 0; k < ac; k++)
            {
                cccc[i][j] += arr1[i][k] * arr2[k][j];
            }
        }
    }
    
    return (cccc);
}
 */


///**  直列に計算  */
//int calc_serial(int[][] arr1,int arr2[][]){
//
//    const int ar = sizeof arr1 / sizeof arr1[0];        //縦の長さ
//    const int ac = sizeof arr1[0] / sizeof arr1[0][0];  //横の長さ
//    const int br = sizeof arr2 / sizeof arr2[0];        //縦の長さ
//    const int bc = sizeof arr2[0] / sizeof arr2[0][0]; //横の長さ
//
//    /*
//     if ac != br {
//     panic("wrong [][]int type")
//     }
//     */
//    int c[ar][bc];
//    k = 0;
//    for (i = 0; i < ar; i++) {
//        for (j = 0; j < bc; j++) {
//        }
//        c[i][j] = k;
//    }
//
//    for (i=0; i < ar; i++) {
//        for (j=0; j < bc; j++){
//            for (k=0; k < ac; j++){
//                c[i][j] += arr1[i][k] * arr2[k][j];
//            }
//        }
//    }
//    return c;
//}
//
///**  並列に計算  */
//int[][] calc_parallel(int arr1[][], arr2[][], c[][], result[][]){
//    int[] result;
//    // 計算可能かを確認
//    const int ar = sizeof arr1 / sizeof arr1[0];        //縦の長さ
//    const int ac = sizeof arr1[0] / sizeof arr1[0][0];  //横の長さ
//    const int br = sizeof arr2 / sizeof arr2[0];        //縦の長さ
//    const int bc = sizeof arr1[0] / sizeof arr1[0][0]; //横の長さ
//    int result[][];
//    /*
//     if ac != br {
//     panic("計算不可能な行列です。")
//     }
//     */
//    //for i := 0; i < ar; i++ {
//    int result[ar][bc];
//    k = 0;
//    for (i = 0; i < ar; i++) {
//        for (j = 0; j < bc; j++) {
//        }
//        result[i][j] = k;
//    }
//
//    // 並列化の際のおまじない
//    //ch := make(chan int)
//    // それぞれの行を並列処理させる
//#pragma omp parallel for private (j, k)
//    for(i=0; i<n; i++) {
//        for(j=0; j<n; j++) {
//            for(k=0; k<n; k++) {
//                result[i][j] += arr1[i][k] * arr2[k][j];
//            }
//        }
//    }
//    /* GO言語特有のもの
//     for (i=0; i < ar; i++){
//     go calc_PPart(i, arr1, arr2, result, ch)//並列処理
//     }
//     // 終わるまで待つ
//     for i := 0; i < ar; i++ {
//     <-ch
//     }*/
//    return result
//}
//
//
///**
// 【引数】
// Args[1] :
// 行列の大きさ（正方行列の一辺。nなら n*n 正方行列になる。）
// Args[2] :
// 並列度（多分、スレッド数？）
// */
//int main() {
//    // 正方行列の一辺の大きさ(0の場合は、テスト用の配列の計算をする。)
//    n, _ := strconv.Atoi(os.Args[1])
//    // 並列度（スレッド数？）
//    k, _ := strconv.Atoi(os.Args[2])
//    runtime.GOMAXPROCS(k) //
//
//    var arr1 [][]int
//    var arr2 [][]int
//    if n == 0 {
//        // テスト用の行列
//        arr1 = t_arr1
//        arr2 = t_arr2
//    } else {
//        // ランダムに行列を作成。
//        arr1 = make_sqrMatrix(n)
//        arr2 = make_sqrMatrix(n)
//    }
//    //計算結果
//    var result [][]int
//    if k == 0 {
//        result = calc_serial(arr1, arr2)
//    } else {
//        result = calc_parallel(arr1, arr2)
//    }
//    fmt.Println(result)
//}
