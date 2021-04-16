fun longest file = 
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

	in 
		(new)
	end;