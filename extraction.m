%% feature extraction
fs = 160;
dt = 1/fs;
StopTime = 1;
t = (0:dt:StopTime-dt);
n_var = 0.01;
a_var = 0.01;
f_var = 0.5;
a = [0.8,1,0.8; 0.5,1,0.4; 1,0.3,0.5; 0.7,0.8,0.9; 0.6,0.8,1; 1,0.7,1; 0.5,0.5,1];
f = [10,15,20; 11,13,25; 13,18,19; 8,14,21; 10,13,15; 12,22,27; 14,16,18];

features = zeros(1400,6);
mav = zeros(1,6);

for k = 1:7
    for n = 1:200
        
        data_L = sample_gen(a(k,:),a_var,f(k,:),f_var,n_var,t);
        [c,l] = wavedec(data_L,4,'db4');
        [cd2,cd3,cd4] = detcoef(c,l,[2 3 4]);
        
        mav_d2 = sum(abs(cd2))/length(cd2);
        mav_d3 = sum(abs(cd4))/length(cd3);
        mav_d4 = sum(abs(cd3))/length(cd4);
        mav(1,1:3) = [mav_d2, mav_d3, mav_d4];
        
        data_R = sample_gen(a(k,:),a_var,f(k,:),f_var,n_var,t);
        [c,l] = wavedec(data_R,4,'db4');
        [cd2,cd3,cd4] = detcoef(c,l,[2 3 4]);
        
        mav_d2 = sum(abs(cd2))/length(cd2);
        mav_d3 = sum(abs(cd4))/length(cd3);
        mav_d4 = sum(abs(cd3))/length(cd4);
        mav(1,4:6) = [mav_d2, mav_d3, mav_d4];
        
        features(200*(k-1)+n,:) = mav;
    end
end

save('features.mat','features');

%%

%test = permute(features(1,1,:),[3,2,1]);
%plot(test);
%%
target = reshape(repmat([0 1 2 3 4 5 6],1,200),1400,1);

save('target.mat','target');
