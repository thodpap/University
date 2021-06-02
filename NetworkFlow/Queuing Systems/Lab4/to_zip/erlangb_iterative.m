clc;
clear all;
close all;
pkg load queueing;

function res = erlangb_iterative (p,c)
  beta = 1;
  arr = zeros(length(c));
  figure_counter = 0;
  result = 0;
  counter = 0
  for j=1:length(c)
    for i = 1:c(j)
      beta = (p * beta)/((p * beta) + i);
    endfor
    if beta < 0.01 && counter == 0
     result = c(j)
     counter += 1
    endif
    arr(j) = beta;
  endfor
  %-----------------------------------
  %for first iterative
  res = beta; 
  checkres = erlangb(p,c);
  display(checkres); 
  %--------------------------------- 
  
  disp("minimuc c is:")
  disp(result)
  %-----------------------------------
  
  
  
endfunction