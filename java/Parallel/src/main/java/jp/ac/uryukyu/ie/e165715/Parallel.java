package jp.ac.uryukyu.ie.e165715;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Parallel {
    public static void main(String[] args) throws InterruptedException {

        //int[] _a = {1, 2, 3, 4};
        //Matrix2D a = new Matrix2D(_a);
        //System.out.println(a);


        int[][] t_arr1 = {
                {1, 2, 3, 4, 5},
                {4, 5, 6, 7 ,8},
                {7, 8, 9, 10, 11},
                {12, 13, 14, 15, 16},
                {17, 18, 19, 20, 21}
        };
        int[][] t_arr2 = {
                {1, 2, 3, 4, 5},
                {4, 5, 6, 7 ,8},
                {7, 8, 9, 10, 11},
                {12, 13, 14, 15, 16},
                {17, 18, 19, 20, 21}
        };



        Parallel t_arr1a = new Parallel(t_arr1);
        Parallel t_arr2a = new Parallel(t_arr2);
        Parallel ans1 = new Parallel(make_sqrMatrix(5,5));
        Parallel ans2 = new Parallel(make_sqrMatrix(5,5));
        long start = System.currentTimeMillis();
        /*
        for (int i=0;i<=5;i++){
            System.out.println(Matrix2D.mult(t_arr1a, t_arr2a));
        }
        */
        //System.out.println(Parallel.calc_serial(t_arr1bk, t_arr2bk));
        ans1 = Parallel.calc_serial(t_arr1a, t_arr2a);
        long end = System.currentTimeMillis();



        long start2 = System.currentTimeMillis();

        //https://qiita.com/koduki/items/086d42b5a3c74ed8b59e#executor-framework
        ans2 = Parallel.calc_parallel(t_arr1a,t_arr2a);
        long end2 = System.currentTimeMillis();
        System.out.println(ans1);
        System.out.println(ans2);

        //System.out.println("並列");
        long start3 = System.currentTimeMillis();
        System.out.println(Parallel.calc_serial(t_arr1a, t_arr2a));
        long end3 = System.currentTimeMillis();
        long start4 = System.currentTimeMillis();
        System.out.println(Parallel.calc_parallel(t_arr1a, t_arr2a));
        long end4 = System.currentTimeMillis();


        System.out.println("逐次" + (end - start)  + "ms");
        System.out.println("並列" + (end2 - start2)  + "ms");
        System.out.println("逐次" + (end3 - start3)  + "ms");
        System.out.println("並列" + (end4 - start4)  + "ms");

    }
    private int[][] intmatrix;
    //make_sqrMatrix
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
    public static int[][] make_sqrMatrix(int a_row, int b_col){
        int[][] d = new int[a_row][b_col];

        return d;

    }

    public static Parallel calc_serial(Parallel arr1,Parallel arr2){
        if(arr1.getIntCol() == arr2.getIntRow()) {
            int[][] d = make_sqrMatrix(arr1.getIntRow(), arr2.getIntCol());
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
        else{
            return null;
        }

    }
    public  static Parallel calc_parallel(Parallel arr1,Parallel arr2){
        if(arr1.getIntCol() == arr2.getIntRow()){
            int[][] d = make_sqrMatrix(arr1.getIntRow(),arr2.getIntCol());
            Parallel pl = new Parallel(d);
                ExecutorService es = Executors.newFixedThreadPool(5);
                try {
                    es.execute(() -> pl.calc_PPart(arr1,arr2,0,d));
                    es.execute(() -> pl.calc_PPart(arr1,arr2,1,d));
                    es.execute(() -> pl.calc_PPart(arr1,arr2,2,d));
                    es.execute(() -> pl.calc_PPart(arr1,arr2,3,d));
                    es.execute(() -> pl.calc_PPart(arr1,arr2,4,d));
                } finally {
                    es.shutdown();

                }

            return new Parallel(d);
        }
        else{
            return null;
        }


    }
    public  void calc_PPart(Parallel arr1,Parallel arr2,int r,int[][] d){
        //r行目
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

