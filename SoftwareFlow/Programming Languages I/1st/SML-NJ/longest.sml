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

		val (M,N, arr) = parse "longest.txt"

		fun longestArg (M:int , N:int, l) = 
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
		  					if sum <= ~ K * N then K
		  					else Int.max( recursion(start + 1,last,a) , recursion(start, last - 1, a) )
		  				end  

		  	in 
		  		recursion (0,M-1, a)
		  	end


	in 
		longestArg (M,N,arr)
	end;