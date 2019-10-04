import random
import numpy as np                                      
import time                                         
import os                                           
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(15000)
# The way I used to index the OPT table is like the one on slides,
# which is from the top-left to the top-right and there is the max opt value in the top-right 
# and thus construct a upper triangle.

#############  trace back##########################
class RNA:
    def show_trace_back(sequence,matrix):
        structure=[]
        N= len(sequence)
        RNA.traceback(0,N-1, structure, matrix, sequence)
        parens_dots, struc=RNA.write_structure(sequence, structure)
        return sequence, parens_dots,struc    
    def pair_check(link):
        if link in [('A', 'U'), ('U', 'A'), ('C', 'G'), ('G', 'C')]:
            return True
        return False
    def traceback(i, j, structure, tab, sequence):
        if j <= i:
            return
        elif tab[i][j] == tab[i][j-1]:
            RNA.traceback(i, j-1, structure, tab, sequence)
        else:
            for k in [b for b in range(i, j-4) if RNA.pair_check((sequence[b], sequence[j]))]:
                if k-1 < 0:
                    if tab[i][j] == tab[k+1][j-1] + 1:
                        structure.append((k,j))
                        RNA.traceback(k+1, j-1, structure, tab, sequence)
                        break
                elif tab[i][j] == tab[i][k-1] + tab[k+1][j-1] + 1:
                    structure.append((k,j))
                    RNA.traceback(i, k-1, structure, tab, sequence)
                    RNA.traceback(k+1, j-1, structure, tab, sequence)
                    break
    def write_structure(sequence, structure):
        dot_bracket = ["." for _ in range(len(sequence))]
        for s in structure:
            dot_bracket[min(s)] = "("
            dot_bracket[max(s)] = ")"
        return "".join(dot_bracket) , structure
################### generate random AUCG #########################333
    def random_seq(n):
        AUCG=[]
        x=0
        for i in range(n):
            x = random.randint(-2,2)
            while x == 0:
                x = random.randint(-2,2)
            AUCG.append(x)               
        return  AUCG
# turn integers to letters
    def generate_letters(AUCG):
        AUCG_list=[]
        AUCG_string=''
        for i in AUCG:
            if i == 2 :
                AUCG_list.append('C')
            elif i == -2:
                AUCG_list.append('G')
            elif i == 1:
                AUCG_list.append('A')
            elif i == -1:
                AUCG_list.append('U')
            else:
                pass
        AUCG_string=AUCG_string.join(AUCG_list)
        return AUCG_string
# turn letters to integers
    def letter_to_int(sequence):
        list_of_sequence=list(sequence)
        list_of_sequence= [w.replace('A','1' ) for w in list_of_sequence]
        list_of_sequence= [w.replace('U','-1' ) for w in list_of_sequence]
        list_of_sequence= [w.replace('C','2' ) for w in list_of_sequence]
        list_of_sequence= [w.replace('G','-2' ) for w in list_of_sequence]
        list_of_sequence = list(map(int, list_of_sequence))
        return list_of_sequence
###########  opt  ######################################
    def opt(start, end):
        no_pair=0
        if start >=  (end-4) :
            return 0
        else:
            no_pair=table[start][end-1]
            potential_t_comparer=[]
            with_pair=0
            for t in range(start,end-4):
                if sequence[t]+sequence[end]==0:
                    potential_t_comparer+=[table[start][t-1]+1+table[t+1][end-1]]
                else:
                    potential_t_comparer.append(0)
        with_pair = max(potential_t_comparer)
        return max(no_pair,with_pair)
# constructing table
    def pair_table(sequence):
        for k in range(4,len(sequence)):
            for i in range(0,len(sequence)-k):
                j=i+k
                table[i][j]=RNA.opt(i,j)
        return table
#################   main 1  ############################
if __name__ == "__main__":
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    outfile = open('out.txt','w')
    for file in os.listdir(dir_path):
        if file.endswith("testcase.txt"):
            with open(file) as f:
                lines = f.readlines()
            for line in lines:
                seq=line.strip('\n')
                table = [[0 for x in range(len(seq))] for y in range(len(seq))]
                sequence=RNA.letter_to_int(seq)
                start_time=time.clock()
                table1 = RNA.pair_table(sequence)
                sequence1, parens_dots1,struc1=RNA.show_trace_back(seq,table1)
                running_time1 = time.clock()-start_time 
                outfile.write(sequence1)
                outfile.write('\n{}'.format(parens_dots1))
                outfile.write('\nLength = {}, Pairs = {}, Time = {} sec\n'.format(len(sequence1),len(struc1),running_time1))
                if len(seq) <25:
                    mat = np.matrix(table1)
                    for line in mat:
                        np.savetxt(outfile, line, fmt='%d')
                outfile.write('{}\n'.format(''))
    outfile.close()
    
    if (True):  # Change to stop/start the random sample 
        m=[]
        runtime_list2=[]
        for i in range(12,13):
            m+=[2**i]
            seq2=RNA.random_seq(2**i)
            sequence=seq2
            sequence2=RNA.generate_letters(seq2)
            table = [[0 for x in range(len(sequence2))] for y in range(len(sequence2))]
            start_time2=time.clock()
            table2 = RNA.pair_table(sequence2)
            sequence2, parens_dots2,struc2=RNA.show_trace_back(sequence2,table2)
            running_time2=time.clock()-start_time2
            runtime_list2+=[running_time2]
            print(running_time2)
        m=np.log2(m)
        plt.figure()
        plt.plot(m,runtime_list2,'r--',label='test')
        plt.ylabel("running time (s)")
        plt.xlabel("input size (log2(n))")
        plt.legend(loc='upper left')
        plt.savefig(dir_path+'/HW7_rand_test1.png')
        plt.show()        
   
