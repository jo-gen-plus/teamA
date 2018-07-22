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



//gcc-6 -fopenmp OpenMP-final.c でコンパイル
/**
 * ./a.out 800 1 並列で実行する
 * １つ目は行列のnの大きさ(n*nの行列なので) 
 * ２つ目は並列度。0なら直列で他の数字なら並列で実行する
 * （並列度の指定とかは俺は出来なかった、本当はできるかもしれない)
 */


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

    int** c = malloc(sizeof(int *) * ar);

    for (int i = 0; i < ar; i++)
    {
        c[i] = malloc(sizeof(int) * bc);
    }
    
    for (int i = 0; i < ar; i++)
    {
        for (int j = 0; j < bc; j++)
        {
            c[i][j] = 0;

            for (int k = 0; k < ac; k++)
            {
                c[i][j] += arr1[i][k] * arr2[k][j];
                
                
            }

        }
    }

    return c;
}

/*  並列に計算  */
int** calc_parallel(int** arr1,int** arr2,int k,int ar,int ac,int bc)
{
    int** c = malloc(sizeof(int *) * ar);
    
    for (int i = 0; i < ar; i++)
    {
        c[i] = malloc(sizeof(int) * bc);
    }
    
    // 並列化 して計算
    // http://tech.ckme.co.jp/openmp.shtml
    #ifdef _OPENMP
    omp_set_num_threads(k);
    #endif
    #pragma omp parallel for private (j, k)
    for (int i = 0; i < ar; i++)
    {
        for (int j = 0; j < bc; j++)
        {
            //c[i][j] = 0;
            
            for (int k = 0; k < ac; k++)
            {
                c[i][j] += arr1[i][k] * arr2[k][j];
                
            }
        }
    }
    
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
        bc = 5;
    }
    else
    {
        arr1 = make_sqrMatrix(n);
        arr2 = make_sqrMatrix(n);
        ar = n;
        ac = n;
        bc = n;
    }
    
    t1 = gettimeofday_sec();
    if (k == 0)
    {
        result = calc_serial(arr1, arr2, ar, ac, bc);
    }
    else
    {
        result = calc_parallel(arr1, arr2, k, ar, ac, bc);
    }
    t2 = gettimeofday_sec();
    printf("%f\n", t2 - t1);
    return 0;
}
