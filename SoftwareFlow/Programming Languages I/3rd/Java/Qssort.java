import java.io.*;
import java.util.*;

class State{
    State(Queue<Integer> q, Stack<Integer> s, String p) {
        this.queue = new LinkedList<>(q);
        this.stack = (Stack<Integer>)s.clone();
        this.path = p;
    }
    String  getState() {
        return queue.toString() + stack.toString();
    }
    Queue<Integer> queue;
    Stack<Integer> stack;
    String path;
}

public class Qssort {
    private static State Q(State state) {
        State newState = new State(state.queue, state.stack, state.path);
        int front = newState.queue.remove();
        newState.stack.push(front);
        newState.path += "Q";
        return newState;
    }
    private static State S(State state) {
        State newState = new State(state.queue, state.stack, state.path);
        int back = newState.stack.pop();
        newState.queue.add(back);
        newState.path += "S";
        return newState;
    }
    public static String bfs(int N, Queue<Integer> queue) {
        LinkedList<Integer> sorted = new LinkedList<Integer>(queue);
        HashMap<String, Integer> dictionary = new HashMap<>();
        Collections.sort(sorted);
        Queue<State> totalQueue = new LinkedList<>();
        State s = new State(queue, new Stack<Integer>() , "");
        totalQueue.add(s);
        dictionary.put(s.getState(), 1);

        while (!totalQueue.isEmpty()) {
            State head = totalQueue.remove();

            if (sorted.equals((head.queue))) {
                if (head.path.equals(""))
                    return "empty";
                return head.path;
            }

            if (head.queue.isEmpty()) {
                State tempS = S(head);
                if (!dictionary.containsKey(tempS.getState())) {
                    totalQueue.add(tempS);
                    dictionary.put(tempS.getState(), 1);
                }
            } else if (head.stack.isEmpty()) {
                State tempQ = Q(head);
                if (!dictionary.containsKey(tempQ.getState())) {
                    totalQueue.add(tempQ);
                    dictionary.put(tempQ.getState(), 1);
                }
            } else {
                State tempQ = Q(head);
                if (!dictionary.containsKey(tempQ.getState())) {
                    totalQueue.add(tempQ);
                    dictionary.put(tempQ.getState(), 1);
                }

                if (head.queue.peek() != head.stack.peek()) {
                    State tempS = S(head);
                    if (!dictionary.containsKey(tempS.getState())) {
                        totalQueue.add(tempS);
                        dictionary.put(tempS.getState(), 1);
                    }
                }

            }

        }
        return "";
    }
    public static void main(String[] args) throws IOException {
        Queue<Integer> queue = new LinkedList<>();

        FileInputStream fs = new FileInputStream(args[0]);
        BufferedReader reader = new BufferedReader(new InputStreamReader(fs));

        int N = Integer.parseInt(reader.readLine().split(" ")[0]);
        String[] line = reader.readLine().split(" ");

        for (int i = 0; i < line.length; ++i) {
            queue.add(Integer.parseInt(line[i]));
        }
        System.out.println(bfs(N, queue));
    }
}
