# -*- coding: utf-8 -*-
"""week_4&5_q3_LSTM and RNN(jafar_aghajani).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/128S7A6jHzkqV-fHBI_KP0DCF70kD7HME
"""

# week 4&5 / Q3 / combine LSTM and RNN / Airline passenger
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, LSTM, Dense

url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv'
df = pd.read_csv(url, usecols=[1], engine='python')

data = df.values.astype('float32')

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

train_size = int(len(scaled_data) * 0.67)
test_size = len(scaled_data) - train_size
train_data, test_data = scaled_data[0:train_size], scaled_data[train_size:]

def create_dataset(data, look_back=1):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        y.append(data[i + look_back, 0])
    return np.array(X), np.array(y)

look_back = 3
X_train, y_train = create_dataset(train_data, look_back)
X_test, y_test = create_dataset(test_data, look_back)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

model = Sequential()
model.add(SimpleRNN(50, return_sequences=True, input_shape=(look_back, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

history = model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=2, validation_data=(X_test, y_test))

train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

train_predict = scaler.inverse_transform(train_predict)
y_train = scaler.inverse_transform(y_train.reshape(-1, 1))
test_predict = scaler.inverse_transform(test_predict)
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

train_score = np.sqrt(np.mean((train_predict[:, 0] - y_train[:, 0]) ** 2))
print(f'Train Score: {train_score:.2f} RMSE')
test_score = np.sqrt(np.mean((test_predict[:, 0] - y_test[:, 0]) ** 2))
print(f'Test Score: {test_score:.2f} RMSE')

train_predict_plot = np.empty_like(scaled_data)
train_predict_plot[:, :] = np.nan
train_predict_plot[look_back:len(train_predict) + look_back, :] = train_predict

test_predict_plot = np.empty_like(scaled_data)
test_predict_plot[:, :] = np.nan
test_predict_plot[len(train_predict) + (look_back * 2):len(scaled_data), :] = test_predict

plt.figure(figsize=(12, 6))
plt.plot(scaler.inverse_transform(scaled_data), label='Original Data')
plt.plot(train_predict_plot, label='Train Prediction')
plt.plot(test_predict_plot, label='Test Prediction')
plt.xlabel('Time')
plt.ylabel('Passengers')
plt.title('Airline Passenger Prediction with Combined RNN and LSTM')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Model Loss During Training')
plt.legend()
plt.show()

# week 4&5 / Q3 / combine LSTM and RNN / Apple stock price
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, SimpleRNN, LSTM, Dense, concatenate
from tensorflow.keras.utils import plot_model

url = 'https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1488326400&period2=1609459200&interval=1d&events=history'
df = pd.read_csv(url, usecols=['Date', 'Close'], parse_dates=['Date'], index_col='Date')

data = df['Close'].values.astype('float32')

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data.reshape(-1, 1))

train_size = int(len(scaled_data) * 0.67)
test_size = len(scaled_data) - train_size
train_data, test_data = scaled_data[0:train_size], scaled_data[train_size:]

def create_dataset(data, look_back=1):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        y.append(data[i + look_back, 0])
    return np.array(X), np.array(y)

look_back = 10
X_train, y_train = create_dataset(train_data, look_back)
X_test, y_test = create_dataset(test_data, look_back)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

inputs = Input(shape=(look_back, 1))

rnn_out = SimpleRNN(units=50, return_sequences=True)(inputs)
lstm_out = LSTM(units=50, return_sequences=True)(inputs)

merged = concatenate([rnn_out, lstm_out], axis=-1)

merged_out = LSTM(units=50)(merged)
output = Dense(1)(merged_out)

model_combined = Model(inputs=inputs, outputs=output)
model_combined.compile(loss='mean_squared_error', optimizer='adam')

history_combined = model_combined.fit(X_train, y_train, epochs=100, batch_size=1, verbose=2, validation_data=(X_test, y_test))

train_predict = model_combined.predict(X_train)
test_predict = model_combined.predict(X_test)

train_predict = scaler.inverse_transform(train_predict)
y_train = scaler.inverse_transform(y_train.reshape(-1, 1))
test_predict = scaler.inverse_transform(test_predict)
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

train_score_combined = np.sqrt(np.mean((train_predict[:, 0] - y_train[:, 0]) ** 2))
print(f'Train Score: {train_score_combined:.2f} RMSE')
test_score_combined = np.sqrt(np.mean((test_predict[:, 0] - y_test[:, 0]) ** 2))
print(f'Test Score: {test_score_combined:.2f} RMSE')

train_predict_plot_combined = np.empty_like(scaled_data)
train_predict_plot_combined[:, :] = np.nan
train_predict_plot_combined[look_back:len(train_predict) + look_back, :] = train_predict

test_predict_plot_combined = np.empty_like(scaled_data)
test_predict_plot_combined[:, :] = np.nan
test_predict_plot_combined[len(train_predict) + (look_back * 2):len(scaled_data), :] = test_predict

plt.figure(figsize=(12, 6))
plt.plot(scaler.inverse_transform(scaled_data), label='Original Data')
plt.plot(train_predict_plot_combined, label='Train Prediction')
plt.plot(test_predict_plot_combined, label='Test Prediction')
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Apple Stock Price Prediction with RNN and LSTM')
plt.legend()
plt.show()

plot_model(model_combined, to_file='model_combined_architecture.png', show_shapes=True, show_layer_names=True)

from PIL import Image
img = Image.open('model_combined_architecture.png')
img.show()

plt.figure(figsize=(12, 6))
plt.plot(history_combined.history['loss'], label='Train Loss')
plt.plot(history_combined.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Model Loss During Training')
plt.legend()
plt.show()