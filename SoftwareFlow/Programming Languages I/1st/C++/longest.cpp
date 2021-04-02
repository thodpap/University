#include <iostream>
#include <cstdio>
#include <algorithm>
#include <map>
#include <vector>

using namespace std; 

int arr[500005];
int N,M;
int recursion(int start, int last, int sums[], int N, int M) {
	if (start >= last) return -1; // error

	int K = last - start + 1;
	int sum = 0;
	/* sum of the subsequence */  
	if (start - 1 < 0) sum = sums[last];
	else sum = sums[last] - sums[start - 1]; 

	if ((double)((double)sum / (double)(K * N)) <= -1.0) 
		return K; 

	int one = recursion(start + 1,last ,sums, N,M);
	int two = recursion(start, last - 1, sums, N, M); 
    
	return max(one,two);
}
int sums[10000];
int dp[1000][1000]; 
void dpSolution(int start, int last, int sums[], int N, int M) {
	if (start >= last) return ;

	int K = last - start + 1;
	int sum = 0;
	
	if (dp[start][last] > 0) {
		return ;
	}
	/* sum of the subsequence */  
	if (start - 1 < 0) sum = sums[last];
	else sum = sums[last] - sums[start - 1]; 

	// if (start == 0 && last == M - 1)
	if ((double)((double)sum / (double)(K * N)) <= -1.0){
		dp[start][last] = K; 
	} else {
		dpSolution(start + 1,last ,sums, N,M);
		dpSolution(start, last - 1, sums, N,M);
		dp[start][last] = max(dp[start+1][last], dp[start][last -1]);
	} 
}  

int anotherSolution(int N,int M, int sums[]) {
	int ans = 0;
	for (int i = 0; i < M; ++i) {
		for (int j = i; j < M; ++j) { 
			if ( (double)((double)(sums[j] - sums[i-1]) / (double)((j - i + 1) * N)) <= -1.0){
				ans = max(ans, j - i + 1); 
			}				 
		}
	}
	return ans;
}  
int nSolution() {
	vector<pair<int,int>> highs,lows;
	for (int i = 0; i < M; ++i) {
		sums[i] = sums[i-1] + arr[i];
		cout << sums[i] << " ";
	}cout << endl;

	int high = sums[0];
	int low = sums[M-1];
	highs.push_back(make_pair(high,0));
	lows.push_back(make_pair(low,M-1));

	for (int i = 0; i < M; ++i) 
		if (sums[i] > high) {
			high = sums[i];
			highs.push_back(make_pair(high,i));
		}
	for (int i = M-1; i >= 0; --i) 
		if (sums[i] < low) {
			low = sums[i];
			lows.push_back(make_pair(low,i));
		}
		
	int ans = 0;
	for (auto h:highs) {
		for (auto l:lows) {
			if (l.second > l.first) continue;
			if (l.first - h.first <= (h.second - l.second ) * N) 
				ans = max(ans, l.second - h.second);
		}
	}
	return ans;
}
 
int logarithmicSolution(int N,int M, int arr[]) {
	map<int,int> sums;
	sums[0] = 0; // empty -> have the whole sums map
	int sum = 0, ans = 0;

	for(int i = 1; i <= M; ++i) {
		sum += arr[i-1];

		if (sum <= -i * N) {
			cout << i << endl;
			ans = i;
		} 
		else {
			// sum - sums[min(k)] <= -(i - k) * N 
			// sums[k] > sum + (i-k) * N > sum + (ans + 1) * N - 1

			auto upper = sums.upper_bound(sum + (ans+1) * N - 1);
			
			for (auto u = upper; u != sums.end(); ++u)
				if (sum - u->first <= - N * (i - u->second)) 
					ans = max(ans, i - u->second);  
		}
		sums[sum] = i;
	}
	return ans;
}
int main(int argc, char **argv) {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	
	FILE *file;
	file = freopen(argv[1], "r", stdin);
	cin >> M >> N;
	for (int i = 0; i < M; ++i) cin >> arr[i];

	for(int i = 0; i < M; ++i) {
		sums[i] = arr[i] + sums[i-1]; 
	}
		
	cout << logarithmicSolution(N,M-1,arr) << endl;
	cout << nSolution() << endl;
	fclose(file);
	return 0;
}

// Code for recursion
// for(int i = 0; i < M; ++i) {
// 	sums[i] = arr[i] + sums[i-1]; 
// }

// cout << recursion(0,M-1,sums,N,M) << endl;

