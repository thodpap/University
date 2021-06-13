clc;
clear all;


function [r, ergodic] = intensities(lambda,m)
  r(1) = lambda(1)/m(1);
  r(2) = (lambda(2) + 2/7 * lambda(1))/m(2);
  r(3) = (4/7 * lambda(1))/m(3);
  r(4) = (3/7 * lambda(1))/m(4);
  r(5) = (4/7 * lambda(1) + lambda(2))/m(5);
  ergodic = 1;
  display("Intensities:");
  for i = 1:5
    display(r(i));
    if (1 < r(i))
      ergodic = 0;
    endif
  endfor
  display(ergodic);
endfunction


function meanClients = mean_clients(lambda,m)
  [r, ergodic] = intensities(lambda,m);
  meanClients = r./(1-r)
endfunction

display("fucking 4 IAM HEREEEEEE");
lambda = [4,1];
m = [6,5,8,7,6];
meanClients = mean_clients(lambda,m);
mean_time = sum(meanClients)/sum(lambda);
display(mean_time); 
max_lambda = 6;
start = 0.1;

for i = 1:89
  l1 = start * max_lambda;
  to_plot(i) = l1;
  lambda = [l1,1];
  temp = mean_clients(lambda,m);
  mean_time_v(i) = sum(temp)/sum(lambda);
  start = start + 0.01;
endfor

figure(1);
plot(to_plot, mean_time_v, 'g', "linewidth", 1.2);
xlabel("Lambda");
ylabel("Mean Time in the system");