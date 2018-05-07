% 3->2->1 neural network

%% signals from 2 classes
fs = 160;
dt = 1/fs;
StopTime = 1;
N = fs*StopTime;
t = (0:dt:StopTime-dt);
n_var = 0.01;


% alpha 7.5-13, beta >14
f = [10, 15, 20, 8, 18, 25];
a = [1.1, 0.8, 0.6, 0.8, 1.2, 0.8];

mav_d2 = zeros(1000,2);
mav_d3 = zeros(1000,2);
mav_d4 = zeros(1000,2);

% initialization
w1 = 2*rand(3,2) - 1;
w2 = 2*rand(2,1) - 1;
%x = zeros(3,1);
y1 = zeros(2,1);
y2 = 0;
phi = zeros(3,1);
a_var = zeros(3,1);
f_var = zeros(3,1);
data = zeros(1,N);
mu = 0.2;
err = zeros(2000,1);




%% training
for n = 1:2
    for k = 1:1000
    
        phi = 2*pi*rand(3,1);
        a_var = 0.2*randn(3,1);
        f_var = 0.1*randn(3,1);
        data = (a(3*n-2) + a_var(1,1))*sin(2*pi*(f(3*n-2) + f_var(1,1))*t + phi(1,1)) + ...
            (a(3*n-1) + a_var(2,1))*sin(2*pi*(f(3*n-1) + f_var(2,1))*t + phi(2,1)) + ...
            (a(3*n) + a_var(3,1))*sin(2*pi*(f(3*n) + f_var(3,1))*t + phi(3,1)) + ...
            sqrt(n_var)*randn(1,N);
    
        [c,l] = wavedec(data,4,'db4');
        [cd2,cd3,cd4] = detcoef(c,l,[2 3 4]);
        
        mav_d2(k,n) = mean(abs(cd2),2);
        mav_d3(k,n) = mean(abs(cd3),2);
        mav_d4(k,n) = mean(abs(cd4),2);
        
        x = [mav_d2(k,n); mav_d3(k,n); mav_d4(k,n)];
        y1 = sigmoid(w1'*x);
        y2 = sigmoid(w2'*y1);
        
        
        if n == 1 
            err(1000*(n-1)+k,1) = (0 - y2)^2;
            sig_k = (0 - y2).*y2.*(1 - y2);
            w_delta = mu*y1*sig_k; 
        else       
            err(1000*(n-1)+k,1) = (1 - y2)^2;
            sig_k = (1 - y2).*y2.*(1 - y2);
            w_delta = mu*y1*sig_k';
        end 
            w2 = w2 + w_delta;
            
            w_delta = mu*x*(sig_k*w2.*y1.*(1 - y1))';
            w1 = w1 + w_delta;
         
    end
end

plot(err);
%%
x = zeros(3,2000);
y = zeros(1,2000);
for i = 1:1000
    x(:,2*(i-1)+ 1) = [mav_d2(i,1); mav_d3(i,1); mav_d4(i,1)];
    y(1,2*(i-1)+ 1) = 0;
    x(:,2*i) = [mav_d2(i,2); mav_d3(i,2); mav_d4(i,2)];
    y(1,2*i) = 1;
end

Y = myNeuralNetworkFunction(x);


figure(1)
Y1 = Y(1:2:1000);
Y1(Y1<0.5) = 0;
plot([1:500],Y1,'ro',[1:500],zeros(1,500),'b-');
title('prediction for class 1 input');


figure(2)
Y2 = Y(2:2:1000);
Y2(Y2>0.5) = 1;
plot([1:500],Y2,'ro',[1:500],ones(1,500),'b-');
title('prediction for class 2 input');

