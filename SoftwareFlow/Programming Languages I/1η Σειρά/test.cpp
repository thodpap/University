#include <iostream>
#include <algorithm>

using namespace std; 
/* sums: 0 42 ... */ 
int recursion(int start, int last, int sums[], int N, int M) {

	if (start >= last) return -1; // error

	int K = last - start + 1;
	int sum = 0;
	/* sum of the subsequence */  
	if (start - 1 < 0) sum = sums[last];
	else sum = sums[last] - sums[start - 1]; 

	// if (start == 0 && last == M - 1)
	if ((double)((double)sum / (double)(K * N)) <= -1.0) 
		return K; 
	int one = recursion(start + 1,last ,sums, N,M);
	int two = recursion(start, last - 1, sums, N, M);
	// cout << start << " " << last << " " << sum << " " << one << " " << two << endl;
    
	return max(one,two);
}

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

int anotherSolution2(int N,int M,int sums[]) {
	int ans = 0;
	for(int endingPoint = 1; endingPoint < M; ++endingPoint){
		for(int K = ans; K <= endingPoint; ++K) {
			int sum = sums[endingPoint] - sums[endingPoint - K - 1];
			if ( (double)((double)sum / (double)(K * N)) <= -1.0){
				ans = max(ans, K);
			}
		}
	}
	return ans;
}
int anotherSolution3(int N,int M,int sums[]) {
	int ans = 0;
	for(int K = 1; K < M; ++K) {
		for(int endingPoint = 0; endingPoint < M; ++endingPoint) { 
			int sum = sums[endingPoint] - sums[endingPoint - K - 1];
			if ( (double)((double)sum / (double)(K * N)) <= -1.0){
				ans = K;
			}
		}
	} 
	return ans;
}

int sums[1000];
int main() {
	int arr[] = {42, -10, 8, 1, 11, -6, -12, 16, -15, -11, 13};
	int N = 3;
	int M = 11;
	for(int i = 0; i < M; ++i) {
		sums[i] = arr[i] + sums[i-1]; 
	}

	cout << recursion(0,M-1,sums,N,M) << endl;

	dpSolution(0,M-1,sums,N,M);
	cout << dp[0][M-1] << endl; 
	cout << anotherSolution(N,M,sums) << endl;
	cout << anotherSolution2(N,M,sums) << endl;
	cout << anotherSolution3(N,M,sums) << endl;
	return 0;
}