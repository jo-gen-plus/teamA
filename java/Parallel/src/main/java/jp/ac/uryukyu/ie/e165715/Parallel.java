package jp.ac.uryukyu.ie.e165715;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class Parallel {




    //n行n列のランダム行列を作成
    public static int[][] make_sqrMatrix(int n){
        Random randnum = new Random();
        int[][] d = new int[n][n];
        for(int i =0 ; i < n ; i ++){
            for(int j = 0; j< n ; j ++){
                d[i][j] = randnum.nextInt(4);
            }
        }

        return d;

    }



}

