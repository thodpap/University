#include <bits/stdc++.h>

using namespace std;

#define dk_max 10001
#define sj_max 1000000001 

int N, dk = dk_max;
unsigned long Q;

vector<unsigned long> dist, query(dk_max, -1);
set<pair<unsigned long,int>> myQ;

void BFS();

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); 
    
    cin >> N >> Q;
    for(int i = 0; i < N; i++) {
        unsigned long di;
        cin >> di;
        dist.push_back(di);
        if(di < dk)
            dk = di;
    }

    query[0] = 0;
    myQ.insert( make_pair(query[0],0));

    BFS();
    while(Q--) {
        unsigned long q;
        cin >> q;
        (query[q % dk] > q) ? printf("NO\n") : printf("YES\n");
    }
}
 
void BFS() {
    while(!myQ.empty()) { 
        pair<unsigned long,int> head = *myQ.begin();
        unsigned long current = head.second;
        int dSum = head.first;
        myQ.erase(head);

        for(auto di : dist) {
            int newNode = (current+di) % dk;
            int newDist = dSum + di;

            if(newDist < query[newNode] || query[newNode] == -1) {
                myQ.erase( make_pair( query[newNode], newNode ) );
                query[newNode] = newDist;
                myQ.insert( make_pair( query[newNode], newNode ) );
            }
        }
    }
}