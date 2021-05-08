% M/M/1 simulation. We will find the probabilities of the first states.
% Note: Due to ergodicity, every state has a probability >0.

clc;
clear all;
close all;

figure_counter = 0; 
rand('seed',12163);

for lambda = [1,5,10] 
  arrivals = [0,0,0,0,0,0,0,0,0,0,0]
  mu = 5;
  total_arrivals = 0; % to measure the total number of arrivals
  current_state = 0;  % holds the current state of the system
  previous_mean_clients = 0; % will help in the convergence test
  index = 0;
  threshold = lambda/(lambda + mu); % the threshold used to calculate probabilities

  transitions = 0; % holds the transitions of the simulation in transitions steps
  tracem_i = 0;
  tracem = []; 
  to_plot = [];
  while transitions >= 0
    transitions = transitions + 1; % one more transitions step
    
    tracem_i = tracem_i + 1;
    if tracem_i > 0 && tracem_i < 31 %&& current_state > 0
      tracem(tracem_i,1) = tracem_i;
      tracem(tracem_i,2) = current_state;
      tracem(tracem_i,3) = arrivals(current_state+1);
    endif 
      
    if mod(transitions,1000) == 0 % check for convergence every 1000 transitions steps
      index = index + 1;
      for i=1:1:length(arrivals)
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
        if current_state == 0 || random_number < threshold % arrival
            %{
            if 0 < tracem_i < 31
                tracem(tracem_i,4) = 1
                %disp("arrival"), disp(current_state);
            endif 
            %}
            total_arrivals = total_arrivals + 1;
            % to catch the exception if variable arrivals(i) is undefined. Required only for systems with finite capacity.
            x = arrivals(current_state + 1) + 1;
            arrivals(current_state + 1) = x; % increase the number of arrivals in the current state
            if (current_state != 10) 
                current_state = current_state + 1;
            endif
            else % departure
            %{
            if 0 < tracem_i < 31
                tracem(tracem_i,5) = 1 
            endif
            %}
            if current_state != 0 % no departure from an empty system
            current_state = current_state - 1;
            endif
        endif
        

  endwhile

  for i=1:1:length(arrivals)
    display(P(i));
  endfor

  figure_counter += 1;
  figure(figure_counter);
  plot(to_plot,"b","linewidth",2);
  title(strjoin({"Average number of clients in the M/M/1/10 queue: Convergence for Lambda = ",num2str((lambda))},""));
  xlabel("Transitions in thousands");
  ylabel("Average number of clients");
  grid on;
  saveas (figure_counter, strjoin({"figure_",num2str(1),"_lambda_",num2str((lambda)),".png"}))
  
  figure_counter += 1;
  figure(figure_counter);
  bar(0:1:(length(arrivals)-1),P,'b',0.4);
  title(strjoin({"Probabilities for Lambda = ",num2str((lambda))}));
  grid on;
  saveas (figure_counter, strjoin({"figure_",num2str(2),"_lambda_",num2str((lambda)),".png"}))
  
  
  disp("trans state num_ar arr dep");
  disp(tracem);
    
endfor