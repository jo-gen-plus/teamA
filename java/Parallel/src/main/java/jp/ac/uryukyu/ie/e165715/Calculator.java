package jp.ac.uryukyu.ie.e165715;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Calculator {


    //逐次処理
    public  Matrix calc_serial(Matrix arr1,Matrix arr2){

        int[][] d = new int[arr1.getIntRow()][arr2.getIntCol()];
        for (int r = 0; r < arr1.getIntRow(); r++) {
            for (int c = 0; c < arr2.getIntCol(); c++) {
                int sum = 0;
                for (int i = 0; i < arr2.getIntRow(); i++) {
                    sum += arr1.getIntValue(r, i) * arr2.getIntValue(i, c);
                }
                d[r][c] = sum;
            }
        }

        return new Matrix(d);

    }
    //並列処理（全体）
    public   Matrix calc_parallel(Matrix arr1,Matrix arr2,int ParallelDigree){
        //スレッドの数(固定)のときnewFixedThreadPool
        //効率的に自動設定する時newWorkStealingPool
        final int MAX_THREADS = 500;
        int[][] d = new int[arr1.getIntRow()][arr2.getIntCol()];
        ExecutorService es = Executors.newFixedThreadPool(MAX_THREADS);
        try {
            for (int r = 0 ; r < MAX_THREADS; r ++) {
                int finalR = r;
                es.execute(() -> calc_PPart(arr1, arr2, finalR, d));
            }
        } finally {
            es.shutdown();

        }

        return new Matrix(d);


    }
    //並列処理（個別）
    public  void calc_PPart(Matrix arr1,Matrix arr2,int r,int[][] d){
        //r行目の処理
        for(int c=0; c<arr2.getIntCol(); c++){
            int sum = 0;
            for(int i=0; i<arr2.getIntRow(); i++){
                sum += arr1.getIntValue(r, i) * arr2.getIntValue(i, c);
            }
            d[r][c] = sum;
        }

    }

}
