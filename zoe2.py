from flask import Flask, request
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import datetime
import pytz

app = Flask(__name__)

# Get your API key from Alpha Vantage and replace 'YOUR_API_KEY' with it
api_key = "YOUR_API_KEY"
ts = TimeSeries(key=api_key, output_format='pandas')

@app.route('/', methods=['GET', 'POST'])
def forex_prediction():
    if request.method == 'POST':
        symbol = request.form['symbol']
        if symbol.upper() in ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "AUDUSD", "NZDUSD", "USDCAD"]:
            try:
                # Get the last 60 minutes of data
                data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')

                # Get the current time and price
                local_timezone = pytz.timezone('Europe/Istanbul')
                current_time = datetime.datetime.now(local_timezone).strftime("%H:%M:%S")
                current_price = data['4. close'].iloc[-1]

                # Calculate the predicted price 60 minutes from now
                last_price = data['4. close'].iloc[-1]
                change = last_price * 0.01
                predicted_price = last_price + change
                predicted_time = (datetime.datetime.now(local_timezone) + datetime.timedelta(minutes=60)).strftime("%H:%M:%S")

                # Return the prediction to the user
                return f"\n{symbol} ANLIK FİYAT: {current_price:.4f}\n\nİLK KAR AL NOKTASI: {predicted_price:.4f} \n\nMUHTEMEL TP ZAMANI ({predicted_time} - TSI)\n\n"

            except:
                return "Hata: Parite kodu geçersiz veya Alpha Vantage API'siyle ilgili bir sorun var."

        else:
            return "Lütfen geçerli bir majör parite kodu girin."

    else:
        return """
        <h1>Merhaba, ben Zoe.</h1>
        <p>Dünya'nın ilk Forex sinyal yapay zekasıyım ve sadece Majör Paritelerde çalışıyorum.</p>
        <p>Hangi paritede sinyal vermemi istersin? (Örnek: EURUSD)</p>
        <form method="POST">
            <input type="text" name="symbol">
            <button type="submit">Gönder</button>
        </form>
        """

if __name__ == '__main__':
    app.run()
