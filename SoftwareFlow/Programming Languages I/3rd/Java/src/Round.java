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
    Solution(int c, int p) {
        pos = p;
        count = c;
    }

    int pos;
    int count;
}

public class Round {
    private static void printArray(int[] arr) {
        for (int i = 0; i < arr.length; ++i) {
            System.out.print(arr[i] + " ");
        }
        System.out.print("\n");
    }

    private static void printPosArray(Position[] arr) {
        for (int i = 0; i < arr.length; ++i) {
            System.out.print("(" + arr[i].pos + ", " + arr[i].value + ") ");
        }
        System.out.print("\n");
    }

    private static void printList(List<Position> array) {
        for (int i = 0; i < array.size(); ++i) {
            System.out.print("(" + array.get(i).pos + ", " + array.get(i).value + ") ");
        }
        System.out.print("\n");
    }

    private static Solution solver(List<Position> array, int N, int K, int start) {
//        printList(array);
        Position[] arr = new Position[array.size()];
        List<Integer> onesPositions = new ArrayList<>();
        // Build the temp array
        for (int i = 0; i < array.size(); ++i) {
            Position element = array.get(i);
            if (i < start) {
                arr[array.size() - i - 1] = new Position(element.pos + N, element.value);
            } else {
                arr[i - start] = new Position(element.pos, element.value);
            }
        }
//        printPosArray(arr);
        int j = 0; // counts ones
        int count = 0;
        int size = arr.length;
        for (int i = 0; i < size - 1; ++i) {
            if (arr[i].value == 1) {
                onesPositions.add(arr[size - 1].pos - arr[i].pos);
            } else {
                count += arr[i].value * (arr[size - 1].pos - arr[i].pos);
                arr[size - 1].value += arr[i].value;
            }
        }

        // move ones if possible
        int independentMoves = 0;
        for (int i = 1; i < onesPositions.size(); ++i) {
            int prev = onesPositions.get(i - 1);
            int curr = onesPositions.get(i);

            if (prev == 0) continue;
            if (curr >= prev) {
                onesPositions.set(i - 1, 0);
                onesPositions.set(i, curr - prev);
                independentMoves += 2 * prev;
            } else {
                onesPositions.set(i - 1, 0);
                onesPositions.set(i, prev - curr);
                independentMoves += 2 * curr;
            }
        }
        // count += independentMoves;
        int movesNeeded = 0;
        if (onesPositions.size() > 1)
            movesNeeded = onesPositions.get(onesPositions.size() - 1);
        else if (onesPositions.size() == 1) {
            movesNeeded = onesPositions.get(0);
        }

        int lastElement = arr[size - 1].pos;

        if (movesNeeded <= count) {
            count += movesNeeded + independentMoves;
        } else {
            // Move the remaining 1 closer based on the count
            if (K == 2) {
                count = Integer.MAX_VALUE;
            } else {
                movesNeeded -= count;
                // Let p be the side movement: movesNeed + p <= (N - 1) * p -> p >= moves / (N-2)
                int p = (movesNeeded - 1) / (K - 2);
                int mod = (movesNeeded - 1) % (K - 2);

                if (mod != 0) ++p;

                // count += temp + p + (N - 1)*p + independentMoves;
                count += movesNeeded + p * K + independentMoves;
                lastElement += p;
            }
        }
        return new Solution(count, lastElement % N);
    }

    public static void main(String[] args) throws IOException {
//        FileInputStream fs = new FileInputStream(args[0]);
        FileInputStream fs = new FileInputStream("r2.txt");
        BufferedReader reader = new BufferedReader(new InputStreamReader(fs));

        String[] first = reader.readLine().split(" ");
        String[] line = reader.readLine().split(" ");

        int N = Integer.parseInt(first[0]);
        int K = Integer.parseInt(first[1]);

        int[] arr = new int[2 * N];

        for (int i = 0; i < line.length; ++i) {
            int carPos = Integer.parseInt(line[i]);
            arr[carPos] += 1;
        }
        List<Position> shortList = new ArrayList<>();
        for (int i = 0; i < arr.length; ++i) {
            if (arr[i] != 0) shortList.add(new Position(i, arr[i]));
        }

        Solution s = new Solution(-1, -1);
        for (int i = 0; i < shortList.size(); ++i) {
            Solution tempSol = solver(shortList, N, K, i);

            if (s.count == -1 || s.count >= tempSol.count) {
                if (tempSol.count == s.count) {
                    if (s.pos >= tempSol.pos) {
                        s.pos = tempSol.pos;
                    }
                } else {
                    s.count = tempSol.count;
                    s.pos = tempSol.pos;
                }

            }
        }
        System.out.println(s.count + " " + s.pos);
    }
}