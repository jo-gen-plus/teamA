package jp.ac.uryukyu.ie.e165715;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class Parallel {

    private int[][] intmatrix;
    //コンストラクタ
    public  Parallel(int[][] vector){
        this.intmatrix = new int[vector.length][vector[0].length];
        for(int r=0; r<vector.length; r++){
            for(int c=0; c<vector[r].length; c++){
                this.intmatrix[r][c] = vector[r][c];
            }
        }

    }

    //行列の取得
    public int[][] getIntArrays(){
        return this.intmatrix;
    }
    //行数を取得
    public int getIntRow(){
        return this.intmatrix.length;
    }

    //列数を取得
    public int getIntCol(){
        return this.intmatrix[0].length;
    }

    private double getIntValue(int row, int col){
        return this.intmatrix[row][col];
    }


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
    //逐次処理
    public static Parallel calc_serial(Parallel arr1,Parallel arr2){

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

            return new Parallel(d);

    }
    //並列処理（全体）
    public  static Parallel calc_parallel(Parallel arr1,Parallel arr2){
        //スレッドの数(固定)のときnewFixedThreadPool
        //効率的に自動設定する時newWorkStealingPool
        final int MAX_THREADS = 2000;
            int[][] d = new int[arr1.getIntRow()][arr2.getIntCol()];
            Parallel pl = new Parallel(d);
                ExecutorService es = Executors.newFixedThreadPool(MAX_THREADS);
                try {
                    for (int r = 0 ; r < MAX_THREADS; r ++) {
                        int finalR = r;
                        es.execute(() -> pl.calc_PPart(arr1, arr2, finalR, d));
                    }
                } finally {
                    es.shutdown();

                }

            return new Parallel(d);


    }
    //並列処理（個別）
    public  void calc_PPart(Parallel arr1,Parallel arr2,int r,int[][] d){
        //r行目の処理
        for(int c=0; c<arr2.getIntCol(); c++){
            int sum = 0;
            for(int i=0; i<arr2.getIntRow(); i++){
                sum += arr1.getIntValue(r, i) * arr2.getIntValue(i, c);
            }
            d[r][c] = sum;
        }

    }

    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        for(int r=0; r<getIntRow(); r++){
            sb.append("|");
            for(int c=0; c<getIntCol(); c++){
                if(intmatrix[r][c] < 0)sb.append(String.format("%d ", intmatrix[r][c]));
                else sb.append(String.format(" %d ", intmatrix[r][c]));
            }
            sb.append("|\n");
        }
        return sb.toString();
    }
}

