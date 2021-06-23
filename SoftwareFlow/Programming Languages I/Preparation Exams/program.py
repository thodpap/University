def count_substr(S, K):
    if K >= len(S):
        return 1

    dictionary = dict()
    dictionary[S[0:K]] = 1 
    for i in range(len(S) - K + 1):
        if S[i:i+K] in dictionary:
            continue
        dictionary[S[i:i+K]] = 1
    
    print(dictionary)
    return len(dictionary)

a = b =  1
c = [b]
def f(x):
    print(x)
    a = 3
    x = 2
    print(x)

def q1():
    f(a)
    print(a)

print(count_substr("helloworld", 3))
print(count_substr("banana", 2)) 
q1()