read_input(File, N, C) :-
    open(File, read, Stream),
    read_line(Stream, [N]),
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

enqueue_stack(E, A, [E | A ]).
dequeue_stack(E, [E | T], T).

enqueue(A,B,C):- append(A,B,C).


dequeue(E, [E | T], T). 
dequeue(_, [A | T],  [A | T]).  

pop_back(E, [E], []).
pop_back(E, [H | T], [H | Tnew]):- pop_back(E, T, Tnew).

push(X,List,[X|List]). 
pop([X|List],X,List).

initial(State, State).


q_fun( ([A|B], C), (B, [A|C])).
s_fun( (A, [B|C]), (D, C) ):- append(A, [B], D).


are_Elements_equal( [], [ _ | _ ]):- false, !.
are_Elements_equal( [H | _ ], [ H | _ ]).

move((Q,S,C_q, C_s), 'Q', (Q1,S1,C_q1, C_s)):-
    Q \= [],
    C_q1 is C_q + 1,
    q_fun( (Q,S), (Q1,S1) ). 
move((Q,S,C_q, C_s), 'S', (Q1,S1,C_q, C_s1)):-
    S \= [],
    \+ are_Elements_equal(Q,S),
    C_s1 is C_s + 1,
    s_fun( (Q,S), (Q1,S1) ).

check_lengths((_,_, C_q, C_s), L):- C_q =< L/2, C_s =< L/2.

solver((Final, [], C, C), (Final, []), [], _).
solver(Conf, Final, [Move | Moves], Length_String):-
    check_lengths(Conf, Length_String),
    move(Conf, Move, Conf1),
    solver(Conf1, Final, Moves, Length_String).

setAns(String, Ans):-
    String = "" -> string_concat('empty', '' , Ans); 
    string_concat(String, '' , Ans).

qssort(File, Ans):-
    set_prolog_stack(global, limit(100 000 000 000)), 
    read_input(File, _, C), 
    quick_sort2(C,C1),
    initial((C, [],0,0),IntialConf), 
    initial((C1,[]), Final),
    length(Moves, Length_String),
    solver(IntialConf, Final, Moves, Length_String), !, 
    atomics_to_string(Moves, '', String ),
    setAns(String, Ans).