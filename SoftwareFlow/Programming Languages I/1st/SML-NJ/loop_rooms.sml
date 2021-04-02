(* fun loop_rooms file = 
	let 
		fun parse file =
		    let 
		        fun readInt input = 
			    Option.valOf (TextIO.scanStream (Int.scan StringCvt.DEC) input)

		    	val inStream = TextIO.openIn file
		 	
				val m = readInt inStream  
				val n = readInt inStream
				val _ = TextIO.inputLine inStream 

				fun readInts 0 acc = acc 
				    | readInts i acc = readInts (i - 1) (readInt inStream :: acc)
		 
		    in
		   		(m,n, readInts m []) 
		    end

		val (M,N, arr) = parse "longest.txt" *)


val array = ["U", "L", "R", "L"];
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
                    else ()
                    
                val _ = if j < M  andalso not Array.sub(visited, index+1) andalso Array.sub(arr, index+1) == 'L' 
                    then find_parents(i,j + 1) 
                    else ()
                   
                val _ = if i >= 1 andalso not Array.sub(visited, index-M) andalso Array.sub(arr, index-M) == 'D' 
                    then find_parents(i - 1,j) 
                    else ()
                   
                val _ = if i < N  andalso not Array.sub(visited, index+M) andalso Array.sub(arr, index+M) == 'U' 
                    then find_parents(i + 1,j) 
                    else () *)
                
                print(Int.toString(counter) ^ "\n")


        in
            find_parents(0, 0)
        end;
