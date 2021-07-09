
read_input(File, N,K, C) :-
    open(File, read, Stream),
    read_line(Stream, [N, K]),
    read_line(Stream, C).

read_line(Stream, L) :-
    read_line_to_codes(Stream, Line),
    atom_codes(Atom, Line),
    atomic_list_concat(Atoms, ' ', Atom),
    maplist(atom_number, Atoms, L).

quick_sort2(List,Sorted):-q_sort(List,[],Sorted).
q_sort([],Acc,Acc).
q_sort([H|T],Acc,Sorted):-
    pivoting(H,T,L1,L2),
    q_sort(L1,Acc,Sorted1),q_sort(L2,[H|Sorted1],Sorted).

pivoting(_,[],[],[]).
pivoting(H,[X|T],[X|L],G):-X>=H,pivoting(H,T,L,G).
pivoting(H,[X|T],L,[X|G]):-X<H,pivoting(H,T,L,G).

count_numbers([], _, C, Ans, Ret):- Ans is C, Ret = [], !.
count_numbers([A|B], A, C, Ans, Ret):- C1 is C + 1, count_numbers(B, A, C1, Ans, Ret),!.
count_numbers(H, _, C, Ans, Ret):- Ans is C, Ret = H. 

append_front(E, A, [E | A ]).

reverse([],Z,Z). 
reverse([H|T],Z,Acc) :- reverse(T,Z,[H|Acc]).

fix_list([], Ans,Ret):- reverse(Ans,Ret).
fix_list([H|T], Ans, Ret):-    
    count_numbers([H|T], H, 0, Sum, B), 
    append_front((H,Sum), Ans, A2),  
    fix_list(B, A2, Ret), !. 


runner([], _, (LastElement, _), Count, Neg, IndependentMoves, Res, K):-
    Neg > 0,
    Div is div(Neg, K),
    Mod is mod(Neg, K),
    (
        Mod > 1 -> (
            L is LastElement + Div + 1, 
            R is Count + K * (Div + 1) + Neg + IndependentMoves,
            Res = (R,L)
        );
        L is LastElement + Div, 
        R is Count + K * Div + Neg + IndependentMoves, 
        Res = (R,L)
    ).
runner([], _, (LastElement, _), Count, _, IndependentMoves, Res, _):-
    C is Count + IndependentMoves, 
    Res = (C, LastElement), !.

runner([(Pos, Sum)|B], Value, (Prev_pos, 1), Count, Neg, IndependentMoves, Res, K):-  
    N is Neg + Pos - Prev_pos,
    V is Value + 1,
    runner(B, V, (Pos, Sum), Count, N, IndependentMoves, Res, K),!.

runner([(Pos, Sum)|B], Value, (Prev_pos, 2),  Count, Neg, IndependentMoves, Res, K):-  
    I is IndependentMoves + Pos - Prev_pos,
    V is Value + 2,
    runner(B, V, (Pos, Sum),  Count, Neg, I, Res, K),!.

runner([(Pos, Sum)|B], Value, (Prev_pos, Prev_sum),  Count, Neg, IndependentMoves, Res, K):-  
    C is  Count + (Pos - Prev_pos) * Prev_sum,
    V is Value + Prev_sum,
    ( 
        C >= Neg -> C2 is C + Neg, N is 0, runner(B, V, (Pos, Sum),  C2, N, IndependentMoves, Res, K);
        Temp is C,
        C2 is C + Neg,
        N is Neg - Temp,
        runner(B, V, (Pos, Sum),  C2, N, IndependentMoves, Res, K)
    ), !.

find_ones([], _).
find_ones([(P,1)|T], Ones):- find_ones(T,O), Ones = [P | O].
find_ones([_|T], Ones):- find_ones(T,Ones).

help_solver(C1, Ind1, NegTotal1, Rest, LastOneTotal, I, N):- 
    C1 >= 2, 
    Rest1 is Rest + 1, 
    Rest1 >= LastOneTotal, 
    I is Ind1 + NegTotal1, 
    N is 0, !.
help_solver(C1, Ind1, _, Rest, LastOneTotal, I, N):- 
    C1 >= 2, 
    I is Ind1 + LastOneTotal, 
    N is LastOneTotal - Rest, !. 
help_solver(_, Ind1, NegTotal1, _, _, Ind1, NegTotal1).

find_solution(N, C, NegTotal, IndependentMovesTotal,MovesTotal,Count,Pos):-
    MovesTotal =:= 0,
    NegTotal =:= 0,
    Count is IndependentMovesTotal,
    Pos is C mod N, !.
find_solution(N, C, NegTotal, IndependentMovesTotal,MovesTotal,Count,Pos):-
    C1 is MovesTotal + IndependentMovesTotal,
    C1 >= NegTotal,
    MovesTotal > 0, 
    Count is MovesTotal + IndependentMovesTotal + NegTotal,
    Pos is C mod N, !.
find_solution(_, _, _, _,_,C,0):- C is 1000000000000000000000.
 

solver(N, LastOne, C1,C2,C3, Neg,I,M, C, AnsCount,AnsPos):-
    LastOneTotal is C - LastOne,
    NegTotal1 is C * C1 - Neg,
    Ind1 is C * C2 - I,
    MovesTotal is C * C3 - M,
    Rest is NegTotal1 - LastOneTotal,
    help_solver(C1, Ind1, NegTotal1, Rest, LastOneTotal, IndependentMovesTotal,NegTotal),
    find_solution(N, C, NegTotal, IndependentMovesTotal, MovesTotal,AnsCount,AnsPos).

