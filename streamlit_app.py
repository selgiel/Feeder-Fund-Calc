import streamlit as st
import pandas as pd
import io
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="Investment Fund Calculator", layout="wide")

st.title("Investment Fund Fee Calculator")

# Parameters always visible
st.subheader("💰 Fund Fee Mechanism")

# newly added
# STATIC DIAGRAM (no variables needed)

st.set_page_config(page_title="Fund Fee Flow", layout="wide")

import streamlit.components.v1 as components

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

        /* FLOWCHART SECTION */
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
            flex: 1 1 0px; /* Allows boxes to grow equally */
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

        /* MECHANISM SECTION */
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
            grid-template-columns: repeat(2, 1fr); /* 2 columns on desktop */
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

        /* RESPONSIVE LOGIC */
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
                grid-template-columns: 1fr; /* 1 column on mobile */
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
                <div class="title">🏦 AXSA Fund</div>
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
            <h3>🔄 Fee Flow Mechanism</h3>
            <h5>Depending on whether it is Gross or Net, the calculator will work on the Excel file accordingly to generate the final net value</h5>
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

# Height adjusted to 650 because the 2-column mechanism saves a lot of space
components.html(html_code, height=650, scrolling=True)


col1, col2 = st.columns(2)

with col1:
    data_type = st.radio("Gross or Net?", ["Gross", "Net"])
    mgmt_fee = st.number_input("Management Fee %", 0.0, 10.0, 2.0, 0.1)

with col2:
    carry_pct = st.number_input("Carry %", 0.0, 50.0, 20.0, 0.5)
    hurdle_rate = st.number_input("Hurdle Rate %", 0.0, 20.0, 8.0, 0.1)
    use_hwm = st.checkbox("High Water Mark", value=False)

# File upload
uploaded_file = st.file_uploader("Upload Excel (2 cols: Month, Gross/Net %)", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("✅ Original Data")
        st.dataframe(df, use_container_width=True)
        
        if len(df.columns) == 2:
            period_col, returns_col = df.columns
            
            # Parse returns (handles % strings like "7.89%")
            def parse_returns(series):
                cleaned = series.astype(str).str.rstrip('%').str.strip()
                return pd.to_numeric(cleaned, errors='coerce') / 100
            
            returns_decimal = parse_returns(df[returns_col])
            
            if returns_decimal.isna().all():
                st.error("❌ Cannot parse returns column. Expected numbers or % (e.g., 7.89 or 7.89%)")
            else:
                if st.button("🚀 Calculate", type="primary"):
                    result_df = df[[period_col, returns_col]].copy()
                    result_df[returns_col + '_Decimal'] = returns_decimal
                    
                    mgmt_dec = mgmt_fee / 100
                    carry_dec = carry_pct / 100
                    hurdle_dec = hurdle_rate / 100
                    
                    # Calculations
                    result_df['Gross %'] = returns_decimal * 100
                    result_df['Mgmt %'] = mgmt_fee
                    result_df['After Mgmt %'] = result_df['Gross %'] - mgmt_fee
                    
                    result_df['Hurdle Met'] = result_df['After Mgmt %'] > hurdle_rate
                    
                    if use_hwm:
                        result_df['Cum Net'] = (1 + returns_decimal - mgmt_dec).cumprod()
                        result_df['HWM'] = result_df['Cum Net'].cummax()
                        result_df['Perf Eligible'] = (result_df['Hurdle Met'] & 
                                                    (result_df['Cum Net'] > result_df['HWM'].shift(1, fill_value=1)))
                    else:
                        result_df['Perf Eligible'] = result_df['Hurdle Met']
                    
                    excess = np.maximum(0, result_df['After Mgmt %'] - hurdle_rate)
                    result_df['Perf Fee %'] = np.where(result_df['Perf Eligible'], excess * carry_dec * 100, 0)
                    result_df['Net %'] = result_df['After Mgmt %'] - result_df['Perf Fee %']
                    
                    # Display
                    display_cols = [period_col, returns_col, 'Gross %', 'Mgmt %', 'After Mgmt %', 
                                  'Hurdle Met', 'Perf Eligible', 'Perf Fee %', 'Net %']
                    if use_hwm:
                        display_cols += ['Cum Net', 'HWM']
                    
                    display_df = result_df[display_cols].round(2)
                    st.subheader("📈 Results")
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Summary
                    st.subheader("📊 Summary")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1: st.metric("Avg Net %", f"{display_df['Net %'].mean():.2f}")
                    with c2: st.metric("Perf Periods", f"{display_df['Perf Eligible'].sum()}/{len(df)}")
                    with c3: st.metric("Total Perf %", f"{display_df['Perf Fee %'].sum():.1f}")
                    with c4: st.metric("Hurdle Met %", f"{display_df['Hurdle Met'].mean()*100:.0f}%")
                    
                    # FIXED DOWNLOAD (xlsxwriter - no openpyxl needed)
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        display_df.to_excel(writer, index=False, sheet_name='Results')
                        worksheet = writer.sheets['Results']
                        worksheet.set_column('A:Z', 12)  # Auto-size columns
                    
                    st.download_button(
                        "📥 Download Excel",
                        output.getvalue(),
                        "fund_fees.xlsx",
                        "application/vnd.ms-excel"
                    )
        else:
            st.error("❌ Exactly 2 columns required!")
            
    except Exception as e:
        st.error(f"❌ File error: {str(e)}")
else:
    st.info("👆 Please upload an Excel file to begin")
    
    # Example format
    st.subheader("Expected File Format")
    st.markdown("""
    Your Excel file should have **exactly 2 columns**:
    - **Column 1**: Month (e.g. 31/12/2019)
    - **Column 2**: Gross (e.g., 7.86%)
    
    Example:
    """)
    
    example_df = pd.DataFrame({
        'Month': ['31/1/2020', '29/2/2020', '31/3/2020', '30/4/2020'],
        'Gross/ Net': ['7.89%', '2.21%', '1.1%', '9.2%']
    })
    st.dataframe(example_df)

st.markdown("**Tip**: Column 2 should be numbers or % (e.g., 7.89 or 7.89%)")
