#!/usr/bin/env python3
import sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
from datafeed import yahoo
days_in_a_year = 252


def random_weights(size):
    weights = np.random.random(size)
    weights /= np.sum(weights)
    return weights
    

def get_returns(stocks, start, end):
    data = yahoo.get_close(stocks, start, end)
    returns = np.log(data / data.shift(1))
    return returns


def portfolio_return(returns, weights):
    return np.sum(returns.mean() * weights) * days_in_a_year


def portfolio_variance(returns, weights):
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * days_in_a_year, weights)))


def monte_carlo_sim(stocks, start, end):
    returns = get_returns(stocks, start, end)
    
    n = 10000
    erets = []
    evars = []

    for i in range(n):
        weights = random_weights(len(stocks))
        erets.append(portfolio_return(returns, weights))
        evars.append(portfolio_variance(returns, weights))

    return erets, evars


def optimizing_criterion(weights, returns):
    return -portfolio_return(returns, weights) / portfolio_variance(returns, weights)


def optimize_sharpe_ratio(stocks, returns, weights):
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
    bounds = tuple((0, 1) for x in range(len(stocks)))
    return optimize.minimize(fun=optimizing_criterion, x0=weights, args=returns,
                            method='SLSQP', bounds=bounds, constraints=constraints)


def plot_frontier(returns, variances):
    returns = np.array(returns)
    variances = np.array(variances)
    plt.figure(figsize=(12, 8))
    plt.scatter(variances, returns, c=returns/variances, marker='.')
    plt.xlabel('Variance')
    plt.ylabel('Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()


if __name__ == '__main__':

    stocks = [ 'WMT', 'TSLA', 'GE', 'AMZN', 'DB', 'AAPL' ]
    start = '01/01/2010'
    end = '01/01/2017'

    #erets, evars = monte_carlo_sim(stocks, start, end)
    #plot_frontier(erets, evars)

    erets = get_returns(stocks, start, end)
    weights = random_weights(len(stocks))
    ret = optimize_sharpe_ratio(stocks, erets, weights)
    
    print(ret['x'].round(3))
