

datatype 'a tree = Leaf | Node of 'a * 'a tree * 'a tree

fun trim Leaf = [Leaf]
    | trim Node(value, left, right) = 
    let 
        fun is_different(value, Leaf) = false
            | is_different(value, Node(v,l,r)) = 
                if value mod 2 = 1 then true
                else false

        fun help(Leaf, acc) = acc
            | help(Node(n, l, r), acc) = 
                let 
                    val left = is_different(n, l)
                    val right = is_different(n,r)
                    
                in  
                end
                

    in 
        (help(tree, []))
    end;


(* fun floor nil K = ~1
    | floor tree K = 
        let 
            fun walk nil max = max
                | walk (Node(n,l,r)) max = 
                    if n < K then  walk r (Int.max(max, n))
                    else if n = K then n
                    else walk l max 
        in  
            walk tree ~1
        end;  *)
