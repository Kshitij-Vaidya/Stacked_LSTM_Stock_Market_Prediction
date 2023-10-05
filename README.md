# Stacked_LSTM_Stock_Market_Prediction

The first step of the project is to actually implement an LSTM(Long Short Term Memory Model). This is a kind of Recurrent Neural Network that can retain the memory of older inputs very well and is great for financial predictions. The Python Notebook added in the repository is the first implementation of the LSTM Model. This is done in an attempt to understand the working of the model, the parameters involved and its performance after trainging over a test data. I have used the stock data for APPLE to train the model. The train test split is 65:35 and the data needs to be scaled before training as a requirement of the LSTM Model.

After training and testing the model, we can start developing the application which acts as the interface between the model and the user. I have chosen Dash to make the application. Dash is very popular for dashboard and data visualisation purposes and can be used along with CSS and HTML to develop interactive and user-friendly interfaces.

Finally, we create a class of the model that will be used for the final training and prediction purposes. This part of the project is currently under progress and once finished the finally updated files will be pushed to this GitHub repository.
