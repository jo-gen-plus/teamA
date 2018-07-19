#!/usr/bin/perl
# perl executor.pl
use File::Spec;
use Time::Piece;

# とりえず、「<グラフ>「逐次(0) 〜 並列(1~8)」」の csv を作る。
# 1回につき 3回実行し、平均値をとる。


## 正方行列の１辺の大きさ。1000を推奨
$n = 10;

# 実行時に表示する文字のタブ
$tab = '   ';

###  実行するプログラム一覧  ###
my $programs = [
    ['Go', '../go/matrix/matrix_muler'],
#    ['Java', 'java -jar ../java/matrix_muler.jar'],
#    ['C-OpenMP', '../c/matrix_muler'],
#    ['Python-multiprocessing', 'python3 ../python_multiprocessing/matrix_muler'],
#    ['Python-joblib', 'python3 ../python_joblib/matrix_muler'],
#    ['Python-dask', 'python3 ../python_dask/matrix_muler']
];


# デバッグ
#print `pwd`;
#`cd ../`;
#print `pwd`;
#print `ls ../`;

## 現在のの日付・時間を取得
my $t = localtime;
$now_t = $t->hms("_");
print $now_t;
mkdir "$now_t", 0777 or die $!;

for (my $p = 0; $p < @$programs; $p++) {
    print "\n=====  $programs->[$p][0] 版 の実験を開始します。  =====\n";
    ## 結果を出力・保存するファイル
    $outputFile="$now_t".'/results_'."$programs->[$p][0]".'.csv';
    #print $outputFile;
    open(FILE, ">>$outputFile") or die "$!";  # ファルハンドル。追加書き込み
    
    ### 並列度毎 ###
    for (my $i = 0; $i < 2; $i++) {
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
        
        printf FILE "%f\n", $average_time;
    }
    
    close (FILE);
    print "\n";
}





# execute echo in back-quote
print "\nExperimentation compleated !\n\n";
