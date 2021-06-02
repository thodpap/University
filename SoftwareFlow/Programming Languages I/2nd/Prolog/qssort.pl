        
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

enqueue_stack(E, A, [E | A ]).
dequeue_stack(E, [E | T], T).

enqueue(A,B,C):- append(A,B,C).


dequeue(E, [E | T], T). 
dequeue(_, [A | T],  [A | T]).  

pop_back(E, [E], []).
pop_back(E, [H | T], [H | Tnew]):- pop_back(E, T, Tnew).

push(X,List,[X|List]). 
pop([X|List],X,List).

 
are_Elements_equal( [H | _ ], [ H | _ ]).

is_sorted([]).
is_sorted([_]).
is_sorted([X,Y|T]) :-
   X=<Y,
   is_sorted([Y|T]).

getString(Queue, Stack, Res):- 
    atomics_to_string(Queue, ',', S1 ),
    atomics_to_string(Stack, ',', S2),
    
    string_concat('', S1, S_a),
    string_concat(S_a, '|', S_a2),

    string_concat(S_a2, S2, Res).

q(Queue, Stack, C,Length, Dict, Q, NewDict, Q1):-
    dequeue(A, Queue, NewQueue), !,
    enqueue_stack(A, Stack, NewStack), !,
    % getString(NewQueue, NewStack, String), 
    
    % \+ member(String, Dict), 
        
    string_concat(C, 'Q', C1), !, 
    L is Length - 1,
    enqueue(Q, [(NewQueue, NewStack, C1, L)], Q1), !.
    % enqueue( Dict,[String], NewDict),!.

s(Queue, Stack, C, Length, Q, Q1):-
    dequeue_stack(B_pop, Stack, NewStack), !,
    enqueue(Queue, [B_pop], NewQueue), !, 
    % getString(NewQueue, NewStack, String),
    
    % \+ member(String, Dict), 
         
    L is Length + 1,
    string_concat(C, 'S', C1), !, 

    enqueue(Q, [(NewQueue, NewStack, C1, L)], Q1), !.
    % enqueue( Dict,[String], NewDict),!.
   
solver([(A,B,C, Length)| Q1], Goal, Res, N):-  

    Length = N,A = Goal -> (
        C = "" -> string_concat('empty', '' , Res);
        ( 
            string_concat(C, '', Res)
        )
    ); 
    (
        A == [] -> 
        ( 
            s(A,B,C,Length, Dict,Q1, D1,Q2), % -> solver(Q2, Goal, D1, Res, N);
            solver(Q1,Goal, Dict, Res, N)
        );   
        B == [] -> 
        (   
            q(A,B,C,Length, Dict, Q1, D1, Q2), % -> solver(Q2, Goal, D1, Res, N);
            solver(Q1, Goal, Dict, Res, N)
        );  
        are_Elements_equal(A,B) ->
        (
            q(A,B,C,Length, Dict, Q1, D1, Q2),
            s(A,B,C, Length, D1, Q2, Q3),
            solver(Q3, Goal, D2, Res, N)
        );
        s(A,B,C,Length, Dict, Q1, D1, Q2),
        solver(Q2, Goal, D1, Res, N)

        % q(A,B,C,Length, Dict, Q1, D1, Q2) -> 
        % ( 
        %     are_Elements_equal(A,B) -> solver(Q2, Goal, D1, Res, N);
        %     (
        %         s(A,B,C,Length, D1,Q2, D2,Q3) -> solver(Q3, Goal, D2, Res, N); 
        %         solver(Q2, Goal, D1, Res, N)
        %     )
        % );  
        % s(A,B,C,Length, Dict,Q1, D2,Q2) -> solver(Q2, Goal, D2, Res, N);
        % solver(Q1,Goal, Dict, Res, N)
    ). 


quick_sort2(List,Sorted):-q_sort(List,[],Sorted).
q_sort([],Acc,Acc).
q_sort([H|T],Acc,Sorted):-
    pivoting(H,T,L1,L2),
    q_sort(L1,Acc,Sorted1),q_sort(L2,[H|Sorted1],Sorted).
   
pivoting(_,[],[],[]).
pivoting(H,[X|T],[X|L],G):-X>=H,pivoting(H,T,L,G).
pivoting(H,[X|T],L,[X|G]):-X<H,pivoting(H,T,L,G).


qssort(File, Ans):-
    set_prolog_stack(global, limit(100 000 000 000)), 
    read_input(File, N, C), 
    quick_sort2(C,C1),  
    enqueue([(C,[], "", N)], [], Q1), !,   
    % getString(C,[], P),
    enqueue([P], [], D),  
    solver(Q1, C1, D, Ans, N), !.  