
unique([]).
unique([Item | Rest]):-
    \+ member(Item, Rest), unique(Rest).


n(_,_,_).

find_max(n(A,B,C), Res):- integer(A),integer(B),integer(C), M1 is max(A,B), Res is max(M1,C).
find_max(n(A,B,C), Res):- integer(A), integer(B), M1 is max(A,B), find_max(C, M2), Res is max(M1,M2).
find_max(n(A,B,C), Res):- integer(A), integer(C),  M1 is max(A,C), find_max(B, M2), Res is max(M1,M2).
find_max(n(A,B,C), Res):- integer(B), integer(C),  M1 is max(B,C), find_max(A, M2), Res is max(M1,M2).

find_max(n(A,B,C), Res):- integer(A), find_max(B,M1), find_max(C,M2), M3 is max(M1,M2), Res is max(A,M3).
find_max(n(A,B,C), Res):- integer(B), find_max(A,M1), find_max(C,M2), M3 is max(M1,M2), Res is max(B,M3).
find_max(n(A,B,C), Res):- integer(C), find_max(A,M1), find_max(B,M2), M3 is max(M1,M2), Res is max(C,M3).
find_max(n(A,B,C), Res):- find_max(A,M1), find_max(B,M2), find_max(C,M3), M4 is max(M1,M2), Res is max(M4, M3).
 

maximize(n(A,B,C), MaxTree):-
    find_max(n(A,B,C), Max),
    updateTree(n(A,B,C), MaxTree, Max).

updateTree(n(A,B,C), MaxTree, Max):- integer(A),integer(B),integer(C), MaxTree = n(Max,Max,Max).
updateTree(n(A,B,C), MaxTree, Max):- integer(A),integer(C), updateTree(B, T, Max), MaxTree = n(Max, T ,Max).
updateTree(n(A,B,C), MaxTree, Max):- integer(A),integer(B), updateTree(C, T, Max), MaxTree = n(Max, Max, T). 
updateTree(n(A,B,C), MaxTree, Max):- integer(C),integer(B), updateTree(A, T, Max), MaxTree = n(T, Max ,Max). 
updateTree(n(A,B,C), MaxTree, Max):- integer(A), updateTree(B,T1,Max), updateTree(C,T2,Max), MaxTree = n(Max,T1,T2).
updateTree(n(A,B,C), MaxTree, Max):- integer(B), updateTree(A,T1,Max), updateTree(C,T2,Max), MaxTree = n(T1,Max,T2).
updateTree(n(A,B,C), MaxTree, Max):- integer(C), updateTree(B,T1,Max), updateTree(A,T2,Max), MaxTree = n(T2,T1,Max).
updateTree(n(A,B,C), MaxTree, Max):- updateTree(A,T,Max), updateTree(B,T1,Max), updateTree(C,T2,Max), MaxTree = n(T,T1,T2).


is_odd_sum(n(A,B,C)):- integer(A),integer(B),integer(C), Sum is A + B + C, Sum mod 2 =:= 1.
 
unoddsum(n(A,B,C), Term):- integer(A),integer(B),integer(C), 
(
    is_odd_sum(n(A,B,C)) -> Term is 17;
    Term = n(A,B,C)
).
unoddsum(n(A,B,C), Term):- integer(A),integer(B), unoddsum(C, T1), 
(
    integer(T1), is_odd_sum(T1) ->  
        (
            is_odd_sum(n(A,B,17))-> Term is 17;
            Term = n(A,B,17)
        );
    Term = n(A,B,T1)
).
unoddsum(n(A,B,C), Term):- integer(A),integer(C), unoddsum(B, T1), 
(
    integer(T1), is_odd_sum(T1) ->  
        (
            is_odd_sum(n(A,17,C))-> Term is 17;
            Term = n(A,17,C)
        );
    Term = n(A,T1,C)
).
unoddsum(n(A,B,C), Term):- integer(B),integer(C), unoddsum(A, T1), 
(
    integer(T1), is_odd_sum(T1) ->  
        (
            is_odd_sum(n(17,B,C))-> Term is 17;
            Term = n(17,B,c)
        );
    Term = n(T1,B,C)
).

unoddsum(n(A,B,C), Term):- integer(A), unoddsum(B, T1), unoddsum(C,T2). % check for 17 solutions and decide 
unoddsum(n(A,B,C), Term):- integer(B), unoddsum(A, T1), unoddsum(C,T2), unoddsum(n(T1,B,T2) Term). % check for 17 solutions and decide 
unoddsum(n(A,B,C), Term):- integer(C), unoddsum(B, T2), unoddsum(A,T1), unoddsum(n(T1,T2,C) Term). % check for 17 solutions and decide 
unoddsum(n(A,B,C), Term):- unoddsum(A, T1), unoddsum(B,T2), unoddsum(C,T3), unoddsum(n(T1,T2,T3) Term). % check for 17 solutions and decide 



