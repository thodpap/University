#include <iostream>
#include <cstdio>
#include <algorithm>
#include <vector> 

using namespace std; 

int N,M; 
int arr[500005];
int sums[500005];   
 
int main(int argc, char **argv) { 
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	
	FILE *file;
	file = freopen(argv[1], "r", stdin);
	cin >> M >> N;
	for (int i = 0; i < M; ++i) cin >> arr[i];

	int ans = 0; 
	for (int i = 0; i < M; ++i) {
		sums[i] = sums[i-1]+ arr[i] + N; 
	}    
	vector<pair<long long,int>> max_from_right, min_from_left;

	int max_so_far = 0;
	int min_so_far = sums[M-1];


	max_from_right.push_back(make_pair(max_so_far,-1));
	min_from_left.push_back(make_pair(min_so_far, M-1));

	for (int i = 1; i < M; ++i) {
		if (sums[i] > max_so_far) {
			max_so_far = sums[i];
			max_from_right.push_back(make_pair(max_so_far,i));
		}
	}
	for (int i = M - 2; i >= 0; --i) {
		if (sums[i] < min_so_far) {
			min_so_far = sums[i];
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

	cout << ans << endl;
	
    fclose(file);
	return 0;
} 
