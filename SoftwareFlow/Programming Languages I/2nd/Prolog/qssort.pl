read_input(File, N, C) :-
    open(File, read, Stream),
    read_line(Stream, [N]),
    read_line(Stream, C).

read_line(Stream, L) :-
    read_line_to_codes(Stream, Line),
    atom_codes(Atom, Line),
    atomic_list_concat(Atoms, ' ', Atom),
    maplist(atom_number, Atoms, L).

empty([]).

enqueue(E, [], [E]).
enqueue(E, [H | T], [H | Tnew]):- enqueue(E,T,Tnew).


dequeue(E, [E | T], T). 
dequeue(_, [A | T],  [A | T]).  

pop_back(E, [E], []).
pop_back(E, [H | T], [H | Tnew]):- pop_back(E, T, Tnew).

is_sorted([]).
is_sorted([_]).
is_sorted([X,Y|T]) :-
   X=<Y,
   is_sorted([Y|T]).


solver([(Goal, _, _)], Goal, Res):- string_concat('', 'empty', Res). % Is already sorted 
solver([(Goal,_,S)| _], Goal, Res):- string_concat(S, '', Res).      % Found solution
solver(Queue, Goal, Res):-
    dequeue(E, Queue, Q1), !, 
    E = (A,B,C), 
    A == [] -> 
        % S
        pop_back(B_pop, B, B_popArr), !,
        enqueue(B_pop, A, A_en), !,
        string_concat(C, 'S', C1), !,
        enqueue((A_en, B_popArr, C1), Q1, Q2), !,
        solver(Q2, Goal, Res);
    
    dequeue((A,B,C), Queue, Q1),
    B == [] -> 
        % Q
        dequeue(A_pop, A, A_de), !,
        enqueue(A_pop, B, B_en), !,
        string_concat(C, 'Q', C1), !,
        enqueue((A_de, B_en, C1), Q1, Q2), !,
        solver(Q2, Goal, Res); 
     
    dequeue((A,B,C), Queue, Q1), !,
    % Q
    dequeue(A_pop, A, A_de), !,
    enqueue(A_pop, B, B_en), !,
    string_concat(C, 'Q', C1), !,

    enqueue((A_de, B_en, C1), Q1, Q2), !,


    % S
    pop_back(B_pop, B, B_popArr), !,
    enqueue(B_pop, A, A_en), !, 
    
    string_concat(C, 'S', C2), !,
    enqueue((A_en, B_popArr, C2), Q2, Q3), !, 
    solver(Q3, Goal, Res).  

quick_sort2(List,Sorted):-q_sort(List,[],Sorted).
q_sort([],Acc,Acc).
q_sort([H|T],Acc,Sorted):-
	pivoting(H,T,L1,L2),
	q_sort(L1,Acc,Sorted1),q_sort(L2,[H|Sorted1],Sorted).
   
pivoting(_,[],[],[]).
pivoting(H,[X|T],[X|L],G):-X>=H,pivoting(H,T,L,G).
pivoting(H,[X|T],L,[X|G]):-X<H,pivoting(H,T,L,G).


qssort(File, Ans):-
    read_input(File, _, C),
    empty(Q), 
    quick_sort2(C,C1),  
    enqueue( (C,[], ""), Q, Q1), !, 
    solver(Q1, C1, Ans), !. 