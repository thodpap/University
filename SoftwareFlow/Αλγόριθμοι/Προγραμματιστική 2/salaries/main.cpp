#include <bits/stdc++.h>  
  
using namespace std;  
  
int N;
uint32_t K, ans;  
vector<uint32_t> arr, reversed, lis2, stackLis, stackLis2;   
   
int binary(int rev, int i, uint32_t K, vector<uint32_t> &arr, vector<uint32_t> &stack) { 
    int start = 0;  
    int last = stack.size();  
    int res = -1;  
    while(start < last) {  
        int mid = (start + last)/2;   
        if ((rev == 0 && arr[i] + K <= stackLis[mid]) || (rev == 1 && stack[mid] <= arr[i])) {  
            res = mid;  
            last = mid;  
        } else   
            start = mid + 1;   
    }    
    return res;
}
void update(int res, vector<uint32_t> &stack, vector<uint32_t> &arr, int i, int rev) {
    if (res == -1) {  
        stack.push_back(arr[i]);  
    
        if (rev == 1)
            lis2.push_back( stackLis2.size() );  
    } else {  
        stack[res] = arr[i];  

        if (rev == 1)
            lis2.push_back(res + 1);  
    }   
}
int main() {  
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);  

    for (int test = 9; test <= 9; ++test) {
        arr.clear();
        reversed.clear(); 
        lis2.clear();
        stackLis.clear();
        stackLis2.clear();
        ans = 0;
        string path = "./testcases/input";
        path += to_string(test) + ".txt"; 
        freopen(path.c_str(), "r", stdin);
 
        clock_t begin = clock();  
        cin >> N >> K;  
            
        for (int i = 0; i < N; ++i) {  
            uint32_t t;  
            cin >> t;   
            arr.push_back(t);   
            reversed.push_back(t);   
        }    

        reverse(reversed.begin(), reversed.end());   
        stackLis2.push_back(reversed[0]);   
            
        lis2.push_back(1);  
             
        int count = 0;
        double time = 0.0;
        double btime = 0.0;
        for (int i = 1; i < N; ++i) {    
            int res = binary(1, i, 0, reversed, stackLis2);      
            update(res, stackLis2, reversed, i, 1); 
            ans = max(ans, lis2[i]);   
        }    

        reverse(lis2.begin(), lis2.end());   

        // cout << ans << "\n"; 
        freopen("nine.txt","w", stdout);


        for (int i = 0; i < N; ++i) {   
            int res = binary(0, i, K, arr, stackLis);  
            int temp = (res == -1) ? stackLis.size() : res;  
            ans = max(ans, temp + lis2[i]);  
            
            cout << i << "," << ans << "," << res << "," << temp << "," << lis2[i] << endl;
            
            res = binary(0, i, 0, arr, stackLis);   
            update(res, stackLis, arr, i, 0);

            temp = (res == -1) ? stackLis.size() : (res + 1);               
        }   
        
        // printf("Last time: %.6f\n", (double)(clock() - begin) / CLOCKS_PER_SEC); 
    }
    return 0;  
}  