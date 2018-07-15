package jp.ac.uryukyu.ie.e165715;
import jp.ac.uryukyu.ie.e165715.Matrix2D;

import java.util.Date;
import java.util.concurrent.Executor;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Parallel {
    public static void main(String[] args) throws InterruptedException {

        double[] _a = {1, 2, 3, 4};
        Matrix2D a = new Matrix2D(_a);
        //System.out.println(a);

        double[][] _b = {
                {1, 2, 3},
                {4, 5, 6},
                {7, 8, 9}
        };
        Matrix2D b = new Matrix2D(_b);
        long start = System.currentTimeMillis();

        for (int i=0;i<=5;i++){
            System.out.println(Matrix2D.mult(b, b));
        }

        long end = System.currentTimeMillis();



        //System.out.println(b);

        long start2 = System.currentTimeMillis();

        //https://qiita.com/koduki/items/086d42b5a3c74ed8b59e#executor-framework
        ExecutorService es = Executors.newWorkStealingPool();
        try {
            es.execute(() -> System.out.println(Matrix2D.mult(b, b)));
            es.execute(() -> System.out.println(Matrix2D.mult(b, b)));
            es.execute(() -> System.out.println(Matrix2D.mult(b, b)));
            es.execute(() -> System.out.println(Matrix2D.mult(b, b)));
            es.execute(() -> System.out.println(Matrix2D.mult(b, b)));
        } finally {
            es.shutdown();

        }
        long end2 = System.currentTimeMillis();


        System.out.println("逐次" + (end - start)  + "ms");
        System.out.println("並列" + (end2 - start2)  + "ms");

    }
}

