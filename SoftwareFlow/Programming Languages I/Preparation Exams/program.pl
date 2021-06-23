% First solution 
sum_runner([], 0).
sum_runner([H|T], Res):- sum_runner(T, Res1), Res is Res1 + H.

% tail recursive accumulator solution
sum(L, N):- sum(L,0,N).

sum([], N, N).
sum([H|T], A, N):-
    A1 is A + H,
    sum(T, A1, N).

n(_,_). 

diadiko(n(0,0), [0,0], []).
diadiko(n(0,1), [0], [1]).
diadiko(n(1,0), [0], [1]).
diadiko(n(1,1), [], [1,1]).
diadiko(n(T1,0), [0|A], B):- diadiko(T1, A, B).
diadiko(n(T1,1), A , [1|B]):- diadiko(T1, A, B).
diadiko(n(0, T1), [0|A], B):- diadiko(T1, A, B).
diadiko(n(1, T1), A , [1|B]):- diadiko(T1, A, B).
diadiko(n(T1,T2), Zeros, Ones):- 
    diadiko(T1, A, B),
    diadiko(T2, C,D),
    append(A, C, Zeros),
    append(B,D, Ones).

count_odd_parity(n(0,1), 1).
count_odd_parity(n(1,0), 1).
count_odd_parity(n(0,0), 0).
count_odd_parity(n(1,1), 0).
count_odd_parity(n(T1,0), Count):- count_odd_parity(T1, Count).
count_odd_parity(n(T1,1), Count):- count_odd_parity(T1, Count).
count_odd_parity(n(0,T1), Count):- count_odd_parity(T1, Count).
count_odd_parity(n(1,T1), Count):- count_odd_parity(T1, Count).
count_odd_parity(n(T1,T2), Count):- 
    count_odd_parity(T1,C1),
    count_odd_parity(T2,C2),
    Count is C1 + C2.
  
floor([], _, -1).
floor(node(X,L,R), K, F):-
(
    K =:= X -> F is X;
    X < K -> floor(R,K,F1), F is max(F1,X);
    floor(L,K,F)
).

p(17).
p(42).
p(7).
qa(X,Y):- p(X), p(Y), X >= Y.

incsubseq(L,K,S):-
    length(S, K),
    subseq(S, L),
    isIncreasing(S).

subseq([], _).
subseq([A | B], [A|D]):- subseq(B,D).
subseq([A | B], [ _ | D]):- subseq([A | B], D).

isIncreasing([]).
isIncreasing([_]).
isIncreasing([H1, H2|T]):- H1 =< H2, isIncreasing([H2 | T]).

is_heap(empty).
is_heap(node(X,L,R)):-
    is_heap(L, X),
    is_heap(R, X).

is_heap(empty, _).
is_heap(node(X,L,R), Value):-
    X >= Value,
    is_heap(L, X),
    is_heap(R, X).


middle([], []).
middle([A], [A]).
middle([A,B], [A,B]).
middle([A|B], [A, Mid, Right]):-
    append(In, [Right], B),
    In = [_|_],
    middle(In, Mid).

 
 permutation([],[]).
 permutation([X|Xs], Ys1) :- permutation(Xs,Ys), select(X,Ys1, Ys).

isPair([A,B|_], [C,D]):- (A =:= D, B =:= C), !.
isPair([_,B|T], [C,D]):- isPair([B|T], [C,D]), !.

countPairs(_, [], Count, Count).
countPairs(_, [_], Count, Count).
countPairs(A, [B,C|T], Count, Ans):-     
(
    isPair(A,[B,C]) -> C1 is 1 + Count, countPairs(A,[C|T], C1, Ans);
    countPairs(A,[C|T], Count, Ans)
).  

odd_permutation(X,Y):- 
    permutation(X,Y),
    countPairs(X, Y,0, C),
    C mod 2 =:= 1.
