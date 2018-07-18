package jp.ac.uryukyu.ie.e165715;

public class Main {
    public static void main(String[] args) throws InterruptedException {

        //n : 行数かつ列数。
        //スレッド数はParallelのcalc_parallel内のMAX_THREADSで変更可能
        //スレッド数を自動的に決定する場合はMAX_THREADSをコメントアウトし
        // newFixedThreadPool を　newWorkStealingPool　に変更
        //Parallel内のmake_sqrMatrixの中のrandnum.nextInt()で行列内の値のランダム幅を変更できる，現在は4(0~4)

        int n = 2000;

        Parallel t_arr1a = new Parallel(jp.ac.uryukyu.ie.e165715.Parallel.make_sqrMatrix(n));
        Parallel t_arr2a = new Parallel(jp.ac.uryukyu.ie.e165715.Parallel.make_sqrMatrix(n));

        int[][] d= new int[n][n];
        //答え入れる用
        Parallel ans1 = new Parallel(d);
        Parallel ans2 = new Parallel(d);

        long start = System.currentTimeMillis();

        //System.out.println(Parallel.calc_serial(t_arr1bk, t_arr2bk));
        ans1 = Parallel.calc_serial(t_arr1a, t_arr2a);
        long end = System.currentTimeMillis();



        long start2 = System.currentTimeMillis();

        //https://qiita.com/koduki/items/086d42b5a3c74ed8b59e#executor-framework
        ans2 = Parallel.calc_parallel(t_arr1a,t_arr2a);
        long end2 = System.currentTimeMillis();
        System.out.println(ans1);
        System.out.println(ans2);


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

}
