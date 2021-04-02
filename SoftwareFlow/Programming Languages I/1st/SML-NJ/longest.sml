 

val M = 11;
val N = 3;
val arr = [42, ~10, 8, 1, 11, ~6, ~12, 16, ~15 , ~11, 13];

fun dpSolution (M:int , N:int, l) = 
	let  
		fun sums l = 
		    let 
		        fun addTo ([], sumSoFar) = []
		                | addTo (l, sumSoFar) = 
		                    sumSoFar + hd l :: addTo(tl l, sumSoFar + hd l)

		    in
		        addTo(l,0)
  		  end 
  		val a = Array.fromList (sums l)
  		
  		fun recursion (start, last, a) = 
  			if start >= last then ~1
  			else 
  				let 
  					fun sumOfStartLast (0, last, a) = Array.sub (a, last)  
  						| sumOfStartLast(start, last,a) =  Array.sub (a, last) - Array.sub(a, start - 1)
  					val sum = sumOfStartLast (start, last, a)
  					val K = last - start + 1

  				in 
  					if sum < ~ K * N then K
  					else Int.max( recursion(start + 1,last,a) , recursion(start, last - 1, a) )
  				end

  		

  	in 
  		recursion (0,M-1, a)
  	end;

dpSolution (M,N,arr)