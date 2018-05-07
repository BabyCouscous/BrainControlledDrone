f1 = 50;
%f2 = 25;
f2 = 0;
f3 = 0;
%f3 = 10;
f4 = 2;
a1 = 1.1;
a2 = 0.8;
a3 = 0.6;
a4 = 0.4;
fs = 256;
dt = 1/fs;
StopTime = 8;
t = (0:dt:StopTime-dt);
n_var = 0.01;

data = a1*sin(2*pi*f1*t) + a2*sin(2*pi*f2*t) + ...
a3*sin(2*pi*f3*t) + a4*sin(2*pi*f4*t);% + sqrt(n_var)*randn(1,1000);

dwtmode('per');
[c,l] = wavedec(data,5,'db4');

[cd1,cd2,cd3,cd4,cd5] = detcoef(c,l,[1 2 3 4 5]);
cp1 = appcoef(c,l,'db4',1);
cp2 = appcoef(c,l,'db4',2);
cp3 = appcoef(c,l,'db4',3);
cp4 = appcoef(c,l,'db4',4);
cp5 = appcoef(c,l,'db4',5);
%[cp1,cp2,cp3] = appcoef(c,l,[1 2 3]);
%cp4 = appcoef(c,l,'db4',4);

%filtered_data = filter(LPF,data);

%{
figure(1)
plot(data);
figure(2)
plot(cp4);
figure(3)
plot(filtered_data);
%}



figure

subplot(3,2,1)
plot(data);
ylabel('signal');


subplot(3,2,2)
plot(cd1);
ylabel('D1');

subplot(3,2,3)
plot(cd2);
ylabel('D2');

subplot(3,2,4)
plot(cd3);
ylabel('D3');

subplot(3,2,5)
plot(cd4);
ylabel('D4');

subplot(3,2,6)
plot(cp5);
ylabel('A5');

%{
%%

L1 = length(data);
Y1 = abs(fft(data));
Y1 = Y1(1:L1/2)/L1;
df1 = fs/L1;
f1 = 0:df1:fs/2-df1;
figure
plot(f1,Y1);
%%
% 32-64Hz
L2 = length(cd2);
Y2 = abs(fft(cd2));
Y2 = Y2(1:L2/2)/L2;
%df2 = fs/(2*L2);
%f2 = 0:df2:fs/4-df2;
figure
plot(Y2);
%%
% 16-32 Hz
L3 = length(cd3);
Y3 = abs(fft(cd3));
Y3 = Y3(1:L3/2)/L3;
%df3 = fs/(4*L3);
%f3 = 0:df3:fs/8-df3;
figure
plot(Y3);
%%
% 8-16 Hz
L4 = length(cd4);
Y4 = abs(fft(cd4));
Y4 = Y4(1:L4/2)/L4;
%df4 = fs/(8*L4);
%f4 = 0:df4:fs/16-df4;
figure
plot(Y4);
%}


%%
A = [1 2 3; 1 0 0; -1 0 0];
%A = [1 0 0; 1 2 3; -1 0 0];
[coeff,score,latent] = pca(A);
%latent
biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',{'v_1','v_2','v_3'});
