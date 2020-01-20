# trading-app
***My idea behind the trading app***
   - Saving money by investing instead of sitting in a bank
   - Having your saved money gain income from dividends
   - Saving automatically once per week
   - Amount to save is (monthly income - expenses) / 4

## How to Install:
**Clone the repository into your desired directory using:**
`git clone https://github.com/afatt/trading-app.git`

## Run the app:
1. Start the script: `python3 info_prompt.py`

# After running the app
1. Prompt the user for a robinhood username and password
   - Save the username and password to environment variables
2. Prompt the user for how much money they would like to invest/save
   each week
   - Check their robinhood buying_power to make sure they have enough
     in their account to invest and suggest adding more if they do not
3. Ask the user what day of the week they would like to invest and what
   frequency once per month, once per week?

## Useful links and References
robin_stocks functions:
http://www.robin-stocks.com/en/latest/functions.html

yfinance github:
https://github.com/ranaroussi/yfinance
