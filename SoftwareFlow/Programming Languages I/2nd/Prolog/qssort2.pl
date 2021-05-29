read_input(File, N, C) :-
    open(File, read, Stream),
    read_line(Stream, [N]),
    read_line(Stream, C).

read_line(Stream, L) :-
    read_line_to_codes(Stream, Line),
    atom_codes(Atom, Line),
    atomic_list_concat(Atoms, ' ', Atom),
    maplist(atom_number, Atoms, L).

% Fill a list to a open list F 
fill_array([], Q, F):- F = Q.
fill_array([H|T], Q, F):-
    add_queue(H, Q, Q1),
    fill_array(T, Q1, F).

% Is open list empty or not  
makeList(List - L2, L2, List).
isQueueEmpty(L):- makeList(L, [], L2), L2 == [].

enqueue_stack(E, A, [E | A ]).
dequeue_stack(E, [E | T], T).

add_queue( Item, Queue-[Item|Y], Queue-Y ).
remove_queue( [Item|Queue]-X, Item, Queue-X ). 
 
getString(Queue1, Stack, Ans):-
    makeList(Queue1, [], Queue),
    atomics_to_string(Queue, ',', S1 ),
    atomics_to_string(Stack, ',', S2),
    
    string_concat('', S1, S_a),
    string_concat(S_a, '|', S_a2),

    string_concat(S_a2, S2, Ans).

q(Start_queue, Stack, Path, Qt, Dict, Start_queue, Qt1, NewDict):-
    remove_queue(Start_queue, P1, NewQueue),
    enqueue_stack(P1, Stack, NewStack), !,
    getString(Start_queue, Stack, String),
    write("String: "),
    writeln(String),
    write("Lists: "),
    writeln()
 
    % \+ member(String, Dict), 
    % string_concat(Path, 'Q', C1), !, 

    % add_queue((NewQueue, NewStack, C1), Qt, Qt1), !,
    % add_queue(String, Dict, NewDict),!.



change_queue(Queue, Q1):-
    writeln("Change Queue"),
    add_queue(10, Queue, Q1),
    writeln(Q1),
    add_queue(15, Q1, Q2),
    writeln(Q2),
    add_queue(25, Q2, Q3),
    writeln(Q3),
    remove_queue(Q3, _, Q4),
    writeln(Q4),
    remove_queue(Q4,_,Q5),
    writeln(Q5),
    writeln("Change Queue over").

qssort(File, Ans):-
    set_prolog_stack(global, limit(100 000 000 000)),
    read_input(File, _, C),
    fill_array()
    Empty = S-S,
    add_queue(5, Empty, N),
    writeln(N),
    \+ isQueueEmpty(N),
    writeln(N),
    q(N, [], '', _, _, Old, _, _),
    writeln("After Q"), 
    writeln(Old),
    writeln(New).
    % change_queue(N,Q3),
    % writeln(N),
    % writeln(Q3).
    % add_queue(1, Q3,Q4),
    % writeln(Q4).
