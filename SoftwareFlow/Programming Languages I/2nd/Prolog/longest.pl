
read_input(File, M, N, C) :-
    open(File, read, Stream),
    read_line(Stream, [M, N]),
    read_line(Stream, C).

read_line(Stream, L) :-
    read_line_to_codes(Stream, Line),
    atom_codes(Atom, Line),
    atomic_list_concat(Atoms, ' ', Atom),
    maplist(atom_number, Atoms, L).

sums(L, S, N) :- sumrunner(L, S, N, 0).
sumrunner([], [], _, _).
sumrunner([A|B], [C|D], N, TOTAL) :- C is TOTAL + A + N, sumrunner(B, D, N, C).

max_from_left([], Temp, _, _, MaxArr):- MaxArr = Temp.
max_from_left([Head|Tail], Temp, Pos, Max, MaxArr):-
  (
    Head > Max ->
      Pos1 is Pos + 1,  
      append(Temp, [(Head,Pos1)], NewArr), 
      max_from_left(Tail, NewArr, Pos1, Head, MaxArr);
    Head =< Max,
      Pos1 is Pos + 1,
      max_from_left(Tail, Temp, Pos1, Max, MaxArr)
  ).

min_from_right([], Temp, _, _, MinArr):- MinArr = Temp.
min_from_right([Head|Tail], Temp, Pos, Min, MinArr):- 
  (
    Head < Min -> 
      Pos1 is Pos - 1,
      append(Temp, [ (Head, Pos1) ], NewTemp),
      min_from_right(Tail, NewTemp, Pos1, Head, MinArr)
    ; Head >= Min, 
        Pos1 is Pos - 1,
        min_from_right(Tail, Temp, Pos1, Min, MinArr)    
  ). 


len_tuple([], Pos1, Pos):-Pos1 is Pos.
len_tuple([_|Tail], Ans, Pos):-
  Ans1 is Pos + 1,
  len_tuple(Tail, Ans, Ans1).


solver(_, [], Ans, F):- F is Ans.
solver([], _, Ans, F):- F is Ans.
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
   read_input(File, M, N, C),
   sums(C,S,N),
   /*writeln(S)*/
   append([0], S, S1),
   max_from_left(S1, [], -1, -1, Max),
   reverse(S1, S2), 
   S2 = [H1|_],
   Max_ is H1 + 1,
   M_ is M+1, 
   min_from_right(S2, [], M_, Max_, Min), 
   reverse(Min, Min1),  
   solver(Max, Min1, 0, Ans).

