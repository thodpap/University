          
fun round file =
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
                (m,n, readInts n []) 
            end


        val (N,K, arr) = parse file 
        val positions = Array.array(N,0)

        fun fill_array [] = ()
            | fill_array arr = ( 
                Array.update(positions, hd arr, Array.sub(positions, hd arr) + 1);
                fill_array(tl arr) 
            )
        
        fun fill_short_list i = 
            if i = N then [] 
            else
                let 
                    val element = Array.sub(positions, i)
                in
                    if element > 0 then (i,element)::fill_short_list (i+1)  
                    else fill_short_list (i+1)
                end

        fun fill_ones_list [] = []
            | fill_ones_list list = 
                let 
                    val (pos, el) = hd list
                in  
                    if el = 1 then pos :: fill_ones_list (tl list)
                    else fill_ones_list (tl list)
                end
            
        val _ = fill_array arr
        val list = fill_short_list 0
        val ones_list = fill_ones_list list
        val ones = Array.fromList(ones_list)


        fun solver (lastOne, countOnes, countTwos, countElse, neg, ind, moves, c) = 
        let
            val lastOneTotal = c - lastOne
            val negTotal1 = c * countOnes - neg
            val ind1 = c * countTwos - ind
            val movesTotal = c * countElse - moves 
            val rest = negTotal1 - lastOneTotal 
            val (independentMovesTotal, negTotal) = 
                if countOnes >= 2 then
                    if rest + 1 >= lastOneTotal then (ind1 + negTotal1, 0)
                    else (ind1 + lastOneTotal, lastOneTotal - rest)
                else (ind1, negTotal1)  
        in  
            if movesTotal = 0 andalso negTotal = 0 then (c mod N, independentMovesTotal)
            else 
                if movesTotal + independentMovesTotal >= negTotal andalso movesTotal > 0
                then (c mod N, movesTotal + independentMovesTotal + negTotal)
            else (0, 1073741823) (* max int *)
        end 
        
        fun first_traverse ([], c1,c2,c3,n,i,m) = (c1,c2,c3,n,i,m)
        | first_traverse (list,c1,c2,c3,n,i,m) = 
            let 
                val (pos, value) = hd list

            in
                if value = 1 then first_traverse (tl list, c1 + value, c2, c3, n + pos, i, m)
                else if value = 2 then first_traverse (tl list, c1, c2 + value, c3, n, i + pos * value, m)
                else first_traverse (tl list, c1, c2, c3 + value, n, i, m + pos * value)
            end

        val (c1,c2,c3, n, i, m) = first_traverse (list, 0,0,0,0,0,0)
        val (first_sol_pos, first_sol_count) = solver(Array.sub(ones,0), c1,c2,c3,n,i,m, N - 1)

        fun decide_solution( sol_count, sol_pos, new_count, new_pos) = 
            if sol_count >= new_count then  
                if new_count = sol_count then 
                    if sol_pos >= new_pos then (sol_count, new_pos)
                    else (sol_count, sol_pos)
                else (new_count, new_pos)
            else (sol_count, sol_pos)
        
        fun getParameters(j, el,lastOne, c1,c2,c3, n, i, m) =
                if el = 0 then (j, lastOne, c1,c2,c3, n, i, m)
                else if el = 1 then
                    let 
                        val new_j = j + 1
                    in 
                        if new_j >= Array.length(ones) then (new_j, N + Array.sub(ones, new_j - Array.length(ones)), c1,c2,c3,n + N,i,m)
                        else (new_j, Array.sub(ones, new_j), c1,c2,c3,n + N,i,m)
                    end
                else if el = 2 then (j, lastOne, c1,c2,c3,n, i + 2 * N, m)
                else (j, lastOne, c1,c2,c3,n, i, m + N * el)

        fun traverse (idx, j, lastOne,c1,c2,c3, n, i, m, sol_count, sol_pos) = 
            if idx = 2 * N then (sol_count, sol_pos)
            else 
                let 
                    val el = Array.sub(positions, idx - N)
                    val (j_n, lastOne_n, c1_n,c2_n,c3_n, n_n, i_n, m_n) = getParameters(j, el, lastOne, c1,c2,c3, n, i, m)
                    val (temp_pos, temp_count) = solver(lastOne_n,  c1_n,c2_n,c3_n, n_n, i_n, m_n, idx)
                    val (new_count, new_pos) = decide_solution(sol_count,sol_pos, temp_count, temp_pos)
                in 
                    traverse(idx+1, j_n, lastOne_n, c1_n,c2_n,c3_n, n_n, i_n, m_n, new_count, new_pos)
                end 

        val (sol_c,sol_pos) = traverse(N,0,Array.sub(ones,0),c1,c2,c3, n, i, m, first_sol_count,first_sol_pos)
        val _ = print(Int.toString(sol_c))
        val _ = print(" ")
        val _ = print(Int.toString(sol_pos))
        val _ = print("\n")
    in  (c1,c2,c3, n, i, m)
    end;
 