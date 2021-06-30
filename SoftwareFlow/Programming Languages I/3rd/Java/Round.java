import java.io.*;
import java.util.*;


class Position {
	Position(int pos, int value) {
		this.pos = pos;
		this.value = value;
	}
	int pos;
	int value;
}
class Solution {
	Solution(int p, int c) {
		pos = p;
		count = c;
	}
	int pos;
	int count; 
    void print() {
        System.out.println(count + " " + pos);
    }
}
public class Round {
    private static Solution solver(
        int N,
        int K,
        int countOnes, 
        int countTwos, 
        int countElse ,
        int neg, 
        int independentMoves, 
        int moves, 
        int sumElse,
        int lastElement) 
    { 
        int negTotal = lastElement * countOnes - neg;
        int independentMovesTotal =  2 * lastElement * countTwos - independentMoves;
        int movesTotal = lastElement * sumElse - moves;

        System.out.println("Counts: " + countOnes + " " + countTwos + " " + countElse);
        System.out.println("Values : " + neg + " " + independentMoves + " "  + moves + " " + sumElse + " " + lastElement);
        System.out.println("New Values: " + negTotal + " " + independentMovesTotal + " " + movesTotal);

        if (movesTotal >= negTotal) {
            movesTotal += negTotal + independentMovesTotal;
            System.out.println(movesTotal + " " + lastElement);
            return new Solution(lastElement % N, movesTotal);
        } 
        movesTotal += independentMovesTotal;
        int div = negTotal / K;
        int mod = negTotal % K;
        if (mod > 1) ++div;
        movesTotal += K * div + negTotal;
        lastElement += div;

        System.out.println("Last: " + div + " " + mod + " " + movesTotal );
        System.out.println(movesTotal + " " + lastElement);
        return new Solution(lastElement % N, movesTotal);
    }  
	public static void main(String[] args) throws IOException {  
        FileInputStream fs = new FileInputStream(args[0]);
        BufferedReader reader = new BufferedReader(new InputStreamReader(fs));

        String[] first = reader.readLine().split(" ");
        String[] line = reader.readLine().split(" ");

        int N = Integer.parseInt(first[0]);
        int K = Integer.parseInt(first[1]); 
        
        int[] arr = new int[N]; 

        for (int i = 0; i < line.length; ++i) {
            int carPos = Integer.parseInt(line[i]);
            arr[carPos] += 1; 
        } 
        List<Position> shortList = new ArrayList<>();
        for (int i = 0; i < arr.length; ++i) {
        	if (arr[i] != 0) shortList.add(new Position(i, arr[i]));
        }  
        /* 
            Let assume we have to stop at C (not mod N) - linear map 
        */
        int countOnes = 0;
        int countTwos = 0;
        int countElse = 0;

        int sumElse = 0;
        int neg = 0;
        int independentMoves = 0;
        int moves = 0;


        // Calculate first window
        for (int i = 0; i < shortList.size(); ++i) {
            Position element = shortList.get(i);
            if (element.value == 1) { 
                ++countOnes;
                neg += element.pos; 
            } else if (element.value == 2) {
                ++countTwos;
                independentMoves += 2 * element.pos;
            } else {
                ++countElse;
                moves += element.pos * element.value;
                sumElse += element.value;
            }
        }

        Solution s = solver(N,K, countOnes, countTwos, countElse, neg, independentMoves, moves, sumElse, 
            shortList.get(shortList.size() - 1).pos); 
        for (int i = 0; i < shortList.size() - 1; ++i) { 
            Position element = shortList.get(i);
            if (element.value == 1) { 
                neg += N;
            } else if (element.value == 2) { 
                independentMoves += 2 * element.pos;
            } else { 
                moves += N * element.value;
            }

            Solution tempSol = solver(N,K, countOnes, countTwos, countElse, neg, independentMoves, moves, sumElse, element.pos + N);
            // tempSol.print();
        		
        	if (s.count >= tempSol.count) { 
        		if (tempSol.count == s.count) {
        			if (s.pos >= tempSol.pos) {
        				s.pos = tempSol.pos; 
        			}	
        		}
                else {
                    s.count = tempSol.count;
                    s.pos = tempSol.pos;
                }         
        	}  	
        }
        
        s.print();
    }
}