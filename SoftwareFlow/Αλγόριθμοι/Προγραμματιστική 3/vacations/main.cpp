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
    
    Graph *mst() { 
        Graph *g = new Graph(this->N, this->M);

        std::sort(edges.begin(), edges.end(),
          [](Edge const & a, Edge const & b) -> bool
          { return a.getWeight() < b.getWeight(); } );   

        int i = 0, count = 0;
        while ( i < this->M && count < this->N - 1 ) {
            pair<int,int> p = make_pair(
                edges[i].getNodes().first,
                edges[i].getNodes().second
            );
            
            if (!find(p)) {
                unite(p);
                g->addEdge(edges[i].getNodes().first, edges[i].getNodes().second, edges[i].getWeight());
                ++count;
            }
            ++i;
        } 

        return g;
    } 
    vector<vector<int>> dfs_start() {
        vector<vector<int>> A; //(this->N, vector<int>(this->N, INT_MAX));
        
        vector<vector<pair<int,int>>> edges(this->N); 
        // fill edges vector
        for (auto e: this->edges) {
            edges[e.getNodes().first].push_back(make_pair(e.getNodes().second, e.getWeight()));
            edges[e.getNodes().second].push_back(make_pair(e.getNodes().first, e.getWeight()));
        }


        for (int u = 0; u < this->N; ++u) {
            vector<int> parent;
            vector<bool> visited;
            vector<int> bottleneck;
            for (int i = 0; i < this->N; ++i) {
                parent.push_back(i);
                visited.push_back(false);
                bottleneck.push_back(INT_MAX);
            }
            bottleneck[u] = 0;
            dfs(u, edges, parent, visited, bottleneck); 

            A.push_back(bottleneck);
        }
        return A;
    }

    void print() {
        for (auto e: edges) {
            cout << e.getWeight() << " " << e.getNodes().first << " " << e.getNodes().second << endl;
        } 
    }
    
private:
int N,M;
    vector<int> id, sz;
    vector<Edge> edges;  
    int temp_root(int k) {
        // if k is not root then find should return find of parent
        if(id[k] !=k) {
            id[k] = temp_root(id[k]);
        }
        return id[k];
    } 
    bool temp_find(pair<int,int> p) { 
        return temp_root(p.first) == temp_root(p.second);
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
    void dfs(int u, vector<vector<pair<int,int>>> &edges, vector<int> &parent, vector<bool> &visited, vector<int> &bottleneck) {
        visited[u] = true; 
        for (auto e: edges[u]) { 
            if(!visited[e.first]) {
                parent[e.first] = u;
                bottleneck[e.first] = max(bottleneck[u], e.second);
                dfs(e.first, edges, parent, visited,bottleneck);
            }
        }
    }
};

int N,M,Q;

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); 
    
    cin >> N >> M;
    Graph *g = new Graph(N,M);

    for (int i = 0; i < M; ++i) {
        int x,y,d;
        cin >> x >> y >> d;

        --x;
        --y; 
        g->addEdge(x,y,d);
    }

    Graph *graph = g->mst(); 
    vector<vector<int>>A = graph->dfs_start();  

    cin >> Q;
    vector<int> ans; 
    for(int k = 0; k < Q; ++k) {
        int u,v;
        cin >> u >> v; 
        --u;
        --v;
        ans.push_back(A[u][v]);
    }
    for (auto a: ans) {
        cout << a << endl;
    } 

    return 0;
}   
