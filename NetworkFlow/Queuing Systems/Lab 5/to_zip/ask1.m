clc;
clear all;
close all;

a = 0.001:0.001:0.999;
m1 = 14648.43;
m2 = 11718.75;
lambda = 10000;
fact1 = a./(m1 - a*lambda);
fact2 = (1-a)./(m2 - (1 - a)*lambda);
mean_time = fact1 + fact2;
figure(1);
plot(a, mean_time, 'g', "linewidth", 1.2);
ylabel("Mean time of delay");
xlabel("Values of a");
[min_t, ind] = min(mean_time);
display(min_t);
a_min = ind/1000;
display(a_min);