first_traverse([],C1,C2,C3,N,I,M,  C1,C2,C3,N,I,M):- !.
first_traverse([(Pos,Value)|B],C1,C2,C3,N,I,M,  C1_n,C2_n,C3_n,N_n,I_n,M_n):-
    Value =:= 1,
    C1N is C1 + Value,
    N2 is N + Pos * Value,
    first_traverse(B, C1N,C2, C3,N2,I,M, C1_n,C2_n,C3_n,N_n,I_n,M_n), !.
first_traverse([(Pos,Value)|B],C1,C2,C3,N,I,M,  C1_n,C2_n,C3_n,N_n,I_n,M_n):-
    Value =:= 2,
    C2N is C2 + Value,
    Ind is I + Pos * Value,
    first_traverse(B, C1,C2N, C3,N,Ind,M, C1_n,C2_n,C3_n,N_n,I_n,M_n), !.
first_traverse([(Pos,Value)|B],C1,C2,C3,N,I,M,  C1_n,C2_n,C3_n,N_n,I_n,M_n):-
    Value > 2,
    C3N is C3 + Value,
    Moves is M + Pos * Value,
    first_traverse(B, C1,C2, C3N,N,I,Moves, C1_n,C2_n,C3_n,N_n,I_n,M_n), !.


decide_solution(Sol_count, _, New_count, New_pos, Final_count, Final_pos):-
    Sol_count > New_count,
    Final_count is New_count,
    Final_pos is New_pos.
decide_solution(Sol_count, Sol_pos, New_count, New_pos, Final_count, Final_pos):-
    Sol_count =:= New_count,
    (
        Sol_pos >= New_pos -> Final_count is Sol_count, Final_pos is New_pos;
        Final_count is Sol_count, Final_pos is Sol_pos
    ).
decide_solution(Sol_count, Sol_pos, New_count, _, Final_count, Final_pos):-
    Sol_count < New_count,
    Final_count is Sol_count,
    Final_pos is Sol_pos.

get_parameters(_, 0, Ones ,Ones, Neg,I,M, Neg,I,M).
get_parameters(N, 1, [_|T], T, Neg,I,M, N_n,I,M):- N_n is Neg + N.
get_parameters(N,2, Ones, Ones,Neg,I,M, Neg,I_n,M):- I_n is I + 2 * N.
get_parameters(N, El, Ones, Ones, Neg,I,M, Neg,I,M_n):- M_n is M + El * N.



traverse(N, _, _, Count, _,_,_, _, _,_, Temp_count, Temp_pos, Sol_count, Sol_pos):- 
    Count =:= 2*N,   
    Sol_count is Temp_count,
    Sol_pos is Temp_pos, !.
traverse(N, [], [H|T], Count, C1,C2,C3, Neg, I, Moves, Temp_count, Temp_pos, Sol_count, Sol_pos):-
    % Index is Count - N,
    solver(N, H, C1,C2,C3, Neg,I,Moves, Count, TempCount, TempPos), !,
    decide_solution(Temp_count, Temp_pos, TempCount, TempPos, Ans_count,Ans_pos), !,
    NewCount is Count + 1,
    traverse(N, [], [H|T], NewCount, C1,C2,C3, Neg, I, Moves, Ans_count, Ans_pos, Sol_count, Sol_pos), !. 
traverse(N, [(Pos,Value)|B], Ones, Count, C1,C2,C3, Neg, I, Moves, Temp_count, Temp_pos, Sol_count, Sol_pos):-
    Index is Count - N,
    Pos =:= Index,  
    get_parameters(N,Value, Ones, NewOnes, Neg,I,Moves, NegTotal, IndependentMovesTotal, MovesTotal), !,
    NewOnes = [LastOne | _],
    solver(N, LastOne, C1,C2,C3, NegTotal, IndependentMovesTotal, MovesTotal, Count, TempCount,TempPos), !,
    decide_solution(Temp_count, Temp_pos, TempCount, TempPos, Ans_count,Ans_pos), !,
    NewCount is Count + 1,
    traverse(N, B, NewOnes, NewCount, C1,C2,C3, NegTotal, IndependentMovesTotal, MovesTotal, Ans_count, Ans_pos, Sol_count, Sol_pos), !.
traverse(N, [(Pos,T)|B], Ones, Count, C1,C2,C3, Neg, I, Moves, Temp_count, Temp_pos, Sol_count, Sol_pos):-
    Index is Count - N,
    Pos \= Index, 
    get_parameters(N,0, Ones, NewOnes, Neg,I,Moves, NegTotal, IndependentMovesTotal, MovesTotal), !,
    NewOnes = [LastOne | _],
    solver(N, LastOne, C1,C2,C3, NegTotal, IndependentMovesTotal, MovesTotal, Count, TempCount,TempPos), !,
    decide_solution(Temp_count, Temp_pos, TempCount, TempPos, Ans_count,Ans_pos), !,
    NewCount is Count + 1,
    traverse(N, [(Pos,T)|B], NewOnes, NewCount, C1,C2,C3, NegTotal, IndependentMovesTotal, MovesTotal, Ans_count, Ans_pos, Sol_count, Sol_pos), !.




round(File,C,M):-
    read_input(File, N, _, Ar), 
    quick_sort2(Ar, Arr), !, 
    fix_list(Arr, [], New), 
    first_traverse(New ,0,0,0,0,0,0, C1,C2,C3, Neg,I,Moves),
    find_ones(New, On), !,   
    On = [F | _],
    F1 is F + N,
    append(On, [F1], Ones),
    solver(N, 0, C1,C2,C3,Neg,I,Moves, N-1, FirstC, FirstPos), !,
    traverse(N, New, Ones,N, C1,C2,C3,Neg, I , Moves, FirstC, FirstPos, C,M).