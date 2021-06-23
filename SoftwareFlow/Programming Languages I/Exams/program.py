def sliding(list, K):
    sums = dict()
 
    sum = 0
    for i in range(K):
        sum += list[i]
    sums[sum]= 1

    for i in range(K, len(list)):
        sum += list[i] - list[i - K]
        if sum in sums:
            sums[sum] += 1
        else:
            sums[sum] = 1
    ans = -1
    max_sum = 0
    for a in sums:
        if sums[a] > ans:
            ans = sums[a]
            max_sum = a
        elif sums[a] == ans:
            if max_sum < a: 
                ans = sums[a]
                max_sum = a

    print(max_sum, ans)


sliding([1,4,2,3,2,1,3,4,2],4)
sliding([1, 4, 2, 3, 2, 1, 3, 4, 2], 3)