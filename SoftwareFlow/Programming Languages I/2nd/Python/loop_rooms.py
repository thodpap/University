import sys
import numpy as np 

#print(sys.getrecursionlimit())
sys.setrecursionlimit(6000)


visited = np.zeros((10000,10000))

with open(sys.argv[1]) as f:
    N, M = [int(x) for x in next(f).split()] # read first line

    arr = [ [x for x in line.split()] for line in f] 
arr = np.array(arr)
counter = 0
def dfs(): 
    def find_parents(i,j):
        global N
        global M
        global counter
        global visited
        global arr

        visited[i][j] = 1
        counter += 1
        
        if j >= 1 and visited[i][j - 1] == 0 and arr[i][0][j - 1] == "R":
            find_parents(i, j - 1)
        
        if j + 1 < M and visited[i][j + 1] == 0 and arr[i][0][j + 1] == "L":
            find_parents(i, j + 1)
        
        if i >= 1 and visited[i - 1][j] == 0 and arr[i - 1][0][j] == "D":
            find_parents(i - 1, j) 

        if i + 1 < N and visited[i + 1][j] == 0 and arr[i + 1][0][j] == "U":
            find_parents(i + 1,j)
   
    def searchHorizontal(p, char):
        global visited
        global arr
        global M
        for j in range(M):
                if arr[p][0][j] == char and visited[p][j] == 0:
                    find_parents(p, j)

    def searchVertical(q, char):
        global visited
        global arr
        global N
        for i in range(N):
                if arr[i][0][q] == char and visited[i][q] == 0:
                    find_parents(i, q)

       
    global N
    global M 
     
    searchHorizontal(0,'U')
    searchHorizontal(N-1,'D')
    
    searchVertical(0, 'L')
    searchVertical(M - 1, 'R')

dfs()
print( N * M - counter)
