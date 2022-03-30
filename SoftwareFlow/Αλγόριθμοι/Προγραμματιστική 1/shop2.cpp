#include <bits/stdc++.h>

using namespace std;

vector<int> arr;
int N,K;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> N >> K;

    for (int i = 0; i < N; ++i) {
        int temp;
        cin >> temp;
        arr.push_back(temp);
    }
    vector<int> iterators(N);
    vector<int> all_sums[N];

    int best = INT_MAX;

    unordered_map<int,int> sums;
    
    for (int i = 0; i < arr.size(); ++i) { 
        int sum = 0;
        for (int j = i; j < N; ++j) {
            sum += arr[j];
            if (sum > K) break;
            
            all_sums[i].push_back(sum);
            if (sum == K)  
                best = min(best, j - i + 1);

            if (sums.find(K - sum) != sums.end()) {
                best = min(best, j - i + 1 + sums[K - sum]); // update solution
            }
        }
        // store first row to sums
        for (int k = 0; k <= i; ++k) {
            if (iterators[k] + 1 <= all_sums[k].size()) {
                int sm = all_sums[k][iterators[k]];
                    
                if (sums.find(sm) != sums.end()) {
                    sums[sm] = min(sums[sm], iterators[k] + 1);
                } else {
                    sums[sm] = iterators[k] + 1; 
                }
                
                ++iterators[k];
            } 
        }
    }
    
    cout << (best != INT_MAX ? best : -1) << endl;
    return 0;
}