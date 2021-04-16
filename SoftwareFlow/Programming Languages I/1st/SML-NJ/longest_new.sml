fun longest file = 
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

		val (M,N, arr) = parse file

        fun prefix(array, sum, counter) = 
            if counter = M then [] 
            else ((sum + N + Array.sub(array, counter)) :: prefix(array, (sum + N + Array.sub(array, counter)), counter + 1))


        val prefix = Array.fromList(0 :: prefix(arr, 0, 0))


        fun max_from_left(array, max, counter) = 
            if counter = M + 1 then [] else
                if Array.sub(array, counter) < max then max_from_left(array, max, counter + 1)
                else ((Array.sub(array, counter), counter) :: max_from_left(array, Array.sub(array, counter), counter + 1))
            
        val max =  Array.fromList(max_from_left(prefix, ~1, 0))

        fun min_from_right(array, min, counter) = 
            if counter < 0 then [] else
                if Array.sub(array, counter) > min then min_from_right(array, min, counter - 1)
                else ((Array.sub(array, counter), counter) :: min_from_right(array, Array.sub(array, counter), counter - 1))
            
        val min =  Array.fromList(List.rev(min_from_right(prefix, valOf Int.maxInt, M)))

        fun first((x,y)) = x
        fun second((x,y)) = y
        fun maximum(a,b) = if a < b then b else a

        fun binary_search(array, start, last, upper_bound) = 
            if start >= last then ~1
            else
                let 
                    val mid = (start + last) div 2
                    val first_array = first(Array.sub(array, mid))
                    val second_array = second(Array.sub(array, mid)) 
                    
                    
                    
                    fun binary(mid) = 
                    if first_array = first(upper_bound) then second_array
                        else if  first_array > first(upper_bound) 
                        then binary_search(array, start, mid, upper_bound)
                        else 
                            if second_array > second(upper_bound) 
                            then maximum(second_array, binary_search(array, mid+1, last, upper_bound)) 
                            else binary_search(array, mid+1, last, upper_bound)
                    
                    val answer = binary(mid)
                    
                in   
                    (answer)
                end
                


        val length_max = Array.length(max)
        val length_min = Array.length(min)


        fun find_me(array_max, counter, ans) = 
            if counter = length_max then ans 
            else 
                let 
                    val binary = binary_search(min, 0, length_min-1, Array.sub(array_max, counter))
                    val new_ans = maximum(binary - second(Array.sub(array_max, counter)), ans)
                    
                in
                    (find_me(array_max, counter+1, new_ans))
                    
                end
                
        
        val final_answer = find_me(max, 0, 0)
        
    in 

        (print(Int.toString(final_answer)))

    end;
    