clc;
clear all;
close all;

pkg load statistics
pkg load queueing

lamda = 5;
utilization = [0,500];
server_response_time = [0,500];
average_number_of_requests = [0,500];
server_throughput = [0,500];

m = [5.1:0.01:10]; 

for i=1:columns(m)
    [utilization(i),server_response_time(i),average_number_of_requests(i),server_throughput(i)] = qsmm1(lamda, m(i));
endfor

figure(1); 
hold on;
title("Utilization based on m");
plot(m,utilization,"linewidth", 2.2);
xlabel("m");
ylabel("utilization"); 
hold off;

figure(2) ;
hold on;
title("server response time based on m");
plot(m,server_response_time,"linewidth", 2.2);
xlabel("m");
ylabel("server response time"); 
hold off;

figure(3) ;
hold on;
title("average number of requests based on m");
plot(m,average_number_of_requests,"linewidth", 2.2);
xlabel("m");
ylabel("average number of requests"); 
hold off;

figure(4);
hold on;
title("server throughput based on m");
plot(m,server_throughput,"linewidth", 2.2);
xlabel("m");
ylabel("server throughput");
hold off;
 
 
