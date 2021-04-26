clc;
clear all;
close all;

pkg load statistics
pkg load queueing

lambda = 5;
m = 10;
states = [0, 1, 2, 3, 4]; % system with capacity 4 states
% the initial state of the system. The system is initially empty.
initial_state = [1, 0, 0, 0, 0];

% define the birth and death rates between the states of the system.
births_B = [lambda, lambda/2, lambda/3, lambda/4];
deaths_D = [m, m, m, m];

% get the transition matrix of the birth-death process
transition_matrix = ctmcbd(births_B, deaths_D);
display (transition_matrix)

# (ii)
% get the ergodic probabilities of the system
P = ctmc(transition_matrix);
display (P);
figure(1);
hold on;
title("Bar of Probabilities per state")
xlabel("State")
ylabel("Probability")
bar(states, P, "b", 0.5);
grid on; 
hold off;
# (iii)
display( " Average Number of customers in the system : ")
display( sum(P.*[0,1,2,3,4]))

# (iv)
display( " Probability of blocking a customer :")
display( P(5) )

%P[Blocking]

P_Blocking = P(5);
display(P_Blocking)
 
index = 0;
for T = 0 : 0.01 : 50
  index = index + 1;
  Po = ctmc(transition_matrix, T, initial_state);
  Prob0(index) = Po(1);
  Prob1(index) = Po(2);
  Prob2(index) = Po(3);
  Prob3(index) = Po(4);
  Prob4(index) = Po(5);
  if Po - P < 0.01
    break;
  endif
endfor

T = 0 : 0.01 : T;
figure(2);
title(strjoin({"lambda = ",num2str(lambda)," and m = ",num2str(m)})) 
xlabel("Time(sec)") 
hold on;
plot(T, Prob0, "r", "linewidth", 1.5);
plot(T, Prob1, "b", "linewidth", 1.5);
plot(T, Prob2, "k", "linewidth", 1.5);
plot(T, Prob3, "g", "linewidth", 1.5);
plot(T, Prob4, "m", "linewidth", 1.5);
legend("State : 0","State : 1","State : 2","State : 3","State : 4");
grid on; 
hold on;


m = [1,5,20]; 
for i=1:columns(m)
  deaths_D = [m(i), m(i), m(i), m(i)];
  transition_matrix = ctmcbd(births_B, deaths_D);
  index = 0;
  for T = 0 : 0.01 : 4
    index = index + 1;
    P0 = ctmc(transition_matrix, T, initial_state);
    Prob0(index) = P0(1);
    Prob1(index) = P0(2);
    Prob2(index) = P0(3);
    Prob3(index) = P0(4);
    Prob4(index) = P0(5);
    if P0 - P < 0.01
      break;
    endif
  endfor


  T = 0 : 0.01 : T;
  figure(i+2);
  title(strjoin({"lambda = ",num2str(lambda)," and m = ",num2str(m(i))}))
  xlabel("Time(sec)")
  ylabel("Probability")
  hold on;
  plot(T, Prob0, "r", "linewidth", 1.5);
  plot(T, Prob1, "g", "linewidth", 1.5);
  plot(T, Prob2, "b", "linewidth", 1.5);
  plot(T, Prob3, "k", "linewidth", 1.5);
  plot(T, Prob4, "m", "linewidth", 1.5);
  legend("State : 0","State : 1","State : 2","State : 3","State : 4");
  grid on; 
  hold off;
endfor
