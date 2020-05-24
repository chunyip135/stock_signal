#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 23:00:27 2020

@author: samuelwong
"""


import pandas as pd
import numpy as np
import plotnine as p9
import matplotlib.pyplot as plt
import seaborn as sns

def stock_signal(stock_name = None, data = None,date = None, SMA = False, period = None, window = None,startend = False, start = '', end = '', Close = 'Close'):
    ''' Plot the stock data with signal based on price and SMA strategy'''
    
    # import data
    df = pd.read_csv(data, parse_dates = [date], index_col = date)
    df = df[[Close]]
    
    # resample data
    df = df.resample(period).ffill()

    # manipulate data period
    if startend == True:
        start = start
        end = end
        df = df.loc[start:end,:]
        
    # plot SMA
    if SMA == True:
        sma_name = 'SMA ' + str(window)
        df[sma_name] = df[Close].rolling(window = window).mean()
        

    def buy_sell(data, Close = '', SMA = ''):
        ''' signal buy or sell.'''
        # empty list
        signalbuy = []
        signalsell = []
        # initial movement of the price ( 1 is price rising while -1 is price dropping)
        flag = -1
        
        for i in range(len(data)):
            # if Closing is above SMA50 : buy
            if data[Close][i] > data[SMA][i]:
                if flag == 1:
                    signalbuy.append(np.nan)
                    signalsell.append(np.nan)
                elif flag == -1:
                    signalbuy.append(data.Close[i])
                    signalsell.append(np.nan)
                    flag = 1
            # if Closing is below SMA50 : sell
            elif data[Close][i] < data[SMA][i]:
                if flag == -1:
                    signalbuy.append(np.nan)
                    signalsell.append(np.nan)
                elif flag == 1:
                    signalbuy.append(np.nan)
                    signalsell.append(data.Close[i])
                    flag = -1
            else:
                signalbuy.append(np.nan)
                signalsell.append(np.nan)
        return signalbuy, signalsell
    
    df['buy'], df['sell'] = buy_sell(df, Close = 'Close', SMA = sma_name)
    
    xlabel_name = 'Date (' + start + ' - ' + end + ')'
    title =  stock_name + '\'s stock price'
    
    # plot the graph
    plt.style.use('seaborn-notebook')      
    plt.plot(df.index, df[Close], label = 'Close', alpha = 0.35)
    plt.plot(df.index, df[sma_name], label = sma_name, alpha = 0.35)
    plt.plot(df.index, df.buy, label = 'Buy', marker = '^', color = 'g', linestyle = 'none')
    plt.plot(df.index, df.sell, label = 'Sell', marker = 'v', color = 'r', linestyle = 'none')
    plt.xlabel(xlabel_name)
    plt.ylabel('Price')
    plt.title(title)
    plt.tight_layout()
    plt.legend()
    plt.show()

    
    return df


def stock_signal_ma_crossover(stock_name = None, data = None,date = None, SMA = False, period = None, window1 = None, window2 = None,startend = False, start = '', end = '', Close = 'Close'):
    ''' Plot the stock data with signal based on SMA crossover strategy'''
    
    # import data
    df = pd.read_csv(data, parse_dates = [date], index_col = date)
    df = df[[Close]]
    
    # resample data
    df = df.resample(period).ffill()

    # manipulate data period
    if startend == True:
        start = start
        end = end
        df = df.loc[start:end,:]
        
    # plot SMA
    if SMA == True:
        sma_name1 = 'SMA ' + str(window1)
        sma_name2 = 'SMA ' + str(window2)
        df[sma_name1] = df[Close].rolling(window = window1).mean()
        df[sma_name2] = df[Close].rolling(window = window2).mean()
        

    def buy_sell_improvised(data, Close = '',SMA1 = '', SMA2 = ''):
        ''' signal buy or sell.'''
        # empty list
        signalbuy = []
        signalsell = []
        # initial movement of the price ( 1 is price rising while -1 is price dropping)
        flag = -1
        
        for i in range(len(data)):
            # if Closing is above SMA50 : buy
            if data[sma_name1][i] > data[sma_name2][i]:
                if flag == 1:
                    signalbuy.append(np.nan)
                    signalsell.append(np.nan)
                elif flag == -1:
                    signalbuy.append(data.Close[i])
                    signalsell.append(np.nan)
                    flag = 1
            # if Closing is below SMA50 : sell
            elif data[sma_name1][i] < data[sma_name2][i]:
                if flag == -1:
                    signalbuy.append(np.nan)
                    signalsell.append(np.nan)
                elif flag == 1:
                    signalbuy.append(np.nan)
                    signalsell.append(data.Close[i])
                    flag = -1
            else:
                signalbuy.append(np.nan)
                signalsell.append(np.nan)
        return signalbuy, signalsell
    
    df['buy'], df['sell'] = buy_sell_improvised(df, Close = 'Close', SMA1 = sma_name1, SMA2 = sma_name2)
    
    xlabel_name = 'Date (' + start + ' - ' + end + ')'
    title =  stock_name + '\'s stock price'
    
    # plot the graph
    plt.style.use('seaborn-notebook')      
    plt.plot(df.index, df[Close], label = 'Close', alpha = 0.35)
    plt.plot(df.index, df[sma_name1], label = sma_name1, alpha = 0.35)
    plt.plot(df.index, df[sma_name2], label = sma_name2, alpha = 0.35)
    plt.plot(df.index, df.buy, label = 'Buy', marker = '^', color = 'g', linestyle = 'none')
    plt.plot(df.index, df.sell, label = 'Sell', marker = 'v', color = 'r', linestyle = 'none')
    plt.xlabel(xlabel_name)
    plt.ylabel('Price')
    plt.title(title)
    plt.tight_layout()
    plt.legend()
    plt.show()

    
    return df

