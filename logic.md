Step 1: Installation

Make sure you have Python installed, then install the required packages:

pip install streamlit pandas openpyxl xlsxwriter
Step 2: Run the App

streamlit run fund_calculator_app.py

Your browser will automatically open to http://localhost:8501
Step 3: Upload Your Data

Prepare an Excel file with 2 columns:

    Column 1: Month (dates like 2020-01-31)

    Column 2: Gross Returns (numbers like 0.0786 or 7.86%)

Step 4: Configure Settings

Set your parameters (explained below) and click "Calculate Net Returns"
Understanding the Parameters
1. Data Type

    Gross: Your input data is gross returns (before any fees)

    Net: Your input data is already net returns

Most common: Use "Gross"
2. Management Fees
Annual Management Fee %

The yearly fee charged by the fund manager for managing your money.

Example: 1.5% means you pay 1.5% per year

Common values:

    Hedge funds: 1.5% - 2%

    Mutual funds: 0.5% - 1%

    Index funds: 0.1% - 0.5%

Management Fee Frequency

How often the fee is charged:

    Monthly: Fee deducted every month (1.5% ÷ 12 = 0.125% per month)

    Quarterly: Fee deducted 4 times per year (Mar, Jun, Sep, Dec)

    Yearly: Fee deducted once per year (December)

Most common: Monthly

How it works in the code:
Monthly: Your fund loses 0.125% every single month
Example: $100,000 loses $125 per month in management fees
3. Performance Fees
Performance Fee (Carry) %

The percentage the fund manager takes from your profits.

Example: 10% means they take 10% of any gains

Common values:

    Hedge funds: 10% - 20%

    Private equity: 20%

    Mutual funds: Usually 0%

Performance Fee Frequency

When the performance fee is calculated and charged:

    Monthly: Calculated every month

    Quarterly: Calculated 4 times per year

    Yearly: Calculated once per year (December)

Most common: Yearly (allows full year to play out before charging)

How it works in the code:
If Yearly:

    January - November: No performance fee charged

    December: Calculate total year's gain, charge 10%

If your fund went from $1.00 to $1.80 over the year:

    Gain = $0.80

    Performance fee = $0.80 × 10% = $0.08

    You keep = $1.72

4. Hurdle Rate

The minimum return the fund must achieve before charging performance fees.

Example: 8% hurdle rate means:

    If fund returns 6%: NO performance fee (didn't beat hurdle)

    If fund returns 10%: Performance fee charged on the 2% excess (10% - 8%)

Set to 0% if there's no hurdle (most common for Excel matching)
5. High Water Mark (HWM)

A protective mechanism for investors. Performance fees are only charged when the fund reaches a new all-time high.

Example Story:

Year 1: Fund grows to $1.50 → Charge 10% performance fee → New HWM = $1.50
Year 2: Fund drops to $1.20 → NO performance fee (below HWM)
Year 3: Fund grows to $1.40 → NO performance fee (still below $1.50 HWM)
Year 4: Fund grows to $1.60 → YES, charge 10% on ($1.60 - $1.50) = $0.10
New HWM = $1.60

Enable this (checked) for investor protection
Understanding the Results
Output Columns Explained

    Month: The date (2020-01-31)

    Input: Your original return data (7.86%)

    Gross: Fund value before any fees ($1.0786)

    Mgmt Fee: Management fee charged this period ($0.00125)

    Mgmt Charged?: Was fee charged this month? (True)

    After Mgmt: Value after management fee ($1.07735)

    Return %: Period return after mgmt fee (7.735%)

    Hurdle Met: Did returns beat hurdle? (True)

    Perf Paid: Performance fee paid this period ($0.00 if not Dec)

    HWM: Current high water mark ($1.00)

    Net Value: Final value after all fees ($1.07735)

Step-by-Step: How One Month Is Calculated

Let's walk through January 2020 with these settings:

    Gross return: 7.86%

    Management fee: 1.5% annual, monthly

    Performance fee: 10%, yearly (so NOT charged in Jan)

    Starting value: $1.00

Step 1: Calculate Gross Value
Gross value = $1.00 × (1 + 0.0786) = $1.0786

Step 2: Apply Management Fee
Monthly mgmt fee rate = -1.5% ÷ 12 = -0.125% = -0.00125
Value after mgmt = $1.00 × (1 + 0.0786 + (-0.00125))
= $1.00 × 1.07735
= $1.07735

Step 3: Check Performance Fee
Is it December? NO → Skip performance fee
Performance fee = $0

Step 4: Final Net Value
Net value = $1.07735 (no performance fee this month)

Step 5: Update for Next Month
Next month starts with: $1.07735
(This becomes the "current_value" for February)