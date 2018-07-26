import os

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt



def Plot_pandas(df, graph_Fname, title='グラフ'):
    plt.figure()
    df.plot.line(
        title=title,
        grid=True,
        # Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, 
        # GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, 
        # Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, 
        # Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Vega10, Vega10_r, Vega20, Vega20_r, Vega20b, Vega20b_r, Vega20c, Vega20c_r, 
        # Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, 
        # afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, 
        # gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, 
        # gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, 
        # spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, viridis, viridis_r, winter, 
        colormap='tab10_r',
        legend=True,
        alpha=0.9,
        style='+-',
#        ylim=[0, ylim_up]
    )
    plt.savefig('result/{0}{1}.png'.format(experiment_name, graph_Fname))
    plt.close('all')


in_csvDirRoot = ''#'Parallel/'
in_csvFiles = (
      'results-[C] OpenMP.csv'
    , 'results-[Go].csv'
    , 'results-[Java].csv'
    , 'results-[Python] dask.csv'
    , 'results-[Python] joblib.csv'
    , 'results-[Python] joblib(+threading).csv'
    , 'results-[Python] multiprocessing.csv'
)

experiment_name = 'n=1000/'
ylim_up = 300

if __name__ == '__main__':
    in_csvDir = in_csvDirRoot + experiment_name
    #print(in_csvDir)
    os.makedirs( ('result/'+experiment_name), exist_ok=True)
    
    # csv 取り込み
    dfs = []
    for fname in in_csvFiles:
        in_csvPath = in_csvDir + fname
        dfs.append( pd.read_csv( in_csvPath, index_col=0 ) )


    ## グラフ：【逐次(0) 〜 並列(1~8)】を描画
    for df in dfs:
        #print(df.head())
        #print(df.columns.values)
        graph_name = df.columns.values[0]
        Plot_pandas(df, graph_name, title='【 {0} 】 x：並列度 と y：実行時間(s) のグラフ'.format(graph_name))


    ## グラフ：【逐次(0) 〜 並列(1~8) を一枚にまとめたグラフ】を描画
    merged_df = dfs[0].reset_index()
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df.reset_index())
    merged_df = merged_df.drop(columns='index')
    #print()
    #print(merged_df)
    Plot_pandas(merged_df, '[all] concurrency order', title='【 {0} 】 x：並列度 と y：実行時間(s) のグラフ'.format('全言語'))


    ## グラフ：【Python ライブラリの速度変化比較】を描画
    merged_df = dfs[-1].reset_index()
    for df in dfs[:-1]:
        if '[Python]' in df.columns.values[0]:
            merged_df = pd.merge(merged_df, df.reset_index())
    merged_df = merged_df.drop(columns='index')
    #print()
    #print(merged_df)
    Plot_pandas(merged_df, '[Pythons] concurrency order', title='【 {0} 】 x：並列度 と y：実行時間(s) のグラフ'.format('Pythonのみ'))


    ## グラフ：【Python 以外のライブラリの速度変化比較】を描画
    merged_df = dfs[0].reset_index()
    for df in dfs[:3]:
        if '[Python]' not in df.columns.values[0]:
            merged_df = pd.merge(merged_df, df.reset_index())
    merged_df = merged_df.drop(columns='index')
    #print()
    #print(merged_df)
    Plot_pandas(merged_df, '[C,Go,Java] concurrency order', title='【 {0} 】 x：並列度 と y：実行時間(s) のグラフ'.format('Python以外'))


    ## グラフ：【言語毎の比較（逐次と最速値の棒グラフ）】を描画
    column_names = ['serial time', 'parallel fast time']
    merged_df = pd.DataFrame(columns=column_names)
    languages = []
    #print(dfs)
    for df in dfs:
        col_name = df.columns.values[0]
        languages.append( col_name )
        df_tmp = pd.DataFrame( [[df.iat[0,0], df[1:][col_name].min()]], columns=column_names)
        merged_df = pd.concat([merged_df, df_tmp], ignore_index=True)
    #print()
    #print(merged_df)
    #print(languages)

    # 日本語を使う場合は以下の2行でフォントを準備
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(fname='/Users/e165738/Library/Fonts/ipaexg.ttf', size=9)

    w = 0.3  # 棒の幅
    y1 = merged_df['serial time']
    y2 = merged_df['parallel fast time']
    #print(y1)
    x = [i for i in range(len(y1))]  # データ数に合わせて横軸を準備

    plt.bar(x, y1, width=w, label='serial time', align="center")
    x2 = list(map(lambda xn: xn+w, x))
    plt.bar(x2, y2, width=w, label='parallel fast time', align="center")
    plt.legend(loc="best", prop=fp)  # 凡例を表示　日本語を使う場合はprop=fp
    plt.title("言語毎の比較（逐次と最速値の棒グラフ）")
    plt.xlabel("プログラミング言語")
    plt.ylabel("時間 (s)")

    # X軸の目盛りを科目名にする　日本語を使う場合はfontproperties=fp
    x_avg = list(map(lambda xn: xn+w/2, x))
    plt.xticks(x_avg, languages, fontproperties=fp, rotation=10)
    plt.savefig('result/{0}{1}.png'.format(experiment_name, '[all] serial vs parallel'))
    
    

