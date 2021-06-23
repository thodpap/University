(* fun loop (m,m) = ()
    | loop (n, m) = ( print(Int.toString n ^ "\n"); loop (n+1),m) *)

(* fun count n = 
    loop 0,n *)

fun loop n = 
    let 
        fun hloop i n = 
            if i <= n then 
                (print (Int.toString i ^ "\n"); hloop (i+1) n)
            else 
                ()
    in 
        (hloop 0 n)
    end;

fun count n = 
    let 
        fun loop i n = 
            if i < n then (print (Int.toString i ^ "\n"); loop (i+1) n)
            else ()
    in 
        (loop 0 n)
    end;

fun sumList list = 
    let 
        fun sum ([], sum_so_far) = sum_so_far
            | sum (list, sum_so_far) =  
                sum (tl list, sum_so_far + hd list)
    in 
        sum (list, 0)
    end;

fun summedList list = 
    let fun sum_ ([], sum) = []
        | sum_ (list, sum) = 
            let  
                val head = hd list + sum;
            in
                head :: sum_(tl list, head) 
            end
            
    in 
        sum_ (list,0)
    end;
 
val temp = [] :: [ [1,2,3] ]
(* val temp = nil :: [1,2,3] :: nil; *)
fun listify([],a) = []
    | listify (list, a) = 
    let 
        fun isEmpty [] = true
            | isEmpty list = false

        fun passListSmaller ([],a) = []
            | passListSmaller (list,a) = 
                if hd list < a then passListSmaller(tl list, a)
                else list
        fun passListGreater ([],a) = []
            | passListGreater (list,a) = 
                if hd list >= a then passListGreater(tl list, a)
                else list

        fun smaller ([],a) = []
            | smaller (li, a) = 
                if hd li < a then hd li :: smaller(tl li, a)
                else []

        fun greater ([],a) = []
            | greater (li,a) = 
                if hd li >= a then hd li :: greater(tl li, a)
                else []
        val sml = smaller(list,a)
        val l1 = passListSmaller(list , a)
        val gtr = greater(l1,a)
        val newList = passListGreater(l1,a)
        val res = listify(newList,a)
    in
        if isEmpty l1 then [sml]
        else sml :: gtr :: res 
    end;

fun maxSumSublist list = 
    let 
        fun sum_ ([], sum) = []
        | sum_ (list, sum) = 
            let  
                val head = hd list + sum;
            in
                head :: sum_(tl list, head) 
            end
        
        fun findBestSum ([], max, el) : int = max
            | findBestSum (sumList, max, el) =
                if hd sumList - el > max then 
                    findBestSum (tl sumList, hd sumList - el, el)
                else findBestSum (tl sumList, max, el)

        fun parseForAllLists([], maxi, elem) = maxi
            | parseForAllLists(sumList, maxi, elem) = 
            let 
                val best = findBestSum(sumList, maxi, elem)
            in 
                parseForAllLists(tl sumList, best, hd sumList)
            end

        val sum_list = sum_(list,0) 
    in    
        parseForAllLists(sum_list, 0, 0)
    end;

fun double_pairs [] = []
    | double_pairs L = 
        let 
            fun find_double([],num) = false
                | find_double(L, num) = 
                if hd L = 2 * num then 
                    true 
                else 
                    find_double(tl L, num)

            fun parseList([], initial) = [] 
                | parseList(list, initial) = 
                    if find_double(initial, hd list) then 
                        (hd list, 2 * (hd list))::parseList(tl list, initial)
                    else 
                        parseList(tl list, initial)

        in
            parseList(L,L)
        end;

fun function2 ls = 
    let 
        fun d [] n = n
            | d (42 :: t) n = d t (n+1)
            | d (h :: t) n = Int.max (n, d t 0)
    in d ls 0
    end;


(* datatype 'a tree = Leaf | Node of 'a * 'a tree * 'a tree *)
datatype 'a tree = nil | Node of 'a * 'a tree * 'a tree

fun floor nil K = ~1
    | floor tree K = 
        let 
            fun walk nil max = max
                | walk (Node(n,l,r)) max = 
                    if n < K then  walk r (Int.max(max, n))
                    else if n = K then n
                    else walk l max 
        in  
            walk tree ~1
        end; 

fun allsubseq list  =
    let 
        fun walk (x, [], acc) = rev acc 
            | walk (x, (ys::yss), acc) = 
                walk (x,yss,((x::ys)::ys::acc))
        
        fun outter [] = []
            | outter (x::xs) =  walk (x,(outter xs),[[x]])
    in [] :: outter list

    end;  

fun bar x y z = x z (y z z)
fun ugh x y z = x (z :: y)

datatype heap = empty | node of int * heap * heap

fun isHeap empty = true
    | isHeap (node(v, le,ri)) = 
    let fun traverse (empty,value) = true
            | traverse (node(x,l,r),value) = 
                        x >= value 
                andalso traverse(l, x) 
                andalso traverse(r, x)
    in 
        traverse(le, v) andalso traverse(ri, v)
    end;
fun f x = x + 1
fun f2 x = 2*x
fun f3 s = s^s

fun itermap f list = 
    let 
        fun calculate_n (f,x,0) = x
            | calculate_n (f,x,1) = f(x)
            | calculate_n (f,x,n) = calculate_n (f,f x,n-1)

        fun itermap_help (f, [], count) = []
            | itermap_help (f, h::t, count) = 
                calculate_n(f, h, count) :: itermap_help(f, t, count + 1)

    in itermap_help (f, list, 0)
    end;
 
 fun enum low high = 
    let fun help (low, high, acc) = 
        if low <= high then help(low+1,high, low::acc)
        else rev acc
    in help (low, high, [])
    end;

fun bidlist list = 
let 
    fun find_sum ([], max, pos) = max
        | find_sum((key,value)::xs, max, pos) = 
            if key = pos then 
                find_sum(xs, max + value, pos)
            else find_sum(xs, max, pos)
    
    fun find_K ([],k) = k
        | find_K ((key,value)::xs, k) = find_K (xs, Int.max(k, key))
    val k = find_K (list, 0)

    fun traverse_up_toK (count, k) = 
        if count = (k+1) then [] 
        else find_sum(list, 0, count) :: traverse_up_toK(count+1,k)
in  
    traverse_up_toK(0,k)
end;