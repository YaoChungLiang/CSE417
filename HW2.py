# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 11:55:30 2019

@author: Yao-Chung Liang, 1826630, 
Readme:
    this is a multi-cases version, by changing the path in line 65 
    and making sure all the file in the directory are all test cases 
    with the same form of strings from the same generator CSE417 TA gave,
    then outputs will be generated.
    I did my best but somehow the part of biconnected graphs are always wrong,
    so I didn't put it into my code.

"""



#-------import some build in function---------------------------------------------
import copy                                           #using build-in copy function to copy some element
import time                                           #using build-in time fuction to calculate running time
import os                                             # using os to get system directory

'''
-------define my functionc in the beginning----------------------------------
'''
# define my DFS function to traverse all vertex I can reach from a certain start point
# input is a graph ( adjacency list) and an integer vertex
def dfs(graph,start):
    dfs_num_list=[]                                   # to store all vertex's dfs number
    explored=set()                                    # create a set to store all the vertex I already explored
    stack=[start]                                     # this stack is used to pop out next vertex I want to explore
    dfs_num_list=[-1]*len(graph)                      # initialize my all vertex's dfs number to be -1
    dfs_num=0                                         # dfs_num initilize to be 0 can treated as a counter
    while stack:                                      # while some vertex still in the stack (  some points have not been explored yet )
        vertex=stack.pop()                            # pop out the last one vertex in the stack to be next one to be explored
        if vertex not in explored:                    # check this vertex if be explored yet
            dfs_num_list[vertex]=dfs_num              # store present dfs number into the list
            dfs_num=dfs_num+1                         # after I explored a new vertex, the dfs number will add 1
            explored.add(vertex)                      # put the explored vertex into the list of explored
            stack.extend(set(graph[vertex])-explored) # compare with what I already explored and find some vertex I have not yet explored
    return dfs_num_list,explored                      # return the list of dfs number and the points I already explored  


# use try_art_ntimes to pick one point out at one time 
#and calculate if the number of  start point can reach eqauls to original graph
def try_art_ntimes(graph,start):
    art_set=[]                                        # use to store articulation points
    graph_saver=copy.deepcopy(graph)                  # store original graph for future to recover
    k=3                                               # another start point for me to use when trying to figure out which node is articulation point 
    for i in range(len(graph)):                       # run n times
        if graph[i] !={}:                             # check if there are some edges around the certain vertex
            graph[i]={}                               # clean the node's all edges
        for j in range(len(graph_saver)):             #run n times
            if i in graph[j]:                         # check if there are still some edges relevant to that node
                graph[j]=graph[j]-{i}                 # clean the edge from other nodes
        if i==0:                                      # if the node be deleted is 0
            k=1                                       # then change the start vertex from 1
        else:                                         # otherwise
            k=3                                       # start point remain from 3
            
        dfs_num,connected_component=dfs(graph,k)      # use dfs function to get the dfs number and number of connected component 
        graph=copy.deepcopy(graph_saver)              # recover the original graph, all edges once were deleted will recover
        if len(connected_component)<(len(graph)-1):   # if the vertex I can reach is less than total nodes-1 (1 is the one I deleted)
            art_set=art_set+[i]                       # then I announce this is a articulation point and store it into a list
    return art_set                                    # return the overall articulation points

'''
-------start the main function------------------------------------------
'''

# open the path where I stored all test cases
path = "D:/desktop/CSE417/biconnectivity-tests/try/"
dirs = os.listdir( path )                             # search for all the .txt file
for all_dir in dirs:                                  # take all file names out
    if ("txt" in all_dir) and ("out" not in all_dir): # check if the filename contains .txt and doesn't contain output file
       file_path=path+all_dir                         # generate the full file path
       output_file_path=path+"output_"+all_dir        # generate the full output file path
    else:                                             # if the file name doesn't contain .txt (not a text file)
        break                                         # get rid of the loop
    file = open(file_path,'r')                        # open the test file
    start_time=time.time()                            # start to record the running time
    listoftext=file.readlines()                       # read the text file line by line
    a=[]                                              # a list to store what I read
    for i in range(len(listoftext)-1):                # only n-1 line I need to read because the first line in the test file only contains number of node 
        i=i+1                                         # start to read from the second line
        a=a+listoftext[i].split()                     # read, split the strings in line and store into a list
    a=list(map(int,a))                                # map the string of numbers into integer of numbers
    total_edge=[]                                     # a list to store the list I will get from the test file
    for i in range(int((len(a))/2)):                  # by read two numbers every time so I only need to read n/2 times to get all edges
        i=i*2                                         # even number
        j=i+1                                         # odd number
        L=a[i]                                        # assign integer of index of even number to L 
        R=a[j]                                        # assign integer of index of odd number to R 
        total_edge=total_edge+[(L,R)]                 # store all edges 
    edges=total_edge                                  # assign all edges to another list, It's shorter and more convenient for me
    num_edges=len(edges)                              # get the number of edges
    ver=[]                                            # a list to store all vertex
    for i,j in total_edge:                            # check all edge pairs
        if i not in ver:                              # check if the node I already or not
            ver.append(i)                             # add this node into my vertex store place
        elif j not in ver:                            # check if the node I already or not
            ver.append(j)                             # add this node into my vertex store place
        else:                                         # if all of them already be stored 
            pass                                      # leave them alone
    vertex=ver                                        # use name of vertex is more comprehensible for myself (I am confused by ver and version)
    num_vertex=len(ver)                               # calculate the amount of vertex in the graph
    graph={}                                          # set a dictionary to store my adjacency list
    for i,j in total_edge:                            # read all my edges 
        graph.setdefault(i,[]).append(j)              # put my edges in a dictionary-list form {ex: {1:[0,3]}, 2:[5,6]} 
        graph.setdefault(j,[]).append(i)              # put my edges in a dictionary-list form {ex: {1:[0,3]}, 2:[5,6]}
    new_graph={}                                      # create a new dictionay to transform my form of edges from above
    for i in range(len(graph)):                       # check n nodes
        new_graph[i]=set(graph[i])                    # put my edges in a dictionary-set form {ex: {1:{0,3}}, 2:{5,6}}
    art_set = try_art_ntimes(new_graph,0)             # put my graph and start point inside the function to get all articulation points
    art_num=len(art_set)                              # number of articulation points
    runtime=time.time()-start_time                    # record the time I used to run all the process
 '''   
--------output my file result -----------------------------------------------
 '''   
    outFile = open(output_file_path,'w')                          # open an output file 
    outFile.write("----%s seconds ----\n"%runtime)                # write the running time into the output file
    outFile.write("number of vertex: %d\n " %num_vertex)          # write the number of vertex into the output file
    outFile.write("number of edges: %d\n" %num_edges)             # write the number of edges into the output file
    outFile.write("numbers of articulation points:%d\n" %art_num) # write the numbers of articulation points into the output file
    outFile.write("points of articulation points:")               # write the articulation points into the output file
    for art in art_set:                                           # because art_set contains a list of art points, I need to write one by one
        outFile.write("%d," % art)                                # write a art point number 
    outFile.close()                                               # close my output file
    file.close()                                                  # close my input file (test file)


