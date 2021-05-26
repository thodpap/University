
read_input(File, M, N, C) :-
    open(File, read, Stream),
    read_line(Stream, [M, N]),
    read_line(Stream, C).

read_line(Stream, L) :-
    read_line_to_codes(Stream, Line),
    atom_codes(Atom, Line),
    atomic_list_concat(Atoms, ' ', Atom),
    maplist(atom_number, Atoms, L).


sums(L, S, N) :- sumrunner(L, S, N, 0, 0).
sumrunner([], [], _, _, _).
sumrunner([A|B], [(E,Pos)|D], N, TOTAL, Pos) :- E is TOTAL + A + N, Pos1 is Pos + 1, sumrunner(B, D, N, E, Pos1).

max_from_left([], _, _).
max_from_left([H|B], C, Total_Max):-
(
  H = (A,_), 
  A =< Total_Max->
    max_from_left(B, C, Total_Max)
  ; H = (A,_),  
  C = [H | D],
  max_from_left(B,D, A)
).
 
min_from_right([],_,_).
min_from_right([H|B], C, Total_Min):-
(
  H = (A,_),
  A >= Total_Min -> 
    min_from_right(B,C, Total_Min)
  ; H = (A,_),
  C = [H | D],
  min_from_right(B,D,A)
).


len_tuple([], Pos1, Pos):-Pos1 is Pos.
len_tuple([_|Tail], Ans, Pos):-
  Ans1 is Pos + 1,
  len_tuple(Tail, Ans, Ans1).
 

solver(_, [], Ans, F):- F is Ans, !.
solver([], _, Ans, F):- F is Ans, !.
solver([(Head_max,Pos_max)|Tail_max], [(Head_min, Pos_min)|Tail_min], Ans, F):-
  (
    Head_min =< Head_max ->
      (
        Tail_min = [(H1, _)|_],
        len_tuple(Tail_min, G, 0),
        (G=\=0, H1 =< Head_max) ->
          solver([(Head_max,Pos_max)|Tail_max], Tail_min, Ans, F);
        Diff is Pos_min - Pos_max,
        Ans1 is max(Diff, Ans),
        solver(Tail_max, Tail_min, Ans1, F)
      );
    Head_min > Head_max,
    (
      Pos_max < Pos_min - 1,
      solver(Tail_max, [(Head_min, Pos_min)|Tail_min], Ans, F);
      Pos_max >= Pos_min - 1,
        solver([(Head_max,Pos_max)|Tail_max], Tail_min, Ans, F)
    )
  ).
 
longest(File, Ans):-
   read_input(File, _, N, C),
   sums(C,S,N), 
   append([(0,-1)], S, S1), 
   max_from_left(S1, Max, -1),   
   reverse(S1, S2),
   S2 = [(A,_)|_], 
   Max_ is A + 1,
   min_from_right(S2, Min, Max_),
   reverse(Min, Min1), !,
   solver(Max, Min1, 0, Ans). 