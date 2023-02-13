import smtplib
import requests
import time
from email.mime.text import MIMEText

def get_price(symbol):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD"
    headers = {
        "Accepts": "application/json",
        "X-CMC_Pro_API_Key": "YOUR_API_KEY"
    }
    response = requests.get(url, headers=headers).json()
    return float(response["data"][symbol]["quote"]["USD"]["price"])

def compare_prices(symbol1, symbol2):
    price1 = get_price(symbol1)
    price2 = get_price(symbol2)
    global oldPrice
    global change_over
    newPrice =  price1 / price2
    priceChange = newPrice - oldPrice
    change = priceChange/oldPrice
    if change > 0 & change * 100 > change_over:
        print(f"change to {symbol2} up {change * 100}%")
        send_email(f"change to {symbol2} up {change * 100}%")
    elif change < 0 & change * 100 < -change_over :
        print(f"change to {symbol1} up {change * 100 * -1}%")
        send_email(f"change to {symbol1} up {change * 100 * -1}%")
    else: 
        print('no Change!')
    oldPrice = newPrice

def get_initPrice(symbol1, symbol2):
    price1 = get_price(symbol1)
    price2 = get_price(symbol2)
    return price1/price2

def send_email(body):
    subject = "AXS RON Update"
    sender = "senderemail@gmail.com"
    recipient = "recipientemail@gmail.com"
    password = "AppPasword"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipient)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipient, msg.as_string())
    smtp_server.quit()

if __name__ == "__main__":
    symbol1 = "AXS" #symbol axs/ron
    symbol2 = "RON"
    change_over = 5 #notify when change is over 5%
    oldPrice = get_initPrice(symbol1, symbol2)
    while True:
        compare_prices(symbol1, symbol2)
        time.sleep(3600) #interval in seconds

