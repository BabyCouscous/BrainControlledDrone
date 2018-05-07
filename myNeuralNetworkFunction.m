function [Y,Xf,Af] = myNeuralNetworkFunction(X,~,~)
%MYNEURALNETWORKFUNCTION neural network simulation function.
%
% Generated by Neural Network Toolbox function genFunction, 24-Oct-2017 14:41:44.
%
% [Y] = myNeuralNetworkFunction(X,~,~) takes these arguments:
%
%   X = 1xTS cell, 1 inputs over TS timesteps
%   Each X{1,ts} = 3xQ matrix, input #1 at timestep ts.
%
% and returns:
%   Y = 1xTS cell of 1 outputs over TS timesteps.
%   Each Y{1,ts} = 1xQ matrix, output #1 at timestep ts.
%
% where Q is number of samples (or series) and TS is the number of timesteps.

%#ok<*RPMT0>

% ===== NEURAL NETWORK CONSTANTS =====

% Input 1
x1_step1_xoffset = [0.236741793555253;0.831642393808681;0.110499605791194];
x1_step1_gain = [1.33364038915869;0.867472056679705;0.642512500969729];
x1_step1_ymin = -1;

% Layer 1
b1 = [3.7912451765278239;-2.4680166428968286;-3.4152147533743622;-1.935177514893466;3.1997872186176175;1.2802347270403991;1.4213021959124783;-0.32710594760957734;1.0300197660608181;0.54591939925749911;-0.21176794358104339;0.3272528526067528;-1.6383308349018699;1.6186305139624697;-0.25846109511263504;-3.4945889757736515;2.2251819586844483;-2.4946011652738385;-2.9717019236205418;2.8880893358648838];
IW1_1 = [-1.7384592556581429 3.7815127677803124 -0.37753649522764088;2.0173249946089364 -1.1443816696361411 -0.95043604969029183;1.5480740579624428 -1.0512846957093454 -3.1911258700174896;0.97728792314907997 -3.2134294209919907 -2.8257603356785368;-0.82326923010324926 2.7471911703910865 -1.9936990209755909;-2.7257112625714441 1.4867092495207164 2.8315423274034761;-2.0664898111734304 -4.2426595051154194 -1.879416438053124;1.8835845654933836 1.4205721019543156 -2.8998789127475875;1.0160898240394469 0.66405138613970738 -2.7905332882237945;-3.6097295341134745 1.8712642072857815 -3.2713189628151835;6.3204415488144674 -3.2774098608705762 -1.6110765802694247;4.3827379452144477 -2.8295190287534302 1.8855692391991434;-1.9642557279620365 1.4268457063429709 1.8395729173348825;2.8524389638435781 2.4968709448883963 1.7986044110529744;0.96868830207969481 1.2457008731231944 -2.5233469893634393;-1.7321144856689337 -1.5578677010289521 -2.5967753631261967;0.99402853594087326 2.0156205273229069 -2.220227352661587;-2.6284966843883026 2.8185786055101953 0.9293771673650556;-1.9853998600828333 2.8771982942193897 -2.3442121347183473;2.2762388471785027 1.5904010455682336 -2.4495706825835479];

% Layer 2
b2 = -0.73756717015394446;
LW2_1 = [0.57257610090504485 1.6860761114374689 -1.1835637559231305 -0.032931996533012389 0.20136566170360329 0.3188387054337839 0.096132868687352102 0.22384515489802104 0.28698190033531068 0.29815414839336141 0.55771825437698141 0.76521637772233664 0.19962970396604857 -0.014239069968222939 -0.19231034209098496 0.15048543007468457 1.4520067746172531 -0.099125463694363911 0.016090034443737973 -1.353223541090335];

% Output 1
y1_step1_ymin = -1;
y1_step1_gain = 2;
y1_step1_xoffset = 0;

% ===== SIMULATION ========

% Format Input Arguments
isCellX = iscell(X);
if ~isCellX, X = {X}; end;

% Dimensions
TS = size(X,2); % timesteps
if ~isempty(X)
    Q = size(X{1},2); % samples/series
else
    Q = 0;
end

% Allocate Outputs
Y = cell(1,TS);

% Time loop
for ts=1:TS
    
    % Input 1
    Xp1 = mapminmax_apply(X{1,ts},x1_step1_gain,x1_step1_xoffset,x1_step1_ymin);
    
    % Layer 1
    a1 = tansig_apply(repmat(b1,1,Q) + IW1_1*Xp1);
    
    % Layer 2
    a2 = repmat(b2,1,Q) + LW2_1*a1;
    
    % Output 1
    Y{1,ts} = mapminmax_reverse(a2,y1_step1_gain,y1_step1_xoffset,y1_step1_ymin);
end

% Final Delay States
Xf = cell(1,0);
Af = cell(2,0);

% Format Output Arguments
if ~isCellX, Y = cell2mat(Y); end
end

% ===== MODULE FUNCTIONS ========

% Map Minimum and Maximum Input Processing Function
function y = mapminmax_apply(x,settings_gain,settings_xoffset,settings_ymin)
y = bsxfun(@minus,x,settings_xoffset);
y = bsxfun(@times,y,settings_gain);
y = bsxfun(@plus,y,settings_ymin);
end

% Sigmoid Symmetric Transfer Function
function a = tansig_apply(n)
a = 2 ./ (1 + exp(-2*n)) - 1;
end

% Map Minimum and Maximum Output Reverse-Processing Function
function x = mapminmax_reverse(y,settings_gain,settings_xoffset,settings_ymin)
x = bsxfun(@minus,y,settings_ymin);
x = bsxfun(@rdivide,x,settings_gain);
x = bsxfun(@plus,x,settings_xoffset);
end
