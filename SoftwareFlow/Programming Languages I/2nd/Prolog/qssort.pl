
          
read_input(File, N, C) :-
    open(File, read, Stream),
    read_line(Stream, [N]),
    read_line(Stream, C).

read_line(Stream, L) :-
    read_line_to_codes(Stream, Line),
    atom_codes(Atom, Line),
    atomic_list_concat(Atoms, ' ', Atom),
    maplist(atom_number, Atoms, L).

fill_array([], Q, F):- F = Q.
fill_array([H|T], Q, F):-
    add_queue(H, Q, Q1),
    fill_array(T, Q1, F).

quick_sort2(List,Sorted):-q_sort(List,[],Sorted).
q_sort([],Acc,Acc).
q_sort([H|T],Acc,Sorted):-
    pivoting(H,T,L1,L2),
    q_sort(L1,Acc,Sorted1),q_sort(L2,[H|Sorted1],Sorted).
   
pivoting(_,[],[],[]).
pivoting(H,[X|T],[X|L],G):-X>=H,pivoting(H,T,L,G).
pivoting(H,[X|T],L,[X|G]):-X<H,pivoting(H,T,L,G).

init_queue(U-U). 
empty([]).

enqueue_stack(E, A, [E | A ]).
dequeue_stack(E, [E | T], T).

add_queue( Item, Queue-[Item|Y], Queue-Y ).
remove_queue( [Item|Queue]-X, Item, Queue-X ). 

isEmpty([]).

getString(Queue, Stack, Res):- 
    atomics_to_string(Queue, ',', S1 ),
    atomics_to_string(Stack, ',', S2),
    
    string_concat('', S1, S_a),
    string_concat(S_a, '|', S_a2),

    string_concat(S_a2, S2, Res).

q(Queue, Stack, C, Dict, Q, NewDict, Q1):-
    writeln("Q before print"), writeln(Queue), writeln(Stack), writeln(C), writeln(Dict), writeln(Q), writeln("Q after print").
    % remove_queue(A, Queue, NewQueue), !,
    % enqueue_stack(A, Stack, NewStack), !,
    % writeln(NewStack), writeln(NewQueue),
    % writeln("Reach here?"),
    % getString(NewQueue - [], NewStack - [], String), 
    % writeln("Q "),
    % \+ member(String, Dict), 
    % string_concat(C, 'Q', C1), !, 

    % add_queue((NewQueue, NewStack, C1), Q, Q1), !,
    % add_queue(String, Dict, NewDict),!.

s(Queue, Stack, C, Dict, Q, NewDict, Q1):-
    writeln("Q before print"), writeln(Queue), writeln(Stack), writeln(C), writeln(Dict), writeln(Q), writeln("Q after print").
    % dequeue_stack(B_pop, Stack, NewStack), !,
    % add_queue(B_pop, Queue, NewQueue), !, 
    % getString(NewQueue, NewStack, String),
    
    % \+ member(String, Dict), 
         
    % string_concat(C, 'S', C1), !, 

    % add_queue((NewQueue, NewStack, C1), Q, Q1), !,
    % add_queue(String, Dict, NewDict),!.

solver([(Goal, _, _)], Goal, _, Res):- string_concat('empty', '' , Res). % Is already sorted 
solver([(Goal,_,S)| _], Goal,_, Res):- string_concat(S, '', Res).      % Found solution
solver(Q, Goal, Dict, Res):-   
    remove_queue(Q, (A,B,C), Q1),  
    writeln(A), 
    A == U - U -> 
    ( 
        % remove_queue(Q, (_,_,_), Q1),  
        s(A,B,C,Dict,Q1, D1,Q2) -> solver(Q2, Goal, D1, Res);
        solver(Q1,Goal, Dict, Res)
    );    
    remove_queue(Q, (A,B,C), Q1),  
    B ==  U - U -> 
    (   
        writeln("Before"),
        q(A,B,C,Dict, Q1, D1, Q2) -> solver(Q2, Goal, D1, Res);
        writeln("After"),
        solver(Q1, Goal, Dict, Res)
    );   
    remove_queue(Q, (A,B,C), Q1), 
    q(A,B,C,Dict, Q1, D1, Q2) -> 
    ( 
        s(A,B,C,D1,Q2, D2,Q3) -> solver(Q3, Goal, D2, Res); 
        solver(Q2,Goal, D1, Res)
    ),
    % remove_queue(Q, (A,B,C), Q1), 
    s(A,B,C,Dict,Q1, D2,Q2) -> solver(Q2, Goal, D2, Res);
    solver(Q1,Goal, Dict, Res). 



qssort(File, Ans):-
    set_prolog_stack(global, limit(100 000 000 000)),
    read_input(File, _, C),
    writeln(C), 
    fill_array(C, U-U, F),
    writeln(F),
    quick_sort2(C,C1), 
    Temp = Q-Q,
    add_queue((F,K-K, ""), Temp, Q1), !,
    writeln(Q1),
    

    
    
    % getString(C,[], P),
    % empty(Dict),
    % enqueue(P, Dict, D), 
    % writeln(D),
    % writeln("Before i close my eyes"),
    % solver(Q1, C1, D, Ans), !.      