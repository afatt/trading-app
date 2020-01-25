# trading-app
## My idea behind the trading app:
   - Saving money by investing instead of sitting in a bank
   - Having your saved money gain income from dividends
   - Saving automatically once per week
   - Amount to save is (monthly income - expenses) / 4

### How to Install:
Clone the repository into your desired directory using:

    git clone https://github.com/afatt/trading-app.git

Next:

    pip install .

### Run the app:
Start the script:

    python3 info_prompt.py

You fill out the following prompts as they appear:

    Enter your Robinhood username/email:
    Enter your Robinhood password:
                          Options
    --------------------------------------------
    Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
    Enter the day or days of the week you would like to invest:
    Enter the amount you would like to invest:
    Enter the time of day to run (Ex. 15:30):

The info_prompt.py script will start the trader and run each day
selected in step 4 and at the time selected in step 6

If for any reason the script stops running rerun the `info_prompt.py`
script and you wil see the following prompt:

    Would you like to change any settings? (y/n):

## Useful links and References
robin_stocks functions:
http://www.robin-stocks.com/en/latest/functions.html

yfinance github:
https://github.com/ranaroussi/yfinance
