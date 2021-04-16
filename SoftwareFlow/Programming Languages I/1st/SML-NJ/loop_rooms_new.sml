val array = ["U","L","D","L","U","D","L","R","L"];
val arr = Array.fromList(array);
val N = 3;
val M = 3;
val q = Queue.mkQueue(): ( int ) Queue.queue;
fun get_list_n 0 = [] 
    | get_list_n n =  0 :: get_list_n (n-1) 

val visited = Array.fromList (get_list_n (N*M)) 
                    
fun solve (q,N,M,arr) =
    let
        fun fill_queue q = 
            let 
                fun dfs_top j = 
                    if j < M andalso Array.sub(arr,j) = "U" 
                        then ( Queue.enqueue(q, j); dfs_top(j+1))
                    else ()
                val c1 = (N-1)*M
                fun dfs_bottom j = 
                    if j < M andalso Array.sub(arr,c1 + j) = "D" 
                        then ( Queue.enqueue(q, c1 + j); dfs_top(j+1))
                    else ()
                    
                fun dfs_left i = 
                    if i < N andalso Array.sub(arr, i*M) = "L"
                        then ( Queue.enqueue(q, i*M); dfs_left(i+1))
                    else ()
                    
                fun dfs_right i = 
                    if i < N andalso Array.sub(arr, i*M + M-1) = "R" 
                        then ( Queue.enqueue(q, i*M + M-1); dfs_right (i+1))
                    else ()
                    
                
            in
                (dfs_top 0, dfs_bottom 0, dfs_left 0, dfs_right 0 ) 
            end
        val _ = fill_queue q
        val ans = 0
        fun find_parents idx = 
            let    
                val _ = Array.update(visited, idx, 1)   
                val i = idx div M
                val j = idx mod M
                val _ = if j >= 1 andalso 
                    (Array.sub(visited,idx - 1) = 0 andalso
                    Array.sub(arr,idx - 1) = "R")
                    then find_parents(idx - 1) 
                    else ()
                    
                val _ = if j < M - 1 andalso Array.sub(visited, idx + 1) = 0 andalso
                        Array.sub(arr,idx + 1) = "L" 
                        then find_parents(idx+1)
                    else ()
                
                
                val _ = if i > 0 andalso
                    Array.sub(visited, idx - M) = 0 andalso
                    Array.sub(arr,idx - M) = "D" 
                    then find_parents(idx - M)
                    else ()
                    
                val _ = if i < N - 1 andalso
                    Array.sub(visited, idx + M) = 0 andalso
                    Array.sub(arr,idx + M) = "U"
                    then find_parents(idx + M)
                    else () 
            in 
                ()
            end 
        
        fun dfs q = 
            if Queue.isEmpty(q) then ()
            else if Array.sub(visited, Queue.head(q)) = 0   
                then (print(Int.toString(Queue.head(q))); 
                    find_parents (Queue.head(q)); Queue.dequeue(q); dfs q)
                else (Queue.dequeue(q); dfs q)
                
        val _ = dfs q
    in
        (visited)
    end;

solve (q,N,M,arr)