import sys

with open(sys.argv[1]) as f:
    M, N = [int(x) for x in next(f).split()] # read first line

    arr = [int(x) for x in next(f).split()] 

prefix = []
prefix.append(0)

for i, a in enumerate(arr):
    prefix.append(prefix[-1] + a + N)

maxi = []
maxi.append((0, 0) )
max_so_far = 0

for i, pre in enumerate(prefix):
    if pre > max_so_far:
        max_so_far = pre
        maxi.append( (max_so_far, i) )

mini = []
mini.append((prefix[-1], M) )
min_so_far = prefix[-1]

for i, pre in reversed(list(enumerate(prefix))):
    if pre < min_so_far:
        min_so_far = pre
        mini.append( (min_so_far, i) )

mini = list(reversed(mini))

i, j, ans = 0, 0, 0
while i < len(maxi) and j < len(mini):
    if mini[j][0] <= maxi[i][0]:
        while j + 1 < len(mini) and  mini[j+1][0] <= maxi[i][0]:
            j += 1
        ans = max(ans, mini[j][1] - maxi[i][1])
        j += 1
        i += 1
    elif maxi[i][1] < mini[j][1] - 1:
        i += 1
    else:
        j += 1

print(ans)