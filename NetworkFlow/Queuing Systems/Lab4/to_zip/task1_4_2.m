clc;
clear all;
close all;
pkg load queueing;

function res = erlangb_iterative (p,c)
  beta = 1;
  for i = 1:c
    beta = (p * beta)/((p * beta) + i);
  endfor
  res = beta;
endfunction

p1 = 200*(23/60);
xstate = 1:200;
for k = 1:200
  to_plot(k) = erlangb_iterative(p1,k);
endfor
figure(1);
hold on;
title("Probabilities per number of lines");
xlabel("Number of lines");
ylabel("Probability");
plot(xstate,to_plot,'g',"linewidth",1.2);

for i = 1:200 
  if (to_plot(i) < 0.01)
    minlines = i;
    display(minlines);
    break;
  endif
endfor
