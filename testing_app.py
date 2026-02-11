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
                <div class="label">Before fees are applied (e.g. management fees)</div>
            </div>
            
            <div class="arrow"></div>
            
            <div class="box axsa">
                <div class="title">🏦 AXSA Fund (AXSA GROSS)</div>
                <div class="big-text">NET</div>
                <div class="label">Master Fund fees are applied (yet to apply AXSA-level fees)</div>
            </div>
            
            <div class="arrow"></div>
            
            <div class="box actual">
                <div class="title">💰 Actual Net</div>
                <div class="big-text">FINAL</div>
                <div class="label">After Carry + Hurdle</div>
            </div>
        </div>
        
        <div class="mechanism">
            <h3>🔄 Fee Flow Mechanism (Bellator Method)</h3>
            <ul class="grid-list">
                <li><b>Management Fee %</b>: Annual fee on AUM</li>
                <li><b>Management Fee Frequency</b>: How often management fee is charged</li>
                <li><b>Carry %</b>: Performance fee on profits</li>
                <li><b>Add-Back Method</b>: Previous month's uncrystallized fees added back to GAV</li>
                <li><b>Hurdle Rate %</b>: Minimum return threshold before performance fees apply</li>
                <li><b>High Water Mark</b>: Benchmark for performance fees</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

components.html(html_code, height=650, scrolling=True)

st.subheader('This application converts **gross values** to **net values**:')

col1, col2 = st.columns(2)

with col1:
    mgmt_fee = st.number_input("Management Fee % (Annual)", 0.0, 10.0, 1.5, 0.1)
    carry_pct = st.number_input("Carry %", 0.0, 50.0, 10.0, 0.5)
    mgmt_freq = st.selectbox("Management Fee Frequency", ["Monthly", "Quarterly", "Yearly"], index=0)
    
with col2:
    pfm_freq = st.selectbox("Performance Fee Calculation Frequency", ["Monthly", "Quarterly", "Yearly"], index=0)
    crystal_freq = st.selectbox("Crystallization Frequency", ["Monthly", "Quarterly", "Yearly"], index=2, help="When performance fees are actually paid out")
    hurdle_rate = st.number_input("Hurdle Rate % (Annual)", 0.0, 20.0, 0.0, 0.1)
    use_hwm = st.checkbox("High Water Mark", value=True)

