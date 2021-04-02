  

val N = 2;
val M = 2;  

val input = ["R", "D", "U", "U"];
val arr = Array.fromList (input);
 

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
                    then  (print("then1"); find_parents(i,j-1))
                    else ()
                    
                val _ = if j < M - 1 andalso Array.sub(visited, idx + 1) = 0 andalso
                        Array.sub(arr,idx + 1) = "L" 
                        then (print("then2\n"); find_parents(i,j+1))
                    else ()
                
                
                val _ = if i > 0 andalso
                    Array.sub(visited, idx - M) = 0 andalso
                    Array.sub(arr,idx - M) = "D" 
                    then (print("then3\n"); find_parents(i-1,j))
                    else ()
                    
                val _ = if i < N - 1 andalso
                    Array.sub(visited, idx + M) = 0 andalso
                    Array.sub(arr,idx + M) = "U"
                    then (print("then4\n"); find_parents(i+1,j))
                    else ()
                        
                in 
                    ()
                end 
            
            fun dfs() = 
                let 
                    
                in
                
                end 
         
    in 
        (visited)
    end;

loop_rooms(N,M, arr)