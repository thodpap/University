% M/M/1 simulation. We will find the probabilities of the first states.
% Note: Due to ergodicity, every state has a probability >0.

clc;
clear all;
close all;
 
figure_counter = 0
for lambda = [1,5,10]  
  arrivals = [0,0,0,0,0,0,0,0,0,0,0];
  total_arrivals = 0; % to measure the total number of arrivals
  current_state = 0;  % holds the current state of the system
  previous_mean_clients = 0; % will help in the convergence test
  index = 0;
  mu = 5;
  threshold = lambda/(lambda + mu); % the threshold used to calculate probabilities

  transitions = 0; % holds the transitions of the simulation in transitions steps

  while transitions >= 0
    transitions = transitions + 1; % one more transitions step
    
    if mod(transitions,1000) == 0 % check for convergence every 1000 transitions steps
      index = index + 1;
      for i=1:1:length(arrivals)
        display(total_arrivals);
          P(i) = arrivals(i)/total_arrivals; % calculate the probability of every state in the system
      endfor
      
      mean_clients = 0; % calculate the mean number of clients in the system
      for i=1:1:length(arrivals)
         mean_clients = mean_clients + (i-1).*P(i);
      endfor
      
      to_plot(index) = mean_clients;
          
      if abs(mean_clients - previous_mean_clients) < 0.00001 || transitions > 1000000 % convergence test
        break;
      endif
      
      previous_mean_clients = mean_clients;
      
    endif
    
    random_number = rand(1); % generate a random number (Uniform distribution)
    
    % Change it
    if current_state == 0 || random_number < threshold % arrival
      x = arrivals(current_state + 1) + 1;
      arrivals(current_state + 1) = x;
      
      if (current_state != 10)
         current_state = current_state + 1;
      endif
    else 
      if current_state != 0 % no departures from an empty system
        current_state = current_state - 1;
      endif
    endif
  endwhile

  for i=1:1:length(arrivals)
    display(P(i));
  endfor

  figure_counter += 1;
  figure(figure_counter);
  plot(to_plot,"r","linewidth",1.3);
  title(strjoin({"Average number of clients in the M/M/10 queue: Convergence for lambda = ", num2str(lambda)}));
  xlabel("transitions in thousands");
  ylabel("Average number of clients"); 
  
  saveas (1, strjoin({"figure_",num2str(1),"_lambda_",num2str((lambda)),".png"},""));
  
  figure_counter += 1
  figure(figure_counter);
  bar(P,'r',0.4);
  title("Probabilities")
  title(strjoin({"Probabilities for lambda = ", num2str(lambda)}));
  saveas (2, strjoin({"figure_",num2str(2),"_lambda_",num2str((lambda)),".png"},""));
  
  clc;
  clear all;
  close all;
endfor