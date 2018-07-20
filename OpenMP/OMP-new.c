#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <sys/time.h>

double gettimeofday_sec()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}



//gcc-6 -fopenmp OMP-new.c でコンパイル
//./a.out 800 1 並列で実行する
// 左は行列のnの大きさ(n*nの行列なので) 右は並列か直列かどうか0なら直列で他の数字なら並列で実行する（並列度の指定とかは俺は出来なかった、本当はできるかもしれない)


int i, j, k;

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

int** make_sqrMatrix(int n)
{
    int** a = malloc(sizeof(int *) * n);
    
    
    for (int i = 0; i < n; i++)
    {
        a[i] = malloc(sizeof(int) * n);
    }

    
    srand(time(NULL));
    
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            a[i][j] = rand() % 100;
        }
    }
    
    return a;
}

/*  直列に計算  */

int** calc_serial(int** arr1,int** arr2,int ar,int ac,int bc)
{
    //int ar = sizeof    arr1 / sizeof arr1[0];
    //int ac = sizeof arr1[0] / sizeof arr1[0][0];
    //int br = sizeof    arr2 / sizeof arr2[0];
    //int bc = sizeof arr2[0] / sizeof arr2[0][0];
    
    
/*
    if (ac != br)
    {
        printf("ERROR \n");
        return 0;
    }
*/
    /*
    c := make([][]int, ar)
    for i := 0; i < ar; i++ {
        c[i] = make([]int, bc)
        for j := 0; j < bc; j++ {
            for k := 0; k < ac; k++ {
                c[i][j] += arr1[i][k] * arr2[k][j]
            }
        }
    }
    */

    int** c = malloc(sizeof(int *) * ar);

    for (int i = 0; i < ar; i++)
    {
        c[i] = malloc(sizeof(int) * bc);
    }
    
    //clock_t start,end;
    //start = clock();
    
    for (int i = 0; i < ar; i++)
    {
        for (int j = 0; j < bc; j++)
        {
            c[i][j] = 0;

            for (int k = 0; k < ac; k++)
            {
                c[i][j] += arr1[i][k] * arr2[k][j];
                
                
            }
            //printf("%d \n",c[i][j]);
        }
    }
    //end = clock();
    //printf("%.2f秒かかりました\n",(double)(end-start)/CLOCKS_PER_SEC);
    
    return c;
}
int** calc_parallel(int** arr1,int** arr2,int ar,int ac,int bc)
{
    //int[] result;
    // 計算可能かを確認
    //const int ar = sizeof arr1 / sizeof arr1[0];        //縦の長さ
    //const int ac = sizeof arr1[0] / sizeof arr1[0][0];  //横の長さ
    //const int br = sizeof arr2 / sizeof arr2[0];        //縦の長さ
    //const int bc = sizeof arr1[0] / sizeof arr1[0][0]; //横の長さ
    //int result[][];
    //for i := 0; i < ar; i++ {
    int** c = malloc(sizeof(int *) * ar);
    
    for (int i = 0; i < ar; i++)
    {
        c[i] = malloc(sizeof(int) * bc);
    }
    
    //clock_t start,end;
    //start = clock();
    
    #pragma omp parallel for private (j, k)
    for (int i = 0; i < ar; i++)
    {
        for (int j = 0; j < bc; j++)
        {
            c[i][j] = 0;
            
            for (int k = 0; k < ac; k++)
            {
                c[i][j] += arr1[i][k] * arr2[k][j];
                
                
            }
            //printf("%d \n",c[i][j]);
        }
    }
    
    //end = clock();
    //printf("%.2f秒かかりました\n",(double)(end-start)/CLOCKS_PER_SEC/3.6); //現実の時間に合わせるために体感で3.6で割りました
    
    return c;
}

int main(int argc, char *argv[])
{
    int** arr1;
    int** arr2;
    int ar, ac, br, bc;
    int** result;
    
    double t1, t2;
    
    int n = atoi(argv[1]);
    int k = atoi(argv[2]);
    
    //行数を聞く
    if (n == 0)
    {
        arr1 = malloc(sizeof(int *) * 3);
        for (int i = 0; i < 3; i++)
        {
            arr1[i] = malloc(sizeof(int) * 4);
        }
        
        arr2 = malloc(sizeof(int *) * 4);
        for (int i = 0; i < 4; i++)
        {
            arr2[i] = malloc(sizeof(int) * 5);
        }
        //計算結果を入れるための配列の箱をまだ作っていない(未)
        
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 4; j++)
            {
                arr1[i][j] = t_arr1[i][j];
            }
        }
        
        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < 5; j++)
            {
                arr2[i][j] = t_arr2[i][j];
            }
        }
        ar = 3;
        ac = 4;
        //br = 4;
        bc = 5;
        //printf("%d",arr1[0][1]);
        //printf("\n");
    }
    else
    {
        ar = n;
        ac = n;
        //br = n;
        bc = n;
        arr1 = make_sqrMatrix(n);
        arr2 = make_sqrMatrix(n);
    }
    
    if (k == 0)
    {
        t1 = gettimeofday_sec();
        result = calc_serial(arr1, arr2, ar, ac, bc);
        t2 = gettimeofday_sec();
        printf("%f\n", t2 - t1);
    }
    else
    {
        t1 = gettimeofday_sec();
        result = calc_parallel(arr1, arr2, ar, ac, bc);
        t2 = gettimeofday_sec();
        printf("%f\n", t2 - t1);
    }
    return 0;
}





/*
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
 
 int** result = malloc(sizeof(int *) * ar);
 
 for (int i = 0; i < ar; i++)
 {
 result[i] = malloc(sizeof(int) * bc);
 }
 
 for (int i = 0; i < bc; i++)
 {
 for (int j = 0; j < ar; j++)
 {
 result[i][j] = 0;
 
 for (int k = 0; k < ac; k++)
 {
 result[i][j] += arr1[i][k] * arr2[k][j];
 }
 }
 }
 
 return (result);
 }






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
