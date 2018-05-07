%% feature 1
f1 = 10; %alpha
f2 = 15; %beta
f3 = 20; %beta
a1 = 1.1;
a2 = 0.8;
a3 = 0.6;

fs = 160;
dt = 1/fs;
StopTime = 1;
t = (0:dt:StopTime-dt);
n_var = 0.01;

% preallocation
rms_d2_f1 = zeros(100,1);
rms_d3_f1 = zeros(100,1);
rms_d4_f1 = zeros(100,1);

mav_d2_f1 = zeros(100,1);
mav_d3_f1 = zeros(100,1);
mav_d4_f1 = zeros(100,1);

var_d2_f1 = zeros(100,1);
var_d3_f1 = zeros(100,1);
var_d4_f1 = zeros(100,1);

aac_d2_f1 = zeros(100,1);
aac_d3_f1 = zeros(100,1);
aac_d4_f1 = zeros(100,1);

for i = 1:100
    phi = 2*pi*rand(3,1);
    a_var = 0.2*randn(3,1);
    f_var = 0.1*randn(3,1);

    data = (a1 + a_var(1,1))*sin(2*pi*(f1 + f_var(1,1))*t + phi(1,1)) + ...
        (a2 + a_var(2,1))*sin(2*pi*(f2 + f_var(2,1))*t + phi(2,1)) + ...
        (a3 + a_var(3,1))*sin(2*pi*(f3 + f_var(3,1))*t + phi(3,1)) + ...
        sqrt(n_var)*randn(1,fs*StopTime);

%dwtmode('per');
    [c,l] = wavedec(data,4,'db4');
    [cd2,cd3,cd4] = detcoef(c,l,[2 3 4]);

    rms_d2_f1(i,1) = sqrt(sum(cd2.^2)/length(cd2));
    rms_d3_f1(i,1) = sqrt(sum(cd3.^2)/length(cd3));
    rms_d4_f1(i,1) = sqrt(sum(cd4.^2)/length(cd4));
    
    mav_d2_f1(i,1) = sum(abs(cd2))/length(cd2);
    mav_d3_f1(i,1) = sum(abs(cd3))/length(cd3);
    mav_d4_f1(i,1) = sum(abs(cd4))/length(cd4);
    
    var_d2_f1(i,1) = var(cd2);
    var_d3_f1(i,1) = var(cd3);
    var_d4_f1(i,1) = var(cd4);
    
    change_d2 = cd2(2:end) - cd2(1:end-1);
    aac_d2_f1(i,1) = sum(abs(change_d2))/length(change_d2);
    change_d3 = cd3(2:end) - cd3(1:end-1);
    aac_d3_f1(i,1) = sum(abs(change_d3))/length(change_d3);
    change_d4 = cd4(2:end) - cd4(1:end-1);
    aac_d4_f1(i,1) = sum(abs(change_d4))/length(change_d4);
end

%% feature 2
f1 = 8; %alpha
f2 = 18; %beta
f3 = 25; %beta
a1 = 0.8;
a2 = 1.2;
a3 = 0.8;

fs = 160;
dt = 1/fs;
StopTime = 1;
t = (0:dt:StopTime-dt);
n_var = 0.01;

% preallocation
rms_d2_f2 = zeros(100,1);
rms_d3_f2 = zeros(100,1);
rms_d4_f2 = zeros(100,1);

mav_d2_f2 = zeros(100,1);
mav_d3_f2 = zeros(100,1);
mav_d4_f2 = zeros(100,1);

var_d2_f2 = zeros(100,1);
var_d3_f2 = zeros(100,1);
var_d4_f2 = zeros(100,1);

aac_d2_f2 = zeros(100,1);
aac_d3_f2 = zeros(100,1);
aac_d4_f2 = zeros(100,1);

for i = 1:100
    phi = 2*pi*rand(3,1);
    a_var = 0.2*randn(3,1);
    f_var = 0.1*randn(3,1);

    data = (a1 + a_var(1,1))*sin(2*pi*(f1 + f_var(1,1))*t + phi(1,1)) + ...
        (a2 + a_var(2,1))*sin(2*pi*(f2 + f_var(2,1))*t + phi(2,1)) + ...
        (a3 + a_var(3,1))*sin(2*pi*(f3 + f_var(3,1))*t + phi(3,1)) + ...
        sqrt(n_var)*randn(1,fs*StopTime);

