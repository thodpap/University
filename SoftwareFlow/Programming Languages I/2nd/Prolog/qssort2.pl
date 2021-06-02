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

% Fill a list to a open list F 
fill_array([], Q, F):- F = Q.
fill_array([H|T], Q, F):-
    add_queue(H, Q, Q1),
    fill_array(T, Q1, F).

% Is open list empty or not  
makeList(List - _, List).
isQueueEmpty(L):- makeList(L - [], L2), L2 == [].

enqueue_stack(E, A, [E | A ]).
dequeue_stack(E, [E | T], T).

add_queue( Item, Queue-[Item|Y], Queue-Y ).
remove_queue( [Item|Queue]-X, Item, Queue-X ). 
 
getString(Queue, Stack, Ans):-
    % makeList(Queue1, [], Queue),
    atomics_to_string(Queue, ',', S1 ),
    atomics_to_string(Stack, ',', S2),
    
    string_concat('', S1, S_a),
    string_concat(S_a, '|', S_a2),

    string_concat(S_a2, S2, Ans).

areEqual(L1 - _, L1 - _).

q(Start_queue, Stack, Path, Qt, Start_queue, Qt1):- 
    writeln("Executing Q"),
    write("Qt: "), writeln(Qt),
    remove_queue(Start_queue, P1, NewQueue),
    write("New Queue"), writeln(NewQueue),
    enqueue_stack(P1, Stack, NewStack),
    write("New Stack"), writeln(NewStack),
    string_concat(Path, 'Q', C1),
    add_queue((NewQueue,NewStack,C1), Qt, Qt1),
    write("New Total Queue"), writeln(Qt1).

s(Start_queue, Stack, Path, Qt, Start_queue, Qt1):- 

    writeln("Executing S"),
    write("Start Queue: "), writeln(Start_queue),
    write("Stack: "), writeln(Stack),
    write("Qt: "), writeln(Qt),
    dequeue_stack(B_pop, Stack, NewStack), 
    write("New Stack"), writeln(NewStack),
    add_queue(B_pop, Start_queue, NewQueue), 
    write("New Queue"), writeln(NewQueue),
    string_concat(Path, 'S', C1),   
    add_queue((NewQueue,NewStack,C1), Qt, Qt1),
    writeln(Start_queue),
    write("New Total Queue"), writeln(Qt1).
 
solver(Q, Goal, Res):-   
    remove_queue(Q, (A,B,C), Q1), 
    writeln("Head in solver"), 
    writeln(A), writeln(B), writeln(C),
    writeln(Q1),
    areEqual(A - [], Goal - [])-> (
        C == '' -> string_concat('empty', '' , Res);
        string_concat(C, '', Res), false
    ); 

    remove_queue(Q, (A,B,C), Q1),   
    isQueueEmpty(A) -> 
    ( 
        % remove_queue(Q, (_,_,_), Q1),  
        s(A,B,C,Q1,_, Q2) -> solver(Q2, Goal, Res);
        solver(Q1,Goal, Res)
    );    
    remove_queue(Q, (A,B,C), Q1),  
    B == [] -> 
    (    
        q(A,B,C, Q1,_, Q2),
        solver(Q2, Goal, Res)
    );   
    remove_queue(Q, (A,B,C), Q1), 
    q(A,B,C, Q1, _ ,Q2),
    s(A,B,C,Q2,_,Q3),
    solver(Q3, Goal, Res).

qssort(File, Ans):-
    set_prolog_stack(global, limit(100 000 000 000)),
    read_input(File, _, C),
    fill_array(C, U-U, C1),
    write("C1: "), writeln(C1), 
    TQ1 = S-S,

    add_queue((C1,[],''), TQ1, Qt),
    quick_sort2(C,C2), 

    % add_queue(5, TQ1, Q),
    % write("Q: "), writeln(Q),


    % add_queue(15, Q, Q1),
    % write("Q: "), writeln(Q),
    % write("Q1: "), writeln(Q1),

    % remove_queue(Q1, Item, Q2),
    % write("Item: "), writeln(Item),
    % write("Q1: "), writeln(Q1),
    % write("Q2: "), writeln(Q2),

    % add_queue(25, Q2, Q3),
    % write("Q2: "), writeln(Q2),
    % write("Q3: "), writeln(Q3).
 

    \+ solver(Qt, C2, Ans),
    writeln(Ans). 