# File upload
uploaded_file = st.file_uploader("Upload Excel (2 cols: Month, Gross %)", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("✅ Original Data")
        st.dataframe(df.head(20), use_container_width=True)
        
        if len(df.columns) >= 2:
            period_col, returns_col = df.columns[0], df.columns[1]
            
            # Parse returns
            def parse_returns(series):
                cleaned = series.astype(str).str.rstrip('%').str.strip()
                numeric = pd.to_numeric(cleaned, errors='coerce')
                return numeric.apply(lambda x: x / 100 if pd.notna(x) and abs(x) > 1 else x)
            
            returns_decimal = parse_returns(df[returns_col])
            
            if returns_decimal.isna().all():
                st.error("❌ Cannot parse returns column. Expected numbers or % (e.g., 7.89 or 7.89%)")
            else:
                if st.button("🚀 Calculate", type="primary"):
                    start_idx = 0
                    
                    if pd.isna(returns_decimal.iloc[0]) or abs(returns_decimal.iloc[0]) < 0.0001:
                        st.info(f"ℹ️ Detected base row: {df[period_col].iloc[0]} - Starting calculations from next row")
                        start_idx = 1
                    
                    # Initialize
                    starting_value = 1.0
                    current_value = starting_value
                    hwm = starting_value
                    prev_perf_accrual = 0.0  # Track previous period's uncrystallized perf fee
                    
                    # Calculate management fee rate (monthly basis)
                    mgmt_fee_monthly = mgmt_fee / 100 / 12
                    
                    # Calculate hurdle rate (monthly basis)
                    hurdle_monthly = hurdle_rate / 100 / 12
                    
                    carry_decimal = carry_pct / 100
                    
                    # Storage lists
                    months = []
                    beginning_values = []
                    gross_returns = []
                    pnl_values = []
                    addback_perf = []
                    adjusted_gav = []
                    mgmt_fees = []
                    mgmt_charged_list = []
                    after_mgmt_values = []
                    perf_accrual_list = []
                    incremental_perf_list = []
                    cumulative_uncryst_list = []
                    perf_crystallized = []
                    crystallized_list = []
                    ending_net_values = []
                    return_pcts = []
                    hwm_list = []
                    
                    if start_idx == 1:
                        months.append(df[period_col].iloc[0])
                        beginning_values.append(starting_value)
                        gross_returns.append(0.0)
                        pnl_values.append(0.0)
                        addback_perf.append(0.0)
                        adjusted_gav.append(starting_value)
                        mgmt_fees.append(0.0)
                        mgmt_charged_list.append(False)
                        after_mgmt_values.append(starting_value)
                        perf_accrual_list.append(0.0)
                        incremental_perf_list.append(0.0)
                        cumulative_uncryst_list.append(0.0)
                        perf_crystallized.append(0.0)
                        crystallized_list.append(False)
                        ending_net_values.append(starting_value)
                        return_pcts.append(0.0)
                        hwm_list.append(hwm)
                    
                    for idx in range(start_idx, len(returns_decimal)):
                        gross_return = returns_decimal.iloc[idx]
                        
                        if pd.isna(gross_return):
                            continue
                        
                        try:
                            month_dt = pd.to_datetime(df[period_col].iloc[idx])
                            current_month = month_dt.month
                            is_year_end = current_month == 12
                        except:
                            current_month = ((idx - start_idx) % 12) + 1
                            is_year_end = current_month == 12
                        
                        # Store month and beginning value
                        months.append(df[period_col].iloc[idx])
                        beginning_value = current_value
                        beginning_values.append(beginning_value)
                        gross_returns.append(gross_return)
                        
                        # Step 1: Calculate P&L (Before Management Fees)
                        pnl = current_value * gross_return
                        pnl_values.append(pnl)
                        
                        # Step 2: Add Back Previous Uncrystallised Performance Fee
                        addback_perf.append(prev_perf_accrual)
                        
                        # Step 3: Adjusted GAV = Opening + P&L + Add Back
                        adj_gav = current_value + pnl + prev_perf_accrual
                        adjusted_gav.append(adj_gav)
                        
                        # Step 4: Apply management fee
                        mgmt_charged = False
                        if mgmt_freq == "Monthly":
                            mgmt_charged = True
                        elif mgmt_freq == "Quarterly":
                            mgmt_charged = current_month in [3, 6, 9, 12]
                        elif mgmt_freq == "Yearly":
                            mgmt_charged = is_year_end
                        
                        mgmt_fee_amount = adj_gav * mgmt_fee_monthly if mgmt_charged else 0.0
                        after_mgmt = adj_gav - mgmt_fee_amount
                        
                        mgmt_fees.append(mgmt_fee_amount)
                        mgmt_charged_list.append(mgmt_charged)
                        after_mgmt_values.append(after_mgmt)
                        
                        # Step 5: Calculate Performance Fee Accrual (EVERY MONTH)
                        perf_accrual = 0.0
                        
                        if use_hwm:
                            if after_mgmt > hwm:
                                perf_accrual = (after_mgmt - hwm) * carry_decimal
                        else:
                            period_return = (after_mgmt - current_value) / current_value if current_value > 0 else 0
                            if period_return > hurdle_monthly:
                                excess_return = period_return - hurdle_monthly
                                perf_accrual = current_value * excess_return * carry_decimal
                        
                        perf_accrual_list.append(perf_accrual)
                        
                        # Step 6: Calculate incremental change
                        incremental = perf_accrual - prev_perf_accrual
                        incremental_perf_list.append(incremental)
                        
                        # Step 7: Check if performance fee should be CRYSTALLIZED
                        should_crystallize = False
                        if crystal_freq == "Yearly":
                            should_crystallize = is_year_end
                        elif crystal_freq == "Quarterly":
                            should_crystallize = current_month in [3, 6, 9, 12]
                        elif crystal_freq == "Monthly":
                            should_crystallize = True
                        
                        perf_paid = 0.0
                        cumulative_uncrystallized = perf_accrual  # Always show current accrual
                        
                        if should_crystallize and perf_accrual > 0:
                            perf_paid = perf_accrual
                            if use_hwm:
                                hwm = after_mgmt  # Update HWM to after_mgmt (before deducting perf fee)
                            cumulative_uncrystallized = 0.0  # Reset after crystallization
                            prev_perf_accrual = 0.0  # Reset for next period
                        else:
                            # Store for next period's add-back
                            prev_perf_accrual = perf_accrual
                        
                        perf_crystallized.append(perf_paid)
                        crystallized_list.append(should_crystallize)
                        cumulative_uncryst_list.append(cumulative_uncrystallized)
                        
                        # Step 8: Final Net Value = After Mgmt - Crystallized Perf Fee
                        final_net = after_mgmt - perf_paid
                        ending_net_values.append(final_net)
                        
                        # Step 9: Calculate return %
                        return_pct = ((final_net - beginning_value) / beginning_value * 100) if beginning_value > 0 else 0
                        return_pcts.append(return_pct)
                        
                        # Store HWM
                        hwm_list.append(hwm)
                        
                        # Update for next iteration
                        current_value = final_net
                    
                    # Create results DataFrame
                    result_df = pd.DataFrame({
                        'Month': months,
                        'Input Return %': [r * 100 for r in gross_returns],
                        'Beginning NAV': beginning_values,
                        'P&L (Before Mgmt)': pnl_values,
                        'Add Back Uncryst PF': addback_perf,
                        'Adjusted GAV': adjusted_gav,
                        'Mgmt Fee': mgmt_fees,
                        'Mgmt Charged?': mgmt_charged_list,
                        'After Mgmt (Gross for PF)': after_mgmt_values,
                        'Perf Fee Accrued (Monthly)': perf_accrual_list,
                        'Incremental Perf Fee': incremental_perf_list,
                        'Cumulative Uncryst PF': cumulative_uncryst_list,
                        'Crystallized?': crystallized_list,
                        'Perf Fee Paid': perf_crystallized,
                        'Closing NAV': ending_net_values,
                        'Net Return %': return_pcts,
                        'HWM': hwm_list
                    })
                    
                    # Display results
                    st.subheader("📈 Detailed Results")
                    st.dataframe(result_df.round(6), use_container_width=True)
                    
                    # Summary
                    st.subheader("📊 Summary Statistics")
                    c1, c2, c3, c4, c5 = st.columns(5)
                    with c1:
                        avg_return = result_df['Net Return %'].mean()
                        st.metric("Avg Net Return %", f"{avg_return:.2f}%")
                    with c2:
                        total_mgmt = sum(mgmt_fees)
                        st.metric("Total Mgmt Fees", f"{total_mgmt:.6f}")
                    with c3:
                        total_perf = sum(perf_crystallized)
                        st.metric("Total Perf Fees Paid", f"{total_perf:.6f}")
                    with c4:
                        current_uncryst = cumulative_uncryst_list[-1] if cumulative_uncryst_list else 0
                        st.metric("Uncrystallized PF", f"{current_uncryst:.6f}")
                    with c5:
                        final_value = ending_net_values[-1]
                        st.metric("Final NAV", f"{final_value:.6f}")
                    
                    # Download
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False, sheet_name='Results')
                        
                        summary_df = pd.DataFrame({
                            'Parameter': ['Method', 'Management Fee', 'Mgmt Frequency', 'Performance Fee', 
                                        'Perf Calc Frequency', 'Crystallization Frequency', 'Hurdle Rate', 'High Water Mark', 
                                        '', 'Avg Net Return %', 'Total Mgmt Fees', 'Total Perf Fees', 
                                        'Uncrystallized PF', 'Final NAV'],
                            'Value': ['Bellator Add-Back', f"{mgmt_fee}%", mgmt_freq, f"{carry_pct}%", 
                                    pfm_freq, crystal_freq, f"{hurdle_rate}%", 'Yes' if use_hwm else 'No',
                                    '', f"{avg_return:.2f}%", f"{total_mgmt:.6f}", 
                                    f"{total_perf:.6f}", f"{current_uncryst:.6f}", f"{final_value:.6f}"]
                        })
                        summary_df.to_excel(writer, index=False, sheet_name='Summary')
                    
                    st.download_button(
                        "📥 Download Excel",
                        output.getvalue(),
                        f"fund_fees_bellator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.error("❌ At least 2 columns required!")
            
    except Exception as e:
        st.error(f"❌ File error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
else:
    st.info("👆 Please upload an Excel file to begin")
    
    st.subheader("Expected File Format")
    st.markdown("""
    Your Excel file should have **exactly 2 columns**:
    - **Column 1**: Month (e.g. 2020-01-31)
    - **Column 2**: Gross Returns (e.g., 7.86% or 0.0786)
    
    Example:
    """)
    
    example_df = pd.DataFrame({
        'Month': ['2019-12-31', '2020-01-31', '2020-02-29', '2020-03-31'],
        'Gross': ['0%', '7.86%', '-4.98%', '-8.09%']
    })
    st.dataframe(example_df)

st.markdown("**Tip**: Returns should be in % format (7.86%) or decimal (0.0786)")
