difference_append2(_, L2, L2). 
difference_append3(List-L2, L2).
difference_append4(List - L2, L2, List).
difference_append5(List - Hole, L1 - _, List):- Hole = L1.
difference_append6(List - L1, L1 - Hole2, List - Hole2).

add_queue( Item, Queue-[Item|Y], Queue-Y ).
remove_queue( [Item|Queue]-X, Item, Queue-X ).

fun():-
    % Test 1
    % List = [a,b,c|X], 
    % X = [d,e,f],
    % writeln(List).  

    % Test2
    % List = [a,b,c|X],
    % difference_append2(List, X, [d,e,f]),
    % writeln(List).

    % Test 3
    % List = [d,e,f|Hole] - Hole,
    % difference_append3(List,[a,b,c]),
    % writeln(List). 
    
    % Test 4
    % List = [a,b,c|H] - H, 
    % difference_append4(List,[d,e,f],Ans),
    % writeln(List),
    % writeln(Ans).

    % Test 5
    % List = [a,b,c|H] - H, 
    % difference_append5(List, [d,e,f|H2] - H2, Ans),
    % writeln(List),
    % writeln(Ans).

    % Test 6 
    List = [a,b,c|H] - H,  
    difference_append6(List, [d,e,f|Hole2] - Hole2, Ans),
    writeln(List), 
    writeln(Ans).

    % My example, take a random list make it differences list and then append one number to end
    % List = [1,2,3|X] - X,
    % writeln(List),
    % difference_append6(List, [5 | Z]- Z, Ans),
    % writeln(List),
    % writeln(Ans).
    % add_queue(10, List - X, L3),
    % add_queue(15, L3, L1), 
    % writeln(L4).
    % remove_queue(L1, I, L2),
    % % difference_append6(List,[4|H] - H, L2), 
    % writeln(L2).