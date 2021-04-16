#include <iostream>

int main(int argc, char *argv[]){

    int N, start = 1, lenght = -1;
    std::cin >> N;
    std::vector<int> v(N), prefix_sum(N+1), best(N+1);

    prefix_sum[0] = 0;
    for(int i=1; i<N+1; ++i){
        std::cin >> v[i-1];
        prefix_sum[i] = prefix_sum[i-1] + v[i-1];
    }

    best[N] = prefix_sum[N];
    for(int i=N-1; i>-1; --i)
        best[i] = std::max(best[i+1], prefix_sum[i]);

    for(int end=1; end<N+1; ++end){
        if(best[end] >= prefix_sum[start-1])
            lenght = std::max(length, end-start+1;
        else ++start;
    }

    std::cout << lenght << "\n";

    return 0;
} 
