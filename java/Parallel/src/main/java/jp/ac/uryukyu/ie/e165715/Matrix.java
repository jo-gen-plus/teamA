package jp.ac.uryukyu.ie.e165715;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

//e165715　上原正基
public class Matrix {
    private int[][] intmatrix;
    public  Matrix(int[][] vector){
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

    public int getIntValue(int row, int col){
        return this.intmatrix[row][col];

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

