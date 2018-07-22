package jp.ac.uryukyu.ie.e165715;

import java.util.Random;

public class Main {
    static final int randNumber = 4 ;

    public static void main(String[] args ) throws InterruptedException {

        //n : 行数かつ列数。
        //スレッド数はParallelのcalc_parallel内のMAX_THREADSで変更可能
        //スレッド数を自動的に決定する場合はMAX_THREADSをコメントアウトし
        // newFixedThreadPool を　newWorkStealingPool　に変更
        //Calculator内のmake_sqrMatrixの中のrandnum.nextInt()で行列内の値のランダム幅を変更できる，現在は4(0~4)
        int n = 500;
        args = new String[]{"20","5"};
        int[] args_num = {0,0,0};

        try {
            args_num = checkAndConvert(args);
            n = args_num[0];
        } catch (ArrayIndexOutOfBoundsException e) {
            args_num[0] = 0;
            n = args_num[0];
        }
        System.out.println();


        Matrix t_arr1a = new Matrix(make_sqrMatrix(n));
        Matrix t_arr2a = new Matrix(make_sqrMatrix(n));

        int[][] d= new int[n][n];
        //答え入れる用
        Matrix ans1 = new Matrix(d);
        Matrix ans2 = new Matrix(d);


        long start = System.currentTimeMillis();

        Calculator calc = new Calculator();


        //System.out.println(Matrix.calc_serial(t_arr1bk, t_arr2bk));
        ans1 = calc.calc_serial(t_arr1a, t_arr2a);
        long end = System.currentTimeMillis();



        //System.out.println(calc.calc_parallel(t_arr1a,t_arr2a,args_num[1]));

        long start2 = System.currentTimeMillis();

        //https://qiita.com/koduki/items/086d42b5a3c74ed8b59e#executor-framework
        ans2 = calc.calc_parallel(t_arr1a,t_arr2a,args_num[1]);
        long end2 = System.currentTimeMillis();
        System.out.println(ans1);
        System.out.println(ans2);





        System.out.println("逐次" + (end - start)  + "ms");
        System.out.println("並列" + (end2 - start2)  + "ms");

        Thread.sleep(1_000L);
    }
    //n行n列のランダム行列を作成
    public static int[][] make_sqrMatrix(int n){
        Random randnum = new Random();
        int[][] d = new int[n][n];
        for(int i =0 ; i < n ; i ++){
            for(int j = 0; j< n ; j ++){
                d[i][j] = randnum.nextInt(randNumber);
            }
        }

        return d;

    }
    public static int[] checkAndConvert(String[] args){
        int row[] = new int[args.length];
        for(int i = 0 ;i < args.length ;i++) {
            //あるかないかのチェック
            if (args[i] == "") {
                row[i] = 0;
            } else {
                //数字かどうかのチェック
                try {
                    Integer.parseInt(args[1]);
                    row[i] = Integer.parseInt(args[i]);
                } catch (NumberFormatException e) {
                    row[i] = 0;
                }
            }
        }
        return row;
    }


}
