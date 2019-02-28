% https://s3.amazonaws.com/quandl-production-static/BSE+Descriptions/stocks.txt

clear;
format bank;
apikey = '';
c = quandl(apikey);

stocks = [ ...
    "BSE/BOM532174" % ICICI
    "BSE/BOM500325" % Reliance 
    "BSE/BOM513010" % Tata Steel
    "BSE/BOM500312" % Oil and Natural Gas
    "BSE/BOM532454" % Airtel
]';

startdate = datetime('2018-12-01','InputFormat','yyyy-MM-dd');
enddate = datetime('2018-12-31','InputFormat','yyyy-MM-dd');
periodicity = 'daily';

d = arrayfun(@(s) history(c,s,startdate,enddate,periodicity), stocks, ...
    'UniformOutput', false);
d = cellfun(@(v) v.Close, d, 'UniformOutput', false);
d = cell2mat(d);

returns = diff(d);
mean = mean(returns);
covar = cov(returns);

weights = rand(size(stocks, 2), 1);
weights = weights / sum(weights);
disp(sum(weights));


n = 1000000;
erets = zeros(1, n);
evars = zeros(1, n);
for c = 1:n
    weights = rand(size(stocks, 2), 1);
    weights = weights / sum(weights);
    erets(c) = sum((mean .* weights') * 252);
    evars(c) = sum(sum((weights * weights') .* (covar * 252)));

end


