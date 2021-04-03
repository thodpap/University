  

val N = 3;
val M = 3;  

val input = ["U", "L", "D", "L", "U", "D", "L","R","L"]
val arr = Array.fromList (input);

print("Before\n");

<<<<<<< HEAD
fun check a = if a < 5 then ((print(Int.toString(a))); ()) else ();


fun equals(b:string) = if b = "g" then true else false;

 val x = Array.fromList(["U","L","R","D"]);

fun run(a:array, counter:int) =
    if Array.sub(a, counter) = "U" then true else false;
    
run(x, 1);


(* val array = ["U", "L", "R", "L"];
val arr = Array.fromList (array);

fun loop_rooms(arr:array, N:int, M:int) = 
        let
            val counter = 0
            val visited = Array.array(N*M, 0)
            fun find_parents(i, j) = 
                index = i*M + j
                Array.update(visited, index)
                counter = counter + 1
                (* val _ = if j >= 1 andalso not Array.sub(visited, index-1) andalso Array.sub(arr, index-1) == 'R' 
                    then find_parents(i,j - 1) 
=======
fun sum_of_list (pos,M)  = 
    if pos < M then pos + sum_of_list(pos+1,M) else 0; 

sum_of_list (0,M);
    
fun loop_rooms(N, M, arr) = 
    let
        
        fun get_list_n 0 = [] 
            | get_list_n n =  0 :: get_list_n (n-1) 
        
        val visited = Array.fromList (get_list_n (N*M))
         
        
        fun find_parents(i:int,j:int) = 
            let   
                val idx =  i*M + j
                val _ = Array.update(visited, idx, 1)   
                
                val _ = if j > 0 andalso 
                    (Array.sub(visited,idx - 1) = 0 andalso
                    Array.sub(arr,idx - 1) = "R")
                    then find_parents(i,j-1)
>>>>>>> a16afe588cfd38b86cdf65758d1f9f9b7beab3bd
                    else ()
                    
                val _ = if j < M - 1 andalso Array.sub(visited, idx + 1) = 0 andalso
                        Array.sub(arr,idx + 1) = "L" 
                        then find_parents(i,j+1)
                    else ()
                
                
                val _ = if i > 0 andalso
                    Array.sub(visited, idx - M) = 0 andalso
                    Array.sub(arr,idx - M) = "D" 
                    then find_parents(i-1,j)
                    else ()
                    
                val _ = if i < N - 1 andalso
                    Array.sub(visited, idx + M) = 0 andalso
                    Array.sub(arr,idx + M) = "U"
                    then find_parents(i+1,j)
                    else ()
                        
                in 
                    ()
                end 
        fun dfs (max_top_bottom, max_left_right) = 
            let
                fun dfs_top j = 
                    if j < M then (find_parents(0,j); dfs_top(j+1)) else ()
                    
                fun dfs_bottom j = 
                    if j < M then (find_parents(N-1,j); dfs_bottom(j+1)) else ()
                    
                    
                fun dfs_right i = 
                    if i < N then (find_parents(i,0); dfs_right(i+1)) else ()
                    
                fun dfs_left i = 
                    if i < N then (find_parents(i,M-1); dfs_left(i+1)) else ()
                    
                    
                 
            in
                dfs_top 0;
                dfs_bottom 0;
                dfs_left 0;
                dfs_right 0
            end
        fun count n =
            if n < N*M then 
                if Array.sub(visited,n) = 1 then 
                    1 + count(n+1) 
                else count(n+1)
            else 0
            
        
                   
         
    in 
        dfs (N-1,M-1);
        count 0
    end;

<<<<<<< HEAD
        in
            find_parents(0, 0)
        end; *)
=======
loop_rooms(N,M, arr)
>>>>>>> a16afe588cfd38b86cdf65758d1f9f9b7beab3bd
