
fun count n =
    let
        fun loop i n = 
        if i <= n then (print (Int.toString i ^ "\n"); loop (i+1) n)
        else 
            ()

    in
        loop 1 n
    end
    
fun halve [] = ([], []) 
    | halve [x] = ([x], [])
    | halve (x :: y :: rest) = 
        let 
            val (left,right) = halve rest
        in
            (x :: left, y :: right)
        end
        
fun splitAt k [] = ([], []) 
    | splitAt 0 l = ([], l)
    | splitAt k (h :: t) = 
        let 
            val (left,right) = splitAt (k-1) t
        in
            (h :: left, right) 
        end

fun split l = 
    let 
        val n = length l
    in
        splitAt ((n+1) div 2) l
    end
        
fun assert condition = if not condition then print "Wrong!\n" else print "Correct!\n"


fun testSplit f = (
    assert (f [] = ([],[]));
    assert (f [42] = ([42],[]));
    assert (f [17,42] = ([17],[42]));
    assert (f [1,2,3] = ([1,2], [3]))
    
)










































 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 





