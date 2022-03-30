#include <bits/stdc++.h>
using namespace std;
using namespace std::chrono;


void readint(int &number)
{
    //variable to indicate sign of input number
    bool negative = false;
    register int c;
 
    number = 0;
 
    // extract current character from buffer
    c = getchar();
    if (c=='-')
    {
        // number is negative
        negative = true;
 
        // extract the next character from the buffer
        c = getchar();
    }
 
    // Keep on extracting characters if they are integers
    // i.e ASCII Value lies from '0'(48) to '9' (57)
    for (; (c>47 && c<58); c=getchar())
        number = number *10 + c - 48;
 
    // if scanned input has a negative sign, negate the
    // value of the input number
    if (negative)
        number *= -1;
}
void print(vector<int> v) {
    for (int i : v) {
        cout << i << " "; 
    }
    cout << "\n";
}
int ceil1(std::vector<int>& v, int l, int r, int key)
{
    int res = -1;
    //print(v);
    while (l <= r) {
        int m = l + (r - l) / 2;
        //cout << l << " " << r << " " << m << " " << key << "\n";
        if (v[m] > key) {
            res = m;
            l = m + 1;
         }
        else if (v[m] == key) {
            res = m-1;
            break;
        }
        else
            r = m - 1;
    }
    return res + 1;
}
int ceil2(std::vector<int>& v, int l, int r, int key)
{
    if(key < 0 ) return -1;
    int res = -1;
   // print(v);
    while (l <= r) {
        int m = l + (r - l) / 2;
        //cout << l << " " << r << " " << m << " " << key << "\n";
        if (v[m] < key) {
            res = m;
            l = m + 1;
         }
        else if (v[m] == key) {
            res = m-1;
            break;
        }
        else
            r = m - 1;
    }
    return res + 1;
}

vector<int> a(2e5 + 5, 0);


int main() {
    auto start = high_resolution_clock::now();
    string path = "input";
    int t;
    readint(t);
    path += to_string(t) + ".txt"; 
    freopen(path.c_str(), "r", stdin);
    int n,k;
    readint(n);
    readint(k);
    vector<int> lds(n);
    vector<int> rev;
    vector<int> lis(n);
    for(int i = 0; i < n; i++) {
        readint(a[i]);
        rev.push_back(a[i]);
    }
    reverse(rev.begin(), rev.end());
    vector<int> track_ld;
    int ans = 0;
    track_ld.push_back(rev[0]);
    lds[0] = 1;
    for(int i = 1; i < n; i++) {
       int len = track_ld.size();
       int temp = ceil1(track_ld, 0, len-1, rev[i]);
       if(rev[i] < track_ld[len-1]) {
           track_ld.push_back(rev[i]);
           lds[i] = temp + 1;
       }
    //    else if(temp == len) {
    //        track[temp-1] = a[i];
    //    }
       else {
           track_ld[temp] = rev[i];
           lds[i] = temp == 0 ? 1 : temp + 1;
       }
       ans = max(ans, lds[i]);
       //cout << lds[i] << "\n";
    }
    vector<int> track_lis;
    lis[0] = 1;
    track_lis.push_back(a[0]);
    for(int i = 1; i < n; i++) {
        int len = track_lis.size();
        int temp = ceil2(track_lis, 0, len-1, a[i] + k);
        ans = max(ans, temp + lds[n-i-1]);
        //cout << ans << " " << temp  << " " << lds[n-i-1] << "\n";
        temp = ceil2(track_lis,0,len-1, a[i]);
        if(a[i] > track_lis[len-1]) {
           track_lis.push_back(a[i]);
           lis[i] = temp + 1;
       }
    //    else if(temp == len) {
    //        track[temp-1] = a[i];
    //    }
       else {
           track_lis[temp] = a[i];
           lis[i] = temp == 0 ? 1 : temp + 1;
       }
    }
    //print(lds);
    //print(lis);
    cout << ans << "\n";
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    cout <<"test case : " << t << " " <<   duration.count() << "\n";
    string path2 = "output";
    path2 += to_string(t) + ".txt"; 
    freopen(path2.c_str(), "r", stdin);
    int real_answer;
    readint(real_answer);
    real_answer = (ans == real_answer)? 1 : 0;
    cout << t << ": " << real_answer << endl;
}