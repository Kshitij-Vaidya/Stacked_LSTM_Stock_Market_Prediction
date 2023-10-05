import yfinance as yf
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

import math
from sklearn.metrics import mean_squared_error


# Here we define a class of the LSTM Model that performs all the preprocessing and modelling taks and also predicts the values as required
class LSTM_Model():
    def __init__(self, ticker, end_date):
        self.Dataframe = yf.download(ticker, end=end_date)
        self.Dataframe.reset_index(inplace=True)

        self.CloseData = self.Dataframe['Close']
        self.scaler = MinMaxScaler(feature_range=(0,1))
        self.CloseData = self.scaler.fit_transform(np.array(self.CloseData).reshape(-1,1))
        self.TrainX, self.TrainY = self.CreateDataset(self.TrainData, time_step=100)
        self.TestX, self.TestY = self.CreateDataset(self.TestData, time_step=100)

        # Stacked LSTM Model Definition
        self.model = Sequential()
        self.model.add(LSTM(50, reteun_sequences=True, input_shape=(100,1)))
        self.model.add(LSTM(50, return_sequences=True))
        self.model.add(LSTM(50))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        # Fit the model to the training data and validate it over the test data
        self.model.fit(self.TrainX, self.TrainY, validation_data=(self.TestX, self.TestY), epochs=50, batch_size=64, verbose=1)

    def TrainTestSplit(self):
        # We split the training and testing data into a 65:35 ratio
        train_size = int(len(self.CloseData)*0.65)
        self.TrainData = self.CloseData[:train_size, :]
        self.TestData = self.CloseData[train_size:len(self.CloseData), :1]

    def CreateDataset(dataset, time_step=1):
        DataX, DataY = [], []
        for i in range(len(dataset) - time_step - 1):
            batch = dataset[i:(i+time_step), 0]
            DataX.append(batch)
            DataY.append(dataset[i+time_step, 0])
        return np.array(DataX), np.array(DataY)
    
