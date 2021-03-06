#!/usr/bin/perl
# perl executor.pl
use File::Spec;
use Time::Piece;

# とりえず、「<グラフ>「逐次(0) 〜 並列(1~8)」」の csv を作る。
# 1回につき 3回実行し、平均値をとる。


## 正方行列の１辺の大きさ。1000を推奨
$n = 50;
## 並列度の範囲。実験は 8 まで行った。
$concurrency_range = 8;

# 実行時に表示する文字のタブ
$tab = '   ';

###  実行するプログラム一覧  ###
my $programs = [
    ['[Java]', 'java -jar ../java/matrix_muler.jar'],
#    ['[C] OpenMP', '../c_OpenMP/matrix_muler'],
    # マルチプロセス と マルチスレッドを選べる。
    ['[Python] multiprocessing', 'python3 ../python_multiprocessing/matrix_muler.py'],
    ['[Python] joblib', 'python3 ../python_joblib/matrix_muler.py'],
#    ['[Python] dask', 'python3 ../python_dask/matrix_muler.py']
#    ['[Python] dask-t_Pandas', 'python3 ../python_dask/test_pandas_and_dask.py']
    ['[Go]', '../go/matrix_muler'],
];


# デバッグ
#print `pwd`;
#`cd ../`;
#print `pwd`;
#print `ls ../`;

## 現在のの日付・時間を取得
my $t = localtime;
$now_t = $t->hms("_");
#print $now_t;
mkdir "$now_t", 0777 or die $!;


print "\n\n実験を開始します！\n";
sleep(2);
print "3\n";
sleep(1);
print "2\n";
sleep(1);
print "1\n";
sleep(1);
print "・\n・\n・\n";


for (my $p = 0; $p < @$programs; $p++) {
    print "\n=====  $programs->[$p][0] 版 を開始します。  =====\n";
    sleep(1);
    ## 結果を出力・保存するファイル
    $outputFile="$now_t".'/results-'."$programs->[$p][0]".'.csv';
    #print $outputFile;
    open(FILE, ">>$outputFile") or die "$!";  # ファルハンドル。追加書き込み
    # ファイルに列名を追加
    printf FILE ",%s\n", $programs->[$p][0];
    
    ### 並列度毎 ###
    for (my $i = 0; $i < $concurrency_range; $i++) {
        print "＜並列度： $i ＞\n";
        # 実行するコマンドを作る
        $cmd = $programs->[$p][1]." $n $i";
        #print "$tab$tab$cmd\n";  # デバッグ
        
        ## 3回計測
        $average_time = 0;
        for (my $c = 1; $c <= 3; $c++) {
            print "$tab$c 回目：";
            chomp(my $result_time = `$cmd`);
            $average_time = $average_time + $result_time;
            print "$tab$result_time s\n";
        }
        # 平均タイムを計算
        $average_time = $average_time / 3;
        print $tab."Average Time：\n";
        print "$tab$tab$average_time s\n\n";
        
        # ファイルに出力
        printf FILE "%d,%f\n", $i, $average_time;
        sleep(1);
    }
    
    close (FILE);
    print "\n";
}





# execute echo in back-quote
#print "\nExperimentation compleated !!\n\n";
