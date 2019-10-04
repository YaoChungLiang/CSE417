# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 15:05:40 2019

@author: Admin
"""


import copy                                           #using build-in copy function to copy some element
import time                                           #using build-in time fuction to calculate running time
import os                                             # using os to get system directory
import numpy as np
import random
import matplotlib.pyplot as plt


def dist(p1,p2):
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


###------version 3 -------------------------------
def v3_closest_pair(arr_x, arr_y):
#    print("ay =",ay)
    p_num = len(arr_x)  
    if p_num<=1:
        return arr_x[0][0],arr_x[0][1],None
    if p_num <= 3:
        tarp1=arr_x[0]
        tarp2=arr_x[1]
        d_min=dist(arr_x[0],arr_x[1])
        for i in range(p_num-1):
            for j in range(i+1,p_num):
                if i!=j:
                    p1=arr_x[i]
                    p2=arr_x[j]
                    d=dist(p1,p2)
                    if d<d_min:
                        d_min=d
                        tarp1=p1
                        tarp2=p2
#        print("d_min = ",d_min)
        return tarp1,tarp2,d_min
    mid = p_num // 2  # Division without remainder, need int
#    print("mid",mid)
    Lx = arr_x[:mid]  # Two-part split
#    print('Qx= x left plane')
#    print(Qx)
    Rx = arr_x[mid:]
#    print('Rx = x right plane',Rx)
    # Determine midpoint on x-axis
    midpoint = arr_x[mid][0]
#    print("midpoint = ",midpoint)
    Ly = list()
    Ry = list()
    for x in arr_y:  # split ay into 2 arrays using midpoint
        if x[0] <= midpoint:
           Ly.append(x)
#           print("Qy= ",Qy)
        else:
           Ry.append(x)
#           print("Ry= ",Ry)
    # Call recursively both arrays after split
    (L1, LL1, mi1) = v3_closest_pair(Lx, Ly)
    (R2, RR2, mi2) = v3_closest_pair(Rx, Ry)
    # Determine smaller distance between points of 2 arrays
    if mi1 <= mi2:
        d = mi1
        mn = (L1, LL1)
    else:
        d = mi2
        mn = (R2, RR2)
    # Call function to account for points on the boundary
    (p3, q3, mi3) = v3_mid_area(arr_x, arr_y, d, mn)
    # Determine smallest distance for the array
    if d <= mi3:
        return mn[0], mn[1], d
    else:
        return p3, q3, mi3
    
    
####--------------------------------------    
    
def v3_mid_area(p_x, p_y, delta, best_pair):
    ln_x = len(p_x)  # store length - quicker
    mx_x = p_x[ln_x // 2][0]  # select midpoint on x-sorted array
    # Create a subarray of points not further than delta from
    # midpoint on x-sorted array
    s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
    best = delta  # assign best value to delta
    ln_y = len(s_y)  # store length of subarray for quickness
    for i in range(ln_y - 1):
        for j in range(i+1, min(i + 7, ln_y)):
            p, q = s_y[i], s_y[j]
            dst = dist(p, q)
            if dst < best:
                best_pair = p, q
                best = dst
    return best_pair[0], best_pair[1], best

####------version 1------------------------------------------
#def v1_brute(sort_x_p):
#    p=copy.deepcopy(sort_x_p)
#    print('brute=',p)
#    if len(sort_x_p)==1:
#        return sort_x_p[0][0],sort_x_p[0][1],None
#    else:
#        d_min=dist(p[0],p[1])
#        p1=p[0]
#        p2=p[1]
#        p_num=len(p)
#        if p_num==2:
#            return p1,p2,d_min
#        for i in range(p_num-1):
#            for j in range(i+1,p_num):
#                if i!=0 and j!=1:
#                    d=dist(p[i],p[j])
#                    if d<d_min:
#                        d_min=d
#                        p1,p2=p[i],p[j]
#        return p1,p2,d_min
    
def v1_brute(sort_x_p):
    p=copy.deepcopy(sort_x_p)
    p_num=len(sort_x_p)
    print('brute=',p)
    if len(sort_x_p)==1:
        return sort_x_p[0][0],sort_x_p[0][1],None
    else:
        tarp1=p[0]
        tarp2=p[1]
        d_min=dist(p[0],p[1])
        for i in range(p_num-1):
            for j in range(i+1,p_num):
                if i!=j:
                    p1=p[i]
                    p2=p[j]
                    d=dist(p1,p2)
                    if d<d_min:
                        d_min=d
                        tarp1=p1
                        tarp2=p2
        return tarp1,tarp2,d_min

####------version 1-------------------------
def v2_closest_point(arr):
#    print("total =",arr)
    p_num=len(arr)
    if p_num<=1:
        return None,arr[0][0],arr[0][1]
    elif p_num<4:
        tarp1=arr[0]
        tarp2=arr[1]
        d_min=dist(arr[0],arr[1])
        for i in range(p_num-1):
            for j in range(i+1,p_num):
                if i!=j:
                    p1=arr[i]
                    p2=arr[j]
                    d=dist(p1,p2)
                    if d<d_min:
                        d_min=d
                        tarp1=p1
                        tarp2=p2
#        print("d_min = ",d_min)
        return d_min,tarp1,tarp2
    else:
        pass
    mid=p_num//2
    
    if p_num%2==1:
        mid_line=arr[mid][0]
    else:
        mid_line=(arr[mid][0]+arr[mid+1][0])/2
        
    LP=arr[:mid]
    RP=arr[mid:]
    d_L,Lp1,Lp2=v2_closest_point(LP)
    d_R,Rp1,Rp2=v2_closest_point(RP)
#    print("LP = ",LP)
#    print("RP = ",  RP)
    arr=sorted(arr, key=lambda x:x[1])
    mid_area=[]
    for i in range(len(arr)):
        if arr[i][0]>=mid_line-min(d_L,d_R) and arr[i][0]<=mid_line+min(d_L,d_R):
            mid_area=mid_area+[arr[i]]
#    print("mid area = ",mid_area)
#    print("arr = ",arr)
    
    if d_L<d_R:
        d_minimum=d_L
        target_p1=Lp1
        target_p2=Lp2
    else:
        d_minimum=d_R
        target_p1=Rp1
        target_p2=Rp2
    
    for i in range(len(mid_area)):
        k=1
#        print("d_minimum = ",d_minimum)
        while ((i+k)<len(mid_area)) and (mid_area[i+k][1]<(mid_area[i][1]+d_minimum)):
            d_minimum=min(d_minimum,dist(mid_area[i+k],mid_area[i]))
            if d_minimum==dist(mid_area[i+k],mid_area[i]):
                target_p1=mid_area[i]
                target_p2=mid_area[i+k]           
            k=k+1
#            print("k=" ,k)
#    print("d_minimum = ",d_minimum)
#    print("target p1=",target_p1)
#    print("target p2=",target_p2)
    return d_minimum,target_p1,target_p2


###-----------case generation-------------------------------------
def test_case(length: int = 20):
    lst1 = [random.randint(0, 10**1)/10.000 for i in range(length)]
    lst2 = [random.randint(0, 10**1)/10.000 for i in range(length)]
    return lst1, lst2    

def gen(lst1,lst2):
    arr=[]
    for i in range(len(lst1)):
        arr+=[(lst1[i],lst2[i])]
    return arr

#--------using random number-----------------


file_path="D:/liang/CSE417/HW4/testcase/points-test2.txt"
file = open(file_path,'r')                        # open the test file
listoftext=file.read().split(' ')   
print(listoftext)
print(type(listoftext))
print(len(listoftext))
liststr=[]
for i in range(len(listoftext)):                # only n-1 line I need to read because the first line in the test file only contains number of node                
                              # start to read from the second line
    liststr=liststr+listoftext[i].split()
    print(listoftext[i])                     # read, split the strings in line and store into a list
print(liststr)
listoffloat=[float(i) for i in liststr]
print(listoffloat)
array=[]
    
for i in range(int((len(listoffloat))/2)):                  # by read two numbers every time so I only need to read n/2 times to get all edges
    i=i*2                                         # even number
    j=i+1                                         # odd number
    L=listoffloat[i]                                        # assign integer of index of even number to L 
    R=listoffloat[j]                                        # assign integer of index of odd number to R 
    array=array+[(L,R)]
print(array)
print(len(array))

#-------running test---------------
   
n=[]
m=[]

array_x=sorted(array, key=lambda x: x[0])
array_y=sorted(array, key=lambda x: x[1])

v3_start=time.clock()
v3_input_size=len(array)
#v3_start_time=time.time()
p3,q3,d3=v3_closest_pair(array_x,array_y)
v3_end=time.clock()
v3_runtime=v3_end-v3_start
#v3_runtime=time.time()-v3_start_time


v2_input_size=len(array_x)
#v2_start_time=time.time()
v2_start=time.clock()
d2,p2,q2=v2_closest_point(array_x)
v2_end=time.clock()
v2_runtime=v2_end-v2_start
#v2_runtime=time.time()-v2_start_time


v1_input_size=len(array_x)    
#v1_start_time=time.time()
v1_start=time.clock()
p1,q1,d1=v1_brute(array_x)
v1_end=time.clock()
v1_runtime=v1_end-v1_start
#v1_runtime=time.time()-v1_start_time




outFile = open('D:/liang/CSE417/HW4/testcase/testout.txt','w')
if len(array)==1:
    
    outFile.write("Version 1,%d,%.2f,%.2f,infinity,%.8f\n" %(v1_input_size,p1,q1,v1_runtime))
    outFile.write("Version 2,%d,%.2f,%.2f,infinity,%.8f\n" %(v2_input_size,p2,q2,v2_runtime))
    outFile.write("Version 3,%d,%.2f,%.2f,infinity,%.8f" %(v3_input_size,p3,q3,v3_runtime))
else:
    outFile.write("Version 1,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.8f\n" %(v1_input_size,p1[0],p1[1],q1[0],q1[1],d1,v1_runtime))
    outFile.write("Version 2,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.8f\n" %(v2_input_size,p2[0],p2[1],q2[0],q2[1],d2,v2_runtime))
    outFile.write("Version 3,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.8f" %(v3_input_size,p3[0],p3[1],q3[0],q3[1],d3,v3_runtime))
outFile.close()          

#outFile = open('D:/liang/CSE417/HW4/testcase/testout.txt','w') 
#outFile.write("Version 1,%d,%f,%f,%f,%f,%f,%f" %(v1_input_size,p1[0],p1[1],q1[0],q1[1],d1,v1_runtime))
#outFile.write("Version 2,%d,%f,%f,%f,%f,%f,%f" %(v2_input_size,p2[0],p2[1],q2[0],q2[1],d1,v2_runtime))
#outFile.write("Version 3,%d,%f,%f,%f,%f,%f,%f" %(v3_input_size,p3[0],p3[1],q3[0],q3[1],d1,v3_runtime))
#outFile.close()
#          
#          
#for i in range(10,100):
#    j=10*i
#    n+=[j]
#    lst1,lst2=test_case(j)
#    array=gen(lst1,lst2)
#    print("array=",array)
#    print("   ")
#    array_x=sorted(array, key=lambda x: x[0])
#    array_y=sorted(array, key=lambda x: x[1])
#
#    v3_start_time=time.time()
#    print("v3_answer:",v3_closest_pair(array_x,array_y))
#    v3_runtime=time.time()-v3_start_time
#    print("v3 runtime=",v3_runtime)
#    v3_time+=[v3_runtime]
#    
#    v2_start_time=time.time()
#    print("v2_answer:",v2_closest_point(array_x))
#    v2_runtime=time.time()-v2_start_time
#    print("v2 runtime=",v2_runtime)
#    v2_time+=[v2_runtime]
#    
#    v1_start_time=time.time()
#    print("v1_answer:",v1_brute(array_x)) 
#    v1_runtime=time.time()-v1_start_time
#    print("v1 runtime=",v1_runtime)
#    v1_time+=[v1_runtime]
#
#m=copy.deepcopy(n)
#    #print("good, this works!!!!!")
#
#for i in range(1,10000):
#    k=1000*i
#    m+=[k]
#    lst1,lst2=test_case(j)
#    array=gen(lst1,lst2)
#    print("array=",array)
#    print("   ")
#    array_x=sorted(array, key=lambda x: x[0])
#    array_y=sorted(array, key=lambda x: x[1])
#
#    v3_start_time=time.time()
#    print("v3_answer:",v3_closest_pair(array_x,array_y))
#    v3_runtime=time.time()-v3_start_time
#    print("v3 runtime=",v3_runtime)
#    v3_time+=[v3_runtime]
#    
#    v2_start_time=time.time()
#    print("v2_answer:",v2_closest_point(array_x))
#    v2_runtime=time.time()-v2_start_time
#    print("v2 runtime=",v2_runtime)
#    v2_time+=[v2_runtime]
#
#n=np.log10(n)
#m=np.log10(m)
#
#plt.figure()
#plt.plot(n,v1_time,'ro',label='v1')
#plt.plot(m,v2_time,'b',label='v2')
#plt.plot(m,v3_time,'*',label='v3')
#plt.ylabel("running time (s)")
#plt.xlabel("input size (log10(n))")
#plt.legend(loc='upper left')
#
##plt.figsize(100,100)
#plt.savefig('D:/liang/CSE417/HW3/HW3_2.png')
#plt.show()