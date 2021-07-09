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
    public static int N;
    public static int K; 

    public static Solution solver(int lastOne, int countOnes, int countTwos, int countElse, int neg, int ind, int moves, int C) {  
        int lastOneTotal = C - lastOne;
        int negTotal = C * countOnes - neg;
        
        int independentMovesTotal = C * countTwos - ind;
        int movesTotal = C * countElse - moves;

        int rest = negTotal - lastOneTotal;
        if (countOnes >= 2) { 
            if (rest + 1 >= lastOneTotal) { 
                independentMovesTotal += negTotal;
                negTotal = 0;                
            } else {
                negTotal = lastOneTotal - rest;
                independentMovesTotal += lastOneTotal;
            }
        } 
 
        if (movesTotal == 0 && negTotal == 0) {
            return new Solution(C % N, independentMovesTotal);
        }
        if (movesTotal + independentMovesTotal >= negTotal && movesTotal > 0) {
            movesTotal += independentMovesTotal + negTotal; 
            return new Solution(C % N, movesTotal);
        }
        return new Solution(0, Integer.MAX_VALUE);
    }
	public static void main(String[] args) throws IOException {  
        FileInputStream fs = new FileInputStream(args[0]);
        BufferedReader reader = new BufferedReader(new InputStreamReader(fs));

        String[] first = reader.readLine().split(" ");
        String[] line = reader.readLine().split(" ");
        reader.close();

        N = Integer.parseInt(first[0]);
        K = Integer.parseInt(first[1]); 
        
        int[] arr = new int[N]; 

        for (int i = 0; i < line.length; ++i) {
            int carPos = Integer.parseInt(line[i]);
            arr[carPos] += 1; 
        } 
        List<Position> shortList = new ArrayList<>();
        for (int i = 0; i < arr.length; ++i) {
        	if (arr[i] != 0) shortList.add(new Position(i, arr[i]));
        }  
        
        List<Integer> ones = new ArrayList<>();
        for (int i = 0; i < shortList.size(); ++i) {
            Position p = shortList.get(i);
            if (p.value == 1) ones.add(p.pos);
        }

        int countOnes = 0;
        int countTwos = 0;
        int countElse = 0;

        int negMoves = 0;
        int independentMoves = 0;
        int moves = 0;
         
        int j = 0;
        int lastOne = ones.get(0);

        // Proto perasma
        for (int i = 0; i < shortList.size(); ++i) {
            Position element = shortList.get(i);
            if (element.value == 1) { 
                countOnes += element.value; 
                negMoves += element.pos;
            }  else if (element.value == 2){ 
                countTwos += element.value;
                independentMoves += element.pos * element.value; 
            }
            else { 
                countElse += element.value;
                moves += element.pos * element.value; 
            }
        } 
        Solution s = solver(lastOne, countOnes, countTwos, countElse, negMoves, independentMoves, moves, N - 1); 
        for (int i = N; i < 2 * N; ++i) {
            // System.out.println(j + " " + lastOne + " " + countOnes + " " + countTwos + " " + countElse + " " + negMoves + " " +  independentMoves + " " + moves);
            if (arr[i - N] == 0) { }
            else if (arr[i - N] == 1) { 
                ++j;
                if (j >= ones.size()) {
                    lastOne = ones.get(j - ones.size()) + N;
                }
                else 
                    lastOne = ones.get(j);   
                negMoves += N;
            } else if (arr[i - N] == 2) {
                independentMoves += 2 * N; 
            } else {
                moves += N * arr[i-N];
            }
            
            Solution tempSol = solver(lastOne, countOnes, countTwos, countElse, negMoves, independentMoves, moves, i);  
            System.out.print("Temp sol: "); tempSol.print();
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