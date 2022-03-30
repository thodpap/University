#include <bits/stdc++.h>

using namespace std;

class Edge{
public:
    Edge(int o, int p, int q) {
        node1 = o;
        node2 = p;
        weight = q;
    }
    pair<int,int> getNodes() const {
        return make_pair(node1,node2);
    }
    int getWeight() const{
        return weight;
    }
private:
    int node1;
    int node2;
    int weight;
};

class Graph {
public:
    Graph(int n, int m) { // M nodes and M edges
        edges.clear();
        id.clear();
        sz.clear();
        N = n;
        M = m; 
        for (int i = 0; i < N; ++i) { // initialize for path compression
            id.push_back(i);
            sz.push_back(i);
        }
    }
    void addEdge(int n1, int n2, int w) {
        edges.push_back(Edge(n1,n2,w));
    }
    
    int solver(queue<pair<int,int>> q) {
        std::sort(edges.begin(), edges.end(),
          [](Edge const & a, Edge const & b) -> bool
          { return a.getWeight() > b.getWeight(); } );  
        
        // for (int i = 0; i < edges.size(); ++i) {
        //     cout << "(" << edges[i].getNodes().first << " , " << edges[i].getNodes().second << " , " << edges[i].getWeight() << ")" << endl;
        // }
        int ans = INT_MAX;
        int i = 0;
        while (i < edges.size()) {
            if (q.empty()) {
                break;
            }
            pair<int,int> f = q.front();
            // for (int k = 0; k < id.size(); ++k)
            //     cout << id[k] << " ";
            // cout << endl;
            if (f.first == f.second || temp_find(f)) {
                // cout << f.first << " " << f.second << " was cut out\n";
                q.pop();
                continue;
            }
            // for (int k = 0; k < id.size(); ++k)
            //     cout << id[k] << " ";
            // cout << endl;cout << endl;
            // cout << f.first << " " << f.second << " continue\n";

            if (!find(edges[i].getNodes())) {
                f = edges[i].getNodes();
                // cout << f.first << " " << f.second << endl;
                unite(edges[i].getNodes());
                ans = edges[i].getWeight();
            }
            ++i;
        }

        return ans;
    } 
    
private:
int N,M;
    vector<int> id, sz;
    vector<Edge> edges;  
    
    int temp_root(int i, vector<int> &t_id) {
        while(i != t_id[i]){            
            t_id[i] = t_id[t_id[i]];            
            i = t_id[i];            
        }            
        return i;            
    }
    bool temp_find(pair<int,int> p) {
        vector <int> temp(id);
        return temp_root(p.first, temp) == temp_root(p.second, temp);
    }
    int root(int i){            
        while(i != id[i]){            
            id[i] = id[id[i]];            
            i = id[i];            
        }            
        return i;            
    }     
    bool find(pair<int,int> p){            
        return root(p.first) == root(p.second);            
    } 
    void unite(pair<int,int> p){            
        int i = root(p.first), j = root(p.second);            
        if(sz[i] < sz[j]){            
            id[i] = j;            
            sz[j] += sz[i];            
        }            
        else{            
            id[j] = i;            
            sz[i] += sz[j];            
        }            
    }     
};

int N,M;          
queue<pair<int,int>> q; 

int main(){
    cin >> N >> M;
    for (int i = 0; i < N; ++i) {
        int t;
        cin >> t;
        q.push(make_pair(i,t-1));  
    }
    Graph *g = new Graph(N,M);

    for (int i = 0; i < M; ++i) {
        int a,b,c;
        cin >> a >> b >> c;
        --a; --b;
        g->addEdge(a,b,c);    
    }  
    cout << g->solver(q) << endl;
    

    return 0;
}   