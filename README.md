# **Price Predictor**

This repository contains Python code for predicting the future price trends of Ethereum and Bitcoin using interactive plots with animations.
A Crypto Currency price predictor using time series model
only support for Bitcoin and Ethereum
do note that the prediction may not 100% reflect the real price

# Features
Predicts future price trends of Ethereum and Bitcoin.
Generates interactive plots with animations for better visualization.
Easy-to-use Python code for data analysis and prediction.
Installation
Clone the repository:
bash
Copy code
```
git clone https://github.com/Qaisar-Mateen/Price-Predictor.git
```
Install the required dependencies:
Copy code
pip install -r requirements.txt
Usage
Navigate to the project directory:
bash
Copy code
cd Price_predictor
Run the main Python script:
Copy code
python price_predictor.py
Follow the on-screen instructions to input data and view predictions.
Example
Here's a quick example of how to use the Price Predictor:

python
Copy code
from price_predictor import PricePredictor

# Create an instance of the PricePredictor class
predictor = PricePredictor()

# Load historical data
predictor.load_data('data/ethereum_prices.csv', 'data/bitcoin_prices.csv')

# Train the model
predictor.train_model()

# Predict future price trends
predictions = predictor.predict()

# Visualize predictions
predictor.plot_predictions(predictions)
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
