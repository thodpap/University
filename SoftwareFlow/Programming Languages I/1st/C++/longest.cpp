#include <iostream>
#include <cstdio>
#include <algorithm>
#include <map>
#include <vector>
#include <time.h>
using namespace std; 

int arr[500005];
int N,M;
int recursion(int start, int last, int sums[]) {
	if (start >= last) return -1; // error

	int K = last - start + 1;
	int sum = 0;
	/* sum of the subsequence */  
	if (start - 1 < 0) sum = sums[last];
	else sum = sums[last] - sums[start - 1]; 

	if ((double)((double)sum / (double)(K * N)) <= -1.0) 
		return K; 

	int one = recursion(start + 1,last ,sums);
	int two = recursion(start, last - 1, sums); 
    
	return max(one,two);
}
int sums[10000];
int dp[50000][500000]; 
void dpSolution(int start, int last, int sums[]) {
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
	if (sum  <= -(K * N)){
		dp[start][last] = K; 
	} else {
		dpSolution(start + 1,last ,sums);
		dpSolution(start, last - 1, sums);
		dp[start][last] = max(dp[start+1][last], dp[start][last -1]);
	} 
}  
int anotherSolution(int N,int M, int sums[]) {
	int ans = 0;
	for (int i = 0; i < M; ++i) {
		for (int j = M-1; j > i; --j) { 
			if (sums[j] - sums[i-1] <= -(j-i+1) * N) {
				ans = max(ans, j - i + 1); 
				break;
			}
		}
	} 
	return ans;
}   

int sums_n[500005];
int linearSolution(int N,int M,int arr[]) { 
	int ans = 0; 
	for (int i = 0; i < M; ++i) {
		sums_n[i] = sums_n[i-1]+ arr[i] + N; 
	}    
	vector<pair<long long,int>> max_from_right, min_from_left;

	int max_so_far = 0;
	int min_so_far = sums_n[M-1];


	max_from_right.push_back(make_pair(max_so_far,-1));
	min_from_left.push_back(make_pair(min_so_far, M-1));

	for (int i = 1; i < M; ++i) {
		if (sums_n[i] > max_so_far) {
			max_so_far = sums_n[i];
			max_from_right.push_back(make_pair(max_so_far,i));
		}
	}
	for (int i = M - 2; i >= 0; --i) {
		if (sums_n[i] < min_so_far) {
			min_so_far = sums_n[i];
			min_from_left.push_back(make_pair(min_so_far,i));
		}
	}  
	auto i = max_from_right.begin();
	auto j = min_from_left.rbegin();

	while(i != max_from_right.end() && j != min_from_left.rend()) {
		if (j->first <= i->first) {
			while (j + 1 != min_from_left.rend() && (j+1)->first <= i->first) 
				++j;
			ans = max(ans, j->second - i->second);
			++i;
			++j;
		} 
		else if (i->second <  j->second - 1)
			++i;
		else 
			j++;

	}

	return ans;
}

 
int main(int argc, char **argv) {
    clock_t tStart = clock();
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	
	FILE *file;
	file = freopen(argv[1], "r", stdin);
	cin >> M >> N;
	for (int i = 0; i < M; ++i) cin >> arr[i];

	// for(int i = 0; i < M; ++i) {
	// 	sums[i] = arr[i] + sums[i-1]; 
	// } 
	// cout << "N^2 = " << anotherSolution(N,M,sums) << endl;
	// dpSolution(0,M-1,sums);
	// cout << "DP = " << dp[0][M-1] << endl; 
	cout << "N = " << linearSolution(N,M,arr) << endl;
	fclose(file);
	printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
    
	return 0;
} 
