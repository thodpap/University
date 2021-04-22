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
        val arr = Array.fromList(List.rev(arr))

        fun prefixFun (array, sum, counter) = 
            if counter = M then [] 
            else 
                let
                    val newSum = sum + N + Array.sub(array,counter)
                in
                    newSum :: prefixFun(array, newSum, (counter + 1))
                end


        val prefix = prefixFun(arr, 0, 0)
        val prefix = Array.fromList(0 :: prefix)


        fun max_from_left(array, max, counter) = 
            if counter = M + 1 then [] else
                if Array.sub(array, counter) < max then max_from_left(array, max, counter + 1)
                else ((Array.sub(array, counter), counter) :: max_from_left(array, Array.sub(array, counter), counter + 1));
            
        val max =  Array.fromList(max_from_left(prefix, ~1, 0))

        fun min_from_right(array, min, counter) = 
            if counter < 0 then [] else
                if Array.sub(array, counter) > min then min_from_right(array, min, counter - 1)
                else ((Array.sub(array, counter), counter) :: min_from_right(array, Array.sub(array, counter), counter - 1));
            
        val min =  Array.fromList(List.rev(min_from_right(prefix, valOf Int.maxInt, M)))

        fun first((x,y)) = x
        fun second((x,y)) = y
        fun maximum(a,b) = if a < b then b else a

        val length_max = Array.length(max)
        val length_min = Array.length(min)
  
        fun solver(i, j, ans) =
            if i >= length_max orelse j >= length_min then ans
            else 
                let
                    val mini = Array.sub(min,j)
                    val maxi = Array.sub(max,i)
                    val res = 
                        if first(mini) <= first(maxi) 
                            then  
                            if j + 1 < length_min andalso first(Array.sub(min,j+1)) <= first(maxi) 
                                then solver(i,j+1,ans)
                            else solver(i+1,j+1,maximum(ans,second(mini) - second(maxi)))
                        else 
                        if second(maxi) < second(mini) - 1 then solver(i+1,j,ans)
                        else solver(i,j + 1,ans)
                in
                    (res)
                end

        val final_answer = solver(0,0,0)
    in 
        print(Int.toString(final_answer))
        (* (max,min,length_max,length_min,binary_search(min,0,2,(0,0)), final_answer) *)
    end;