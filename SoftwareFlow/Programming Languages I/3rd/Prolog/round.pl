
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
     
   
solver(_, N, N,_, A, B, C):- C = (A,B), !.
solver([(P,C)|T], Count, N, K, Ans_Sum, Ans_Pos, Res):-  
    runner(T, 0, (P,C), 0, 0, 0, (R,Last), K),
    write(R), write(' ') , write(Last), write('\n'),
    LastPos is mod(Last, K),
    write(R), write(' ') , write(LastPos), write('\n'),
    S is P + N,
    append(T,[(S,C)], T1), !,  
    C1 is Count + 1, 
    (  
        R =< Ans_Sum -> (
            LastPos =:= Ans_Pos -> ( 
                write(R), write(' LastPos: ') , write(LastPos), write(' AnsPos: '), write(Ans_Pos), write('\n'),
                solver(T1, C1, N, K, R, min(LastPos,Ans_Pos), Res)
            );
                write(R), write(' LastPos: ') , write(LastPos), write(' AnsPos: '), write(Ans_Pos), write('\n'), 
            solver(T1, C1, N, K, R, LastPos, Res)  
        );
        solver(T1, C1, N, K, Ans_Sum, Ans_Pos, Res)
    ).


% if (s.count == -1 || s.count >= tempSol.count) { 
%         		if (tempSol.count == s.count) {
%         			if (s.pos >= tempSol.pos) {
%         				s.pos = tempSol.pos; 
%         			}	
%         		}
% 				else {
% 					s.count = tempSol.count;
% 					s.pos = tempSol.pos;
% 				}        		
        		
%         	}  
round(File, M, C):-
    read_input(File, N, K, Ar), 
    quick_sort2(Ar, Arr), !, 
    fix_list(Arr, [], New),
    solver(New, 0, N, K, 10000000,0 , (M, C)). 
