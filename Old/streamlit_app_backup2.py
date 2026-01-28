import streamlit as st
import pandas as pd
import io
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="FoF Calculator", layout="wide")

st.title("Investment Fund Fee Calculator")

# Parameters always visible
st.subheader("💰 Fund Fee Mechanism")

# STATIC DIAGRAM
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; }
        
        body { 
            margin: 0; 
            padding: 10px; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: transparent;
        }

        .container { 
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
            padding: 20px; 
            border-radius: 20px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
        }

        .flowchart { 
            display: flex; 
            flex-direction: row; 
            align-items: center; 
            justify-content: space-between; 
            gap: 10px; 
            padding: 20px 0;
            width: 100%;
        }

        .box { 
            border: 4px solid; 
            padding: 20px 15px; 
            border-radius: 15px; 
            text-align: center; 
            font-weight: bold; 
            box-shadow: 0 8px 20px rgba(0,0,0,0.1); 
            flex: 1 1 0px;
            min-width: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 140px;
        }

        .master { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-color: #4CAF50; }
        .axsa { background: linear-gradient(135deg, #2196F3, #1976D2); color: white; border-color: #2196F3; }
        .actual { background: linear-gradient(135deg, #FF9800, #F57C00); color: white; border-color: #FF9800; }

        .arrow { 
            font-size: 28px; 
            color: #475569; 
            font-weight: bold; 
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 40px;
            animation: pulse 2s infinite;
        }

        .arrow::before { content: "➜"; }

        @keyframes pulse { 
            0%, 100% { opacity: 1; transform: scale(1); } 
            50% { opacity: 0.6; transform: scale(1.1); } 
        }

        .title { font-size: 16px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
        .big-text { font-size: 28px; font-weight: 900; line-height: 1; margin: 5px 0; }
        .label { font-size: 13px; opacity: 0.9; font-weight: 500; }

        .mechanism { 
            margin-top: 20px; 
            padding: 20px; 
            background: rgba(255,255,255,0.7); 
            border-radius: 15px; 
            border: 1px solid rgba(0,0,0,0.05);
        }

        .mechanism h3 { 
            text-align: center; 
            margin-top: 0; 
            margin-bottom: 15px; 
            color: #1e293b;
            font-size: 18px;
        }
        .mechanism h5 {
            text-align: center; 
            color: #64748b;
            font-weight: 500;
            font-size: 14px;
            margin-bottom: 20px;
            line-height: 1.4;
        }

        .grid-list {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .grid-list li {
            background: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 14px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        }

        .grid-list li::before {
            content: "✓";
            color: #10b981;
            font-weight: bold;
            margin-right: 10px;
        }

        @media (max-width: 800px) {
            .flowchart { 
                flex-direction: column; 
                gap: 5px; 
            }
            .box {
                width: 100%;
                max-width: 400px;
                min-height: 120px;
            }
            .arrow::before { content: "⬇"; }
            .arrow { height: 40px; width: 100%; }
            
            .grid-list {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="flowchart">
            <div class="box master">
                <div class="title">📈 Master Fund</div>
                <div class="big-text">GROSS</div>
                <div class="label">Before fees are applied</div>
            </div>
            
            <div class="arrow"></div>
            
            <div class="box axsa">
                <div class="title">🏦 AXSA Fund</div>
                <div class="big-text">NET</div>
                <div class="label">After Management Fees</div>
            </div>
            
            <div class="arrow"></div>
            
            <div class="box actual">
                <div class="title">💰 Actual Net</div>
                <div class="big-text">FINAL</div>
                <div class="label">After Carry + Hurdle</div>
            </div>
        </div>
        
        <div class="mechanism">
            <h3>🔄 Fee Flow Mechanism</h3>
            <h5>Calculator processes Gross or Net data to generate final net values with fee breakdowns</h5>
            <ul class="grid-list">
                <li><b>Master Fund Gross</b>: Raw performance</li>
                <li><b>Subtract Mgmt Fee</b>: AXSA Net result</li>
                <li><b>Hurdle Check</b>: Must exceed benchmark</li>
                <li><b>Carry Applied</b>: Fee on excess return</li>
                <li style="grid-column: span 1;"><b>Actual Net</b>: Final distribution</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

components.html(html_code, height=650, scrolling=True)

# Parameters - REORGANIZED WITH MANAGEMENT FEE FREQUENCY
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Basic Settings")
    data_type = st.radio("Data Type", ["Gross", "Net"], help="Select whether input data is Gross or Net")
    
    st.markdown("### 💼 Management Fees")
    mgmt_fee_annual = st.number_input("Annual Management Fee %", 0.0, 10.0, 1.5, 0.1, 
                                      help="Annual management fee percentage")
    mgmt_freq = st.selectbox("Management Fee Frequency", 
                            ["Monthly", "Quarterly", "Yearly"],
                            help="How often management fees are charged",
                            index=0)  # Default to Monthly
    
with col2:
    st.markdown("### 🎯 Performance Fees")
    carry_pct = st.number_input("Performance Fee (Carry) %", 0.0, 50.0, 10.0, 0.5,
                                help="Performance fee percentage on gains above hurdle")
    perf_freq = st.selectbox("Performance Fee Frequency", 
                            ["Monthly", "Quarterly", "Yearly"],
                            help="How often performance fees are calculated",
                            index=2)  # Default to Yearly
    
    st.markdown("### 🚀 Advanced Settings")
    hurdle_rate = st.number_input("Hurdle Rate % (Annual)", 0.0, 20.0, 0.0, 0.1,
                                  help="Minimum return required before charging performance fees")
    use_hwm = st.checkbox("Use High Water Mark (HWM)", value=True,
                         help="Only charge performance fees when value exceeds previous high")

# Helper function to convert datetime columns to strings for safe display
def prepare_for_display(df):
    """Convert datetime columns to strings to avoid PyArrow errors"""
    df_display = df.copy()
    for col in df_display.columns:
        if df_display[col].dtype == 'object':
            # Check if column contains datetime objects
            if df_display[col].apply(lambda x: isinstance(x, (pd.Timestamp, datetime))).any():
                df_display[col] = df_display[col].apply(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, (pd.Timestamp, datetime)) else x)
    return df_display

# Helper function to parse returns
def parse_returns(series):
    """Parse returns that may be in % format or decimal - returns pandas Series"""
    cleaned = series.astype(str).str.rstrip('%').str.strip()
    numeric = pd.to_numeric(cleaned, errors='coerce')
    # If values are > 1, assume they're percentages and divide by 100
    result = numeric.apply(lambda x: x / 100 if pd.notna(x) and abs(x) > 1 else x)
    return result

# File upload
uploaded_file = st.file_uploader("Upload Excel (2 cols: Month, Gross/Net %)", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Try to read the file - check for multiple sheets
        xl_file = pd.ExcelFile(uploaded_file, engine='openpyxl')
        
        # If multiple sheets, try to find the data sheet
        if len(xl_file.sheet_names) > 1:
            st.info(f"📋 Found {len(xl_file.sheet_names)} sheets: {', '.join(xl_file.sheet_names)}")
            
            # Try to find Sheet1 or a sheet with data
            if 'Sheet1' in xl_file.sheet_names:
                df = pd.read_excel(uploaded_file, sheet_name='Sheet1', engine='openpyxl')
                st.success("✅ Using 'Sheet1' for calculations")
            else:
                df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
                st.info(f"ℹ️ Using first sheet: '{xl_file.sheet_names[0]}'")
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        st.subheader("✅ Original Data")
        
        # Prepare for safe display
        df_display = prepare_for_display(df.head(20))
        st.dataframe(df_display, use_container_width=True)
        
        if len(df.columns) < 2:
            st.error(f"❌ Expected at least 2 columns, but got {len(df.columns)}. Please upload a file with Month and Gross/Net columns.")
        else:
            # Take first 2 columns only
            df = df.iloc[:, :2].copy()
            period_col, returns_col = df.columns
            
            # Parse returns
            returns_decimal = parse_returns(df[returns_col])
            
            if returns_decimal.isna().all():
                st.error("❌ Cannot parse returns column. Expected numbers or % (e.g., 7.89 or 7.89%)")
            else:
                if st.button("🚀 Calculate Net Returns", type="primary"):
                    # Step 1: Check if Gross or Net
                    if data_type == "Gross":
                        st.info("ℹ️ Gross selected - Proceeding with net calculations from gross values")
                    
                    # Prepare DataFrame
                    result_df = df[[period_col, returns_col]].copy()
                    result_df.columns = ['Month', 'Input_Return']
                    
                    # Parse dates
                    result_df['Month_dt'] = pd.to_datetime(result_df['Month'], dayfirst=True, errors='coerce')
                    result_df['Gross_Return'] = returns_decimal.values
                    
                    # Drop invalid rows
                    result_df = result_df.dropna(subset=['Month_dt', 'Gross_Return'])
                    result_df = result_df.sort_values('Month_dt').reset_index(drop=True)
                    
                    if result_df.empty:
                        st.error("❌ No valid data after parsing dates and returns")
                    else:
                        # ✅ FIX 1: Management fee as RATE (additive to return), not percentage of value
                        if mgmt_freq == "Monthly":
                            mgmt_fee_rate = -(mgmt_fee_annual / 100 / 12)
                            mgmt_periods_per_year = 12
                        elif mgmt_freq == "Quarterly":
                            mgmt_fee_rate = -(mgmt_fee_annual / 100 / 4)
                            mgmt_periods_per_year = 4
                        else:  # Yearly
                            mgmt_fee_rate = -(mgmt_fee_annual / 100)
                            mgmt_periods_per_year = 1
                        
                        # Hurdle and performance fee setup
                        if perf_freq == "Monthly":
                            hurdle_period = hurdle_rate / 100 / 12
                            perf_periods_per_year = 12
                        elif perf_freq == "Quarterly":
                            hurdle_period = hurdle_rate / 100 / 4
                            perf_periods_per_year = 4
                        else:  # Yearly
                            hurdle_period = hurdle_rate / 100
                            perf_periods_per_year = 1
                        
                        carry_decimal = carry_pct / 100
                        
                        # Initialize tracking variables
                        starting_value = 1.0
                        current_value = starting_value
                        hwm = starting_value
                        prev_year = None
                        
                        # Results lists
                        gross_values = []
                        mgmt_fees = []
                        after_mgmt_values = []
                        returns_list = []
                        hurdle_met_list = []
                        hwm_list = []
                        perf_fees_paid = []
                        net_values = []
                        mgmt_charged_list = []
                        
                        # Process each period
                        for idx, row in result_df.iterrows():
                            gross_return = row['Gross_Return']
                            month_dt = row['Month_dt']
                            current_year = month_dt.year
                            current_month = month_dt.month
                            is_year_end = current_month == 12
                            
                            # Calculate gross value
                            gross_value = current_value * (1 + gross_return)
                            
                            # ✅ FIX 2: Apply management fee as ADDITIVE RATE to returns
                            mgmt_fee_applied = 0.0
                            mgmt_charged = False
                            
                            if mgmt_freq == "Monthly":
                                mgmt_charged = True
                                mgmt_fee_applied = mgmt_fee_rate
                            elif mgmt_freq == "Quarterly":
                                if current_month in [3, 6, 9, 12]:
                                    mgmt_charged = True
                                    mgmt_fee_applied = mgmt_fee_rate
                            elif mgmt_freq == "Yearly":
                                if is_year_end:
                                    mgmt_charged = True
                                    mgmt_fee_applied = mgmt_fee_rate
                            
                            # Apply: current_value * (1 + gross_return + mgmt_fee_rate)
                            value_after_mgmt = current_value * (1 + gross_return + mgmt_fee_applied)
                            
                            # Calculate actual fee dollar amount for display
                            mgmt_fee_display = abs(mgmt_fee_applied * current_value) if mgmt_charged else 0.0
                            
                            # Calculate period return after mgmt fee
                            period_return = (value_after_mgmt - current_value) / current_value if current_value > 0 else 0
                            
                            # Check hurdle rate
                            hurdle_met = False
                            if hurdle_rate == 0:
                                hurdle_met = True
                            elif period_return > hurdle_period:
                                hurdle_met = True
                            
                            # ✅ FIX 3: Performance fee - ONLY CALCULATE IN PERFORMANCE PERIOD (not monthly accrual)
                            perf_fee_paid = 0.0
                            
                            # Determine if this is a performance fee period
                            should_calc_perf = False
                            if perf_freq == "Yearly":
                                should_calc_perf = is_year_end
                            elif perf_freq == "Quarterly":
                                should_calc_perf = current_month in [3, 6, 9, 12]
                            elif perf_freq == "Monthly":
                                should_calc_perf = True
                            
                            if should_calc_perf:
                                if use_hwm:
                                    # Only charge if value > HWM
                                    if value_after_mgmt > hwm:
                                        gain_above_hwm = value_after_mgmt - hwm
                                        perf_fee_paid = gain_above_hwm * carry_decimal
                                        value_after_mgmt -= perf_fee_paid
                                        hwm = value_after_mgmt  # ✅ FIX 4: Update HWM only in perf period
                                else:
                                    # No HWM - charge on any gain above hurdle
                                    if hurdle_met and period_return > hurdle_period:
                                        excess_return = period_return - hurdle_period
                                        perf_fee_paid = current_value * excess_return * carry_decimal
                                        value_after_mgmt -= perf_fee_paid
                            
                            # Net value
                            net_value = value_after_mgmt
                            
                            # Store results
                            gross_values.append(gross_value)
                            mgmt_fees.append(mgmt_fee_display)
                            mgmt_charged_list.append(mgmt_charged)
                            after_mgmt_values.append(value_after_mgmt + perf_fee_paid)  # Before perf fee deduction
                            returns_list.append(period_return * 100)
                            hurdle_met_list.append(hurdle_met)
                            hwm_list.append(hwm)
                            perf_fees_paid.append(perf_fee_paid)
                            net_values.append(net_value)
                            
                            # Update for next iteration
                            current_value = net_value
                            prev_year = current_year
                        
                        # Assemble results
                        result_df['Month_Display'] = result_df['Month_dt'].dt.strftime('%Y-%m-%d')
                        result_df['Gross_Value'] = gross_values
                        result_df['Mgmt_Fee'] = mgmt_fees
                        result_df['Mgmt_Charged'] = mgmt_charged_list
                        result_df['After_Mgmt'] = after_mgmt_values
                        result_df['Period_Return_%'] = returns_list
                        result_df['Hurdle_Met'] = hurdle_met_list
                        result_df['HWM'] = hwm_list
                        result_df['Perf_Fee_Paid'] = perf_fees_paid
                        result_df['Net_Value'] = net_values
                        
                        # Display results
                        st.subheader("📈 Detailed Calculation Results")
                        
                        display_cols = [
                            'Month_Display', 'Input_Return', 'Gross_Value', 
                            'Mgmt_Fee', 'Mgmt_Charged', 'After_Mgmt', 'Period_Return_%', 'Hurdle_Met',
                            'Perf_Fee_Paid', 'HWM', 'Net_Value'
                        ]
                        
                        display_df = result_df[display_cols].round(10)
                        display_df.columns = ['Month', 'Input', 'Gross', 
                                            'Mgmt Fee', 'Mgmt Charged?', 'After Mgmt', 'Return %', 'Hurdle Met',
                                            'Perf Paid', 'HWM', 'Net Value']
                        
                        st.dataframe(display_df, use_container_width=True)
                        
                        # Summary statistics
                        st.subheader("📊 Summary Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            total_return = (net_values[-1] - starting_value) / starting_value * 100
                            st.metric("Total Net Return", f"{total_return:.2f}%")
                        
                        with col2:
                            total_mgmt_fees = sum(mgmt_fees)
                            mgmt_charged_count = sum(mgmt_charged_list)
                            st.metric("Total Mgmt Fees", f"{total_mgmt_fees:.6f}")
                            st.caption(f"Charged {mgmt_charged_count} times ({mgmt_freq})")
                        
                        with col3:
                            total_perf_fees = sum(perf_fees_paid)
                            perf_paid_count = sum(1 for x in perf_fees_paid if x > 0)
                            st.metric("Total Perf Fees Paid", f"{total_perf_fees:.6f}")
                            st.caption(f"Paid {perf_paid_count} times ({perf_freq})")
                        
                        with col4:
                            final_net = net_values[-1]
                            st.metric("Final Net Value", f"{final_net:.10f}")
                        
                        # Download
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            display_df.to_excel(writer, index=False, sheet_name='Fee_Calculations')
                            
                            # Add a summary sheet with parameters
                            summary_data = {
                                'Parameter': [
                                    'Data Type',
                                    'Management Fee (Annual)',
                                    'Management Fee Frequency',
                                    'Performance Fee (Carry)',
                                    'Performance Fee Frequency',
                                    'Hurdle Rate (Annual)',
                                    'High Water Mark',
                                    '',
                                    'Total Net Return',
                                    'Total Management Fees',
                                    'Management Fees Charged Count',
                                    'Total Performance Fees',
                                    'Performance Fees Paid Count',
                                    'Final Net Value'
                                ],
                                'Value': [
                                    data_type,
                                    f"{mgmt_fee_annual}%",
                                    mgmt_freq,
                                    f"{carry_pct}%",
                                    perf_freq,
                                    f"{hurdle_rate}%",
                                    'Yes' if use_hwm else 'No',
                                    '',
                                    f"{total_return:.2f}%",
                                    f"{total_mgmt_fees:.6f}",
                                    mgmt_charged_count,
                                    f"{total_perf_fees:.6f}",
                                    perf_paid_count,
                                    f"{final_net:.10f}"
                                ]
                            }
                            summary_df = pd.DataFrame(summary_data)
                            summary_df.to_excel(writer, index=False, sheet_name='Summary')
                            
                            # Format worksheets
                            worksheet = writer.sheets['Fee_Calculations']
                            worksheet.set_column('A:Z', 15)
                            
                            summary_worksheet = writer.sheets['Summary']
                            summary_worksheet.set_column('A:A', 30)
                            summary_worksheet.set_column('B:B', 20)
                        
                        st.download_button(
                            "📥 Download Detailed Results (Excel)",
                            output.getvalue(),
                            f"fund_net_calculations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                            
    except ImportError:
        st.error("""
        ❌ Missing required library for Excel reading.
        
        Please install openpyxl:
        ```bash
        pip install openpyxl
        ```
        Then restart the app.
        """)
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        with st.expander("🔍 View Error Details"):
            st.exception(e)
        
else:
    st.info("👆 Please upload an Excel file to begin")
    
    st.subheader("📋 Expected File Format")
    st.markdown("""
    Your Excel file should have **2 columns** (additional columns will be ignored):
    - **Column 1**: Month (dates - any standard format)
    - **Column 2**: Gross/Net Return (numbers, decimals, or percentages)
    
    Example:
    """)
    
    example_df = pd.DataFrame({
        'Month': ['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30'],
        'Gross': ['7.86%', '-4.98%', '-8.09%', '21.02%']
    })
    st.dataframe(example_df)
    
    st.markdown("""
    **Features**:
    - ✅ Management fee frequency (Monthly/Quarterly/Yearly)
    - ✅ Performance fee frequency (Monthly/Quarterly/Yearly)
    - ✅ Fixed management fee as return reduction (matches Excel)
    - ✅ Performance fees calculated only at period end (no monthly accrual)
    - ✅ HWM updates only during performance fee periods
    - ✅ Automatic sheet detection (uses Sheet1 if available)
    - ✅ Handles percentage (7.89%) or decimal (0.0789) formats
    - ✅ Supports multiple date formats
    """)
