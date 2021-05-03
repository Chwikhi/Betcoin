# -*- coding: utf-8 -*-
"""

@author: Wadie
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data_B = pd.read_csv('BTC-USD.csv', index_col='Date', parse_dates=True)
print(data_B.head())
print(data_B.shape)
print(data_B.index)

data_B['Close'].plot(figsize=(12, 8))
data_B['2020-05':'2021-05']['Close'].plot(figsize=(12, 8))

plt.figure(figsize=(12, 8))
data_B['2019-05':'2020-05']['Close'].resample('2W').std().plot(label='std par deux semaines', lw=2, alpha=1)
data_B['2020-05':'2021-05']['Close'].resample('2W').std().plot(label='std par deux semaines', lw=2, alpha=1)
data_B['2019-05':'2020-05']['Close'].resample('2W').mean().plot(label='mean par deux semaines', lw=2,ls='--', alpha=1)
data_B['2020-05':'2021-05']['Close'].resample('2W').mean().plot(label='mean par deux semaines', lw=2,ls='--', alpha=1)
plt.legend()
plt.show()

sample = data_B['Close'].resample('2W').agg(['mean', 'std', 'min', 'max'])
plt.figure(figsize=(12, 8))
sample['mean'].plot(label='Moyenne par deux semaines', lw=1)
plt.fill_between(sample.index, sample['min'], sample['max'], alpha=0.5, label='min - max par deux semaines')
plt.legend()
plt.show()

plt.figure(figsize=(12, 8))
data_B['2020-10':'2021-05']['Close'].plot(label='Close')
data_B['2020-10':'2021-05']['Close'].rolling(window=5, center=True).mean().plot(label='moyenne centrée chaque 5 jours', ls='--')
plt.legend()
plt.show()

data_E = pd.read_csv('ETH-USD.csv', index_col='Date', parse_dates=True)
print(data_E.head())
print(data_E.shape)
print(data_E.index)

data_BE = pd.merge(data_B, data_E,on='Date', how='outer', suffixes=('-BTC', '-ETH') )
print(data_BE.head())
print(data_BE.shape)

data_BE = pd.merge(data_B, data_E,on='Date', how='inner', suffixes=('-BTC', '-ETH') )
print(data_BE.head())
print(data_BE.shape)

data_BE[['Close-BTC', 'Close-ETH']].plot(subplots=True, figsize=(15, 10))
plt.show()

corr_BTC_ETH = data_BE[['Close-BTC', 'Close-ETH']].corr()
print(corr_BTC_ETH)
sns.heatmap(corr_BTC_ETH)

def turtle_strategy(data):
    
    df = data.copy()
    df['Buy'] = np.zeros(len(df))
    df['Sell'] = np.zeros(len(df))
    df['rollingmax'] = df['Close'].shift(1).rolling(window=15).max()
    df['rollingmin'] = df['Close'].shift(1).rolling(window=15).min()
    df.loc[df['rollingmin'] > df['Close'], 'Sell'] = -1
    df.loc[df['rollingmax'] < df['Close'], 'Buy'] = 1
    
    fig, ax = plt.subplots(2, figsize=(12, 8), sharex=True, )
    ax[0].plot(df['2020-05':'2021-05']['Close'])
    ax[0].plot(df['2020-05':'2021-05']['rollingmin'])
    ax[0].plot(df['2020-05':'2021-05']['rollingmax'])
    ax[0].legend(['Close', 'Min after 15 days', 'Max after 15 days'])
    ax[1].plot(df['2020-05':'2021-05']['Buy'])
    ax[1].plot(df['2020-05':'2021-05']['Sell'])
    ax[1].legend(['Buy !!','Sell !!!'])
    plt.show()

turtle_strategy(data_B)
turtle_strategy(data_E)