import random
import copy
import numpy as np

#############  trace back ver 2##########################
def show_trace_back(sequence,matrix):
    structure=[]
    N= len(sequence)
    for i in range(N):
        for j in range(0, i):
            matrix[i][j] = matrix[j][i]
    traceback(0,N-1, structure, matrix, sequence)
    return (sequence, write_structure(sequence, structure))
def pair_check(tup):
    if tup in [('A', 'U'), ('U', 'A'), ('C', 'G'), ('G', 'C')]:
        return True
    return False
def traceback(i, j, structure, DP, sequence):
    if j <= i:
        return
    #if j is unpaired, there will be no change in score when we take it out, so we just recurse to the next index
    elif DP[i][j] == DP[i][j-1]:
        traceback(i, j-1, structure, DP, sequence)
    else:
        #try pairing j with a matching index k to its left.
        for k in [b for b in range(i, j-4) if pair_check((sequence[b], sequence[j]))]:
            #if the score at i,j is the result of adding 1 from pairing (j,k) and whatever score
            #comes from the substructure to its left (i, k-1) and to its right (k+1, j-1)
            if k-1 < 0:
                if DP[i][j] == DP[k+1][j-1] + 1:
                    structure.append((k,j))
                    traceback(k+1, j-1, structure, DP, sequence)
                    break
            elif DP[i][j] == DP[i][k-1] + DP[k+1][j-1] + 1:
                #add the pair (j,k) to our list of pairs
                structure.append((k,j))
                #move the recursion to the two substructures formed by this pairing
                traceback(i, k-1, structure, DP, sequence)
                traceback(k+1, j-1, structure, DP, sequence)
                break

def write_structure(sequence, structure):
    dot_bracket = ["." for _ in range(len(sequence))]
    print(structure)
    for s in structure:
        dot_bracket[min(s)] = "("
        dot_bracket[max(s)] = ")"
    return "".join(dot_bracket)

################### generate random AUCG #########################333
def random_seq(n):
	AUCG=[]
	for i in range(n):
		x = random.randint(-2,2)
		while x == 0:
			x = random.randint(-2,2)
		AUCG.append(x)                ### Simulate A, U, C, G as -1, 1, -2, 2
	return  AUCG

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

###########  v3 finish   ######################################
def opt(start, end ,sequence):
    with_pair=0
    no_pair=0
    potential_t_comparer=[]
    if start >=  (end-4) :
        return 0
    else:
        no_pair=opt(start,end-1,sequence)
        for t in range(start,end-4):
            if sequence[t]+sequence[end]==0:
                potential_t_comparer+=[opt(start,t-1,sequence)+1+opt(t+1,end-1,sequence)]
            else:
                potential_t_comparer.append(0)
    with_pair = max(potential_t_comparer)
    return max(no_pair,with_pair)
    
def pair_table(sequence):
    size_of_table = len(sequence)
    w = size_of_table
    h = size_of_table
    table = [[0 for x in range(w)] for y in range(h)] 
    for k in range(4,len(sequence)):
        for i in range(0,len(sequence)-k):
            j=i+k
            table[i][j]=opt(i,j,sequence)
    return table
##############################################
#sequence=[2,-1,2,2,-2,-2,-1,-1,-2,2,1,1,-1,-2,-1,2]
#print(pair_table(sequence))
#traceback(0,len(sequence)-1,pair_table(sequence),sequence)
#print(generate_letters(random_seq(10)))
random=random_seq(20)
sequence=generate_letters(random)
print(pair_table(random))
print(show_trace_back(sequence,pair_table(random)))
         