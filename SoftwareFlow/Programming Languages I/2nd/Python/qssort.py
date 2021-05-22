import sys

with open(sys.argv[1]) as f:
    N = [int(x) for x in next(f).split()] 
    N = N[0]

    queue = [int(x) for x in next(f).split()]  

def BFS(queue, N):
    def Q(queue, stack, path):  
        newStack = stack
        newStack.append(queue[0])

        return queue[1:] , newStack, path + 'Q'

    def S(queue,stack, path):  
        queue2 = queue
        queue2.append(stack[-1])
        
        return queue2, stack[:-1], path + 'S'

    def isIncreasing(L):
        return all(x<=y for x, y in zip(L, L[1:])) 

    def foundIt(queue):
        return isIncreasing(queue) and len(queue) == N

    def solver(queue, N):
        path = '' 
        states = []
        states.append([queue, [], ''])
 
        while True: 
            newStates = []
            for queue, stack, path in states:  
                if foundIt(queue):
                    if path == '':
                        path = 'empty'
                    return path

                # print("Standard print: ", queue, stack, path)
                if not stack:  
                    tempQ = Q(queue,stack,path) 
                    newStates.append([tempQ[0],tempQ[1],tempQ[2]])
                elif not queue: 
                    tempS = S(queue,stack,path)
                    newStates.append([tempS[0],tempS[1],tempS[2]])
                else: 
                    queueQ, stackQ, pathQ = Q(queue, stack, path) 
                    queueS, stackS, pathS = S(queue, stack[:-1], path) # GIA KAPOIO LOGO VAZI 1 STOIXEIO STO TELOS TOU STACK ELEOSS
                    
                    newStates.append([queueQ, stackQ, pathQ ])
                    newStates.append([queueS, stackS, pathS]) 
            
            states = newStates 

    return solver(queue, N)        
 
print(BFS(queue, N)) 