function data = sample_gen(a,a_var,f,f_var,v,t)
    L = length(t);
    data = zeros(1,L);
    for i = 1:length(a)
        data = data + (a(i) + sqrt(a_var)*randn(1))*sin(2*pi*(f(i) + sqrt(f_var)*randn(1))*t + ...
            2*pi*rand(1));       
    end
    data = data + sqrt(v)*randn(1,L);
end