%dwtmode('per');
    [c,l] = wavedec(data,4,'db4');
    [cd2,cd3,cd4] = detcoef(c,l,[2 3 4]);

    rms_d2_f2(i,1) = sqrt(sum(cd2.^2)/length(cd2));
    rms_d3_f2(i,1) = sqrt(sum(cd3.^2)/length(cd3));
    rms_d4_f2(i,1) = sqrt(sum(cd4.^2)/length(cd4));
    
    mav_d2_f2(i,1) = sum(abs(cd2))/length(cd2);
    mav_d3_f2(i,1) = sum(abs(cd3))/length(cd3);
    mav_d4_f2(i,1) = sum(abs(cd4))/length(cd4);
    
    var_d2_f2(i,1) = var(cd2);
    var_d3_f2(i,1) = var(cd3);
    var_d4_f2(i,1) = var(cd4);
    
    change_d2 = cd2(2:end) - cd2(1:end-1);
    aac_d2_f2(i,1) = sum(abs(change_d2))/length(change_d2);
    change_d3 = cd3(2:end) - cd3(1:end-1);
    aac_d3_f2(i,1) = sum(abs(change_d3))/length(change_d3);
    change_d4 = cd4(2:end) - cd4(1:end-1);
    aac_d4_f2(i,1) = sum(abs(change_d4))/length(change_d4);
end

%%
figure(1)
subplot(3,1,1)
plot([1:100],rms_d2_f1,'b-',[1:100],rms_d2_f2,'r-');
title('RMS');
legend('feature 1','feature 2');
ylabel('rms-d2');

subplot(3,1,2)
plot([1:100],rms_d3_f1,'b-',[1:100],rms_d3_f2,'r-');
ylabel('rms-d3');

subplot(3,1,3)
plot([1:100],rms_d4_f1,'b-',[1:100],rms_d4_f2,'r-');
ylabel('rms-d4');

figure(2)
subplot(3,1,1)
plot([1:100],mav_d2_f1,'b-',[1:100],mav_d2_f2,'r-');
title('MAV');
legend('feature 1','feature 2');
ylabel('mav-d2');

subplot(3,1,2)
plot([1:100],mav_d3_f1,'b-',[1:100],mav_d3_f2,'r-');
ylabel('mav-d3');

subplot(3,1,3)
plot([1:100],mav_d4_f1,'b-',[1:100],mav_d4_f2,'r-');
ylabel('mav-d4');

figure(3)
subplot(3,1,1)
plot([1:100],var_d2_f1,'b-',[1:100],var_d2_f2,'r-');
title('VAR')
legend('class 1','class 2');
ylabel('var-d2');

subplot(3,1,2)
plot([1:100],var_d3_f1,'b-',[1:100],var_d3_f2,'r-');
ylabel('var-d3');

subplot(3,1,3)
plot([1:100],var_d4_f1,'b-',[1:100],var_d4_f2,'r-');
ylabel('var-d4');

figure(4)
subplot(3,1,1)
plot([1:100],aac_d2_f1,'b-',[1:100],aac_d2_f2,'r-');
title('AAC');
legend('feature 1','feature 2');
ylabel('aac-d2');

subplot(3,1,2)
plot([1:100],aac_d3_f1,'b-',[1:100],aac_d3_f2,'r-');
ylabel('aac-d3');

subplot(3,1,3)
plot([1:100],aac_d4_f1,'b-',[1:100],aac_d4_f2,'r-');
ylabel('aac-d4');

%%
figure(2)
subplot(2,2,1)
plot(data);
ylabel('signal');

subplot(2,2,2)
plot(cd2);
ylabel('D2');

subplot(2,2,3)
plot(cd3);
ylabel('D3');

subplot(2,2,4)
plot(cd4);
ylabel('D4');

%%
plot(data);
title('sample data for feature 1');


%%
A = [1 2 3; 1 0 0; -1 0 0];
%A = [1 0 0; 1 2 3; -1 0 0];
[coeff,score,latent] = pca(A);
%latent
biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3'});
