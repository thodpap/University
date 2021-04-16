
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
 
		val q = Queue.mkQueue(): ( int ) Queue.queue;
		fun solver (q,N,M,arr) =
			let 
				fun get_list_n 0 = [] 
					| get_list_n n =  0 :: get_list_n (n-1) 
				
				val visited = Array.fromList (get_list_n (N*M)) 
				fun solve (q,N,M,arr) =
					let
						fun fill_queue q = 
							let 
								fun dfs_top j = 
									if j < M then 
										if Array.sub(arr,j) = "U" then ( Queue.enqueue(q, j); dfs_top(j+1))
										else dfs_top(j+1)
									else ()
								val c1 = (N-1)*M
								fun dfs_bottom j = 
									if j < M then if Array.sub(arr,c1 + j) = "D" 
										then ( Queue.enqueue(q, c1 + j); dfs_bottom(j+1))
										else dfs_bottom(j+1)
									else ()
									
								fun dfs_left i = 
									if i < N then if Array.sub(arr, i*M) = "L"
										then ( Queue.enqueue(q, i*M); dfs_left(i+1))
										else dfs_left(i+1)
									else ()
									
								fun dfs_right i = 
									if i < N then if Array.sub(arr, i*M + M-1) = "R"
										then ( Queue.enqueue(q, i*M + M-1); dfs_right (i+1))
										else dfs_right(i+1)
									else () 
							in
								(dfs_top 0, dfs_bottom 0, dfs_left 0, dfs_right 0) 
							end
						val _ = fill_queue q
						val ans_var = [0]
						val ans = Array.fromList(ans_var)
						
						fun find_parents idx = 
							let    
								val _ = Array.update(visited, idx, 1)  
								val prev = Array.sub(ans,0)
								val _ = Array.update(ans,0, prev + 1)    
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
								then (find_parents (Queue.head(q)); Queue.dequeue(q); dfs q)
								else (Queue.dequeue(q); dfs q)
								
						val _ = dfs q
						val sol = N*M - Array.sub(ans,0)
					in
						(sol)
					end
			in
				solve (q,N,M,arr)
			end
		val answer = solver (q,N,M,arr);
	in
		print(Int.toString(answer))
	end;
