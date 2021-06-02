
clc;
clear all;
close all;


pkg load queueing

function erlangb_factorial(r, c)
  nominator = (r^c)/factorial(c)
  Pblock = 0;
  denominator = 0;
  for k=0:c
    denominator = (denominator + (r^(k))/factorial(k));
  endfor
  
  Pblock = nominator/denominator;
  
  disp("On hand Pblocking")
  disp(Pblock)
  
  Pblocking = erlangb(r, c);
  
  disp("erlangb Pblocking")
  disp(Pblocking)
  
endfunction
