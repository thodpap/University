
fun loop_rooms file = 
    let
        fun parse file =
            let 
                fun readInt input = 
                    Option.valOf (TextIO.scanStream (Int.scan StringCvt.DEC) input)

                val inStream = TextIO.openIn file
            
                val n = readInt inStream 
                val m = readInt inStream  
                val _ = TextIO.inputLine inStream 
 
                
            in
                (n,m) 
            end

        val (N,M) = parse file
        val instream = TextIO.openIn file;
        fun toStr c = if c = #"\n" then "\n" else (Char.toString c);
        fun toChar s = map toStr (String.explode (Option.valOf s))
        fun parseIns l x =
          if x = NONE then l
          else parseIns (x :: l) (TextIO.inputLine instream);

        (* list and dimensions *)
        val l = List.map toChar (parseIns [] (TextIO.inputLine instream)); 
        val new = List.concat (List.rev (List.take(l,N)));

        fun keepElements [] = [] 
            | keepElements list = 
                if (hd list) = "\n" then keepElements(tl list)
                else (hd list) :: keepElements(tl list)

        val arr = Array.fromList(List.take(keepElements new, N*M ))

        fun loop_rooms (N, M, arr) = 
            let 
                fun get_list_n 0 = [] 
                    | get_list_n n =  0 :: get_list_n (n-1) 
                
                val visited = Array.fromList (get_list_n (N*M)) 
                    
                fun count n =
                    let  
                        fun dfs t = 
                            let
                                fun find_parents(i:int,j:int) = 
                                    let   
                                        val idx =  i*M + j
                                        val _ = Array.update(visited, idx, 1)   
                                        
                                        val _ = if j >= 1 andalso 
                                            (Array.sub(visited,idx - 1) = 0 andalso
                                            Array.sub(arr,idx - 1) = "R")
                                            then find_parents(i,j-1) 
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

                                val precalc1 = (N-1)*M
                                
                                fun dfs_top j = 
                                    if j < M then  
                                        if Array.sub (arr, j) = "U" andalso Array.sub(visited, j) = 0 then (find_parents(0,j); dfs_top (j+1)) 
                                        else dfs_top (j+1)
                                    else ()
                                    
                                fun dfs_bottom j = 
                                    if j < M then 
                                        if Array.sub(arr,precalc1 + j) = "D" andalso Array.sub(visited, precalc1+j) = 0  then (find_parents(N-1,j); dfs_bottom(j+1)) 
                                        else dfs_bottom (j+1)
                                    else ()
                                    
                                    
                                fun dfs_right i = 
                                    if i < N then 
                                        if Array.sub(arr, i*M) = "L" andalso Array.sub(visited, i*M) = 0  then (find_parents(i,0); dfs_right(i+1)) 
                                        else dfs_right(i+1)
                                    else ()
                                    
                                fun dfs_left i = 
                                    if i < N then
                                        if Array.sub(arr, i*M + M-1) = "R" andalso Array.sub(visited, i*M+M-1) = 0  then (find_parents(i,M-1); dfs_left(i+1)) 
                                        else dfs_left(i+1)
                                    else () 
                            in
                                (dfs_top 0, dfs_bottom 0, dfs_right 0,dfs_left 0) 
                            end
                        val _ = dfs 0
                        fun help_count n = 
                            if n < N*M then 
                                if Array.sub(visited,n) = 1 then 
                                    1 + count(n+1) 
                                else count(n+1)
                            else 0 
                    in
                        (help_count n)
                    end 
            in 
                (N*M - count 0)
            end; 
    in
        print(Int.toString(loop_rooms(N,M, arr)))
    end;