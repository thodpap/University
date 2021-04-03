#include <iostream>
#include <cstdio>
#include <algorithm>
using namespace std;

char arr[1000][1000];
int visited[1000][1000];
int N,M;
int counter;

void find_parents(int i,int j) {
	visited[i][j] = 1;
	++counter;
	// there are 4 possible parents 
	if (j >= 1 && !visited[i][j-1] && arr[i][j-1] == 'R')
		find_parents(i,j - 1);
	if (j < M  && !visited[i][j+1] && arr[i][j+1] == 'L')
		find_parents(i,j + 1);
	if (i >= 1 && !visited[i-1][j] && arr[i-1][j] == 'D')
		find_parents(i - 1,j);
	if (i < N  && !visited[i+1][j] && arr[i+1][j] == 'U')
		find_parents(i + 1,j);
}

void dfs() {
	int p,q;

	/* i = 0   and j 	     */
	p = 0;
	for(int j = 0; j < M; ++j) 
		if (arr[p][j] == 'U' && !visited[p][j]) 
			find_parents(p,j);

	/* i = N-1 and j 	     */
	p = N-1;
	for (int j = 0; j < M; ++j) 
		if (arr[p][j] == 'D' && !visited[p][j]) 
			find_parents(p,j);

	/* i 	   and j = 0 	 */
	q = 0;
	for (int i = 0; i < N; ++i) 
		if (arr[i][q] == 'L' && !visited[i][q]) 
			find_parents(i,q);

	/* i 	   and j = M - 1 */
	q = M - 1;
	for (int i = 0; i < M; ++i) 
		if (arr[i][q] == 'R' && !visited[i][q]) 
			find_parents(i,q);
			
} 
int main(int argc,char **argv){
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	
	FILE *file;
	file = freopen(argv[1], "r", stdin);

	cin >> N >> M;
	for(int i = 0; i < N; ++i) 
		for (int j = 0; j < N; ++j) 
			cin >> arr[i][j];
	dfs();
	cout << (N*M - counter) << endl;

	fclose(file);
	return 0;
}