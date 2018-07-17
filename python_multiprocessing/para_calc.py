from multiprocessing import Process, cpu_count,current_process, Array


size=10

#A = [[i+j*size for i in range(size)] for j in range(size)]
A=[[3,0,0,3,3,5,2,2,4], [1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]

#B = [[1 for i in range(size)] for j in range(size)]
B=[[3,0,0,3,3,5,2,2,4],[1,2,0,3,6,2,1,5,2],[1,4,7,2,5,3,3,6,5],[3,5,2,5,2,5,3,6,3],[4,6,2,5,2,5,7,3,4],[6,2,6,4,2,5,6,2,6],[2,5,2,5,3,5,6,4,5],[4,2,4,5,2,5,3,4,5],[3,5,3,6,4,5,3,1,2]]

C = [0 for j in range(size*size)]


sheardC = Array('f',C)

number_of_cpus = cpu_count()

def calc_mat(mat1,mat2,sheardmat):

    cpuindex = int(current_process().name.split("-")[1])
    ### 実行されているプロセスを取得(ex:current_process()はProcess-1と出力するので、1だけを抽出する)

    row = len(mat1)/number_of_cpus
    ### この場合、行をcpu数で割ることで、各プロセスが担当するデータを定義する。

    start = int(row*(cpuindex-1))
    end = int(row*cpuindex)

    ### 10x10の行列の計算に、12processを使用した場合、process-1が1,2行目を担当する。

    for i in range(start,end):
        for j in range(size):
            for k in range(size):
                sheardmat[i*size+j] += mat1[i][k]*mat2[k][j]

calc_list = []

for i in range(number_of_cpus):
    calc = Process(target=calc_mat,args=(A,B,sheardC))
    ## Process(target=関数、args=関数の引数)
    calc.start()
    calc_list.append(calc)

[icalc.join() for icalc in calc_list]

for i,data in enumerate(sheardC.get_obj()):

    print("%6.1lf" % (data),end='')

    if (i+1)%size==0:

        print()
