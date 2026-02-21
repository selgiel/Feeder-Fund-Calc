import streamlit as st
import pandas as pd
import io
import numpy as np
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="FoF Calculator", layout="wide")
st.title("Investment Fund Fee Calculator")

st.subheader("💰 Fund Fee Mechanism")

# STATIC DIAGRAM
html_code = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; }
        body { margin: 0; padding: 10px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: transparent; }
        .container { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 1100px; margin: 0 auto; }
        .flowchart { display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 10px; padding: 20px 0; width: 100%; }
        .box { border: 4px solid; padding: 20px 15px; border-radius: 15px; text-align: center; font-weight: bold; box-shadow: 0 8px 20px rgba(0,0,0,0.1); flex: 1 1 0px; min-width: 150px; display: flex; flex-direction: column; justify-content: center; min-height: 140px; }
        .master { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-color: #4CAF50; }
        .axsa { background: linear-gradient(135deg, #2196F3, #1976D2); color: white; border-color: #2196F3; }
        .actual { background: linear-gradient(135deg, #FF9800, #F57C00); color: white; border-color: #FF9800; }
        .arrow { font-size: 28px; color: #475569; font-weight: bold; display: flex; align-items: center; justify-content: center; flex: 0 0 40px; animation: pulse 2s infinite; }
        .arrow::before { content: "➜"; }
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.6; transform: scale(1.1); } }
        .title { font-size: 16px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
        .big-text { font-size: 28px; font-weight: 900; line-height: 1; margin: 5px 0; }
        .label { font-size: 13px; opacity: 0.9; font-weight: 500; }
        .mechanism { margin-top: 20px; padding: 20px; background: rgba(255,255,255,0.7); border-radius: 15px; border: 1px solid rgba(0,0,0,0.05); }
        .mechanism h3 { text-align: center; margin-top: 0; margin-bottom: 15px; color: #1e293b; font-size: 18px; }
        .grid-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; list-style: none; padding: 0; margin: 0; }
        .grid-list li { background: white; padding: 10px 15px; border-radius: 8px; font-size: 14px; display: flex; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
        .grid-list li::before { content: "✓"; color: #10b981; font-weight: bold; margin-right: 10px; }
        @media (max-width: 800px) {
            .flowchart { flex-direction: column; gap: 5px; }
            .box { width: 100%; max-width: 400px; min-height: 120px; }
            .arrow::before { content: "⬇"; }
            .arrow { height: 40px; width: 100%; }
            .grid-list { grid-template-columns: 1fr; }
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
            <h3>🔄 Fee Flow Mechanism</h3>
            <ul class="grid-list">
                <li><b>Management Fee %</b>: Annual fee on AUM</li>
                <li><b>Management Fee Frequency</b>: How often management fee is charged</li>
                <li><b>Carry %</b>: Performance fee on profits</li>
                <li><b>Add-Back Method</b>: Prior accrued PF added back to GAV</li>
                <li><b>Crystallization</b>: Resets accrued PF going forward</li>
                <li><b>High Water Mark</b>: Benchmark for performance fees</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
components.html(html_code, height=650, scrolling=True)

st.subheader("This application converts **gross values** to **net values**:")

col1, col2 = st.columns(2)
with col1:
    mgmt_fee = st.number_input("Management Fee % (Annual)", 0.0, 10.0, 1.5, 0.1)
    carry_pct = st.number_input("Carry %", 0.0, 50.0, 10.0, 0.5)
    mgmt_freq = st.selectbox("Management Fee Frequency", ["Monthly", "Quarterly", "Yearly"], index=0)

with col2:
    pfm_freq = st.selectbox("Performance Fee Calculation Frequency", ["Monthly", "Quarterly", "Yearly"], index=2)
    crystal_freq = st.selectbox("Crystallization Frequency", ["Monthly", "Quarterly", "Yearly"], index=2)
    hurdle_rate = st.number_input("Hurdle Rate % (Annual)", 0.0, 20.0, 0.0, 0.1)
    use_hwm = st.checkbox("High Water Mark", value=True)

first_row_is_base = st.checkbox(
    "Treat first row as base row (Net Return % = 0 for first line)",
    value=True
)

uploaded_file = st.file_uploader("Upload Excel (2 cols: Month, Gross)", type=["xlsx", "xls"])

def parse_returns(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.rstrip("%").str.strip()
    numeric = pd.to_numeric(cleaned, errors="coerce")
    # Auto-detect percent-units vs decimals
    if numeric.dropna().abs().max() > 1:
        return numeric / 100.0
    return numeric

def is_calc_month(freq: str, month: int, is_year_end: bool) -> bool:
    if freq == "Monthly":
        return True
    if freq == "Quarterly":
        return month in [3, 6, 9, 12]
    if freq == "Yearly":
        return is_year_end
    return False

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("✅ Original Data")
        st.dataframe(df.head(20), use_container_width=True)

        if len(df.columns) < 2:
            st.error("❌ At least 2 columns required!")
            st.stop()

        period_col, returns_col = df.columns[0], df.columns[1]
        returns_decimal = parse_returns(df[returns_col])

        if returns_decimal.isna().all():
            st.error("❌ Cannot parse returns column.")
            st.stop()

        if st.button("🚀 Calculate", type="primary"):
            start_idx = 1 if first_row_is_base else 0

            starting_value = 1.0
            current_value = starting_value
            hwm = starting_value

            mgmt_fee_monthly = (mgmt_fee / 100.0) / 12.0
            carry_decimal = (carry_pct / 100.0)
            hurdle_monthly = (hurdle_rate / 100.0) / 12.0

            # KEY STATE: previous month accrued PF (liability) for add-back + incremental
            prev_accrued_pf = 0.0

            # Storage
            months = []
            beginning_values = []
            gross_returns = []
            pnl_values = []
            addback_perf = []
            adjusted_gav = []
            mgmt_fees = []
            mgmt_charged_list = []
            nav_before_pf_list = []
            accrued_pf_list = []
            incremental_pf_list = []
            cumulative_uncryst_list = []
            crystallized_list = []
            crystallization_amount_list = []
            closing_nav_list = []
            net_return_pct_list = []
            hwm_list = []

            # Optional base row line
            if first_row_is_base and len(df) > 0:
                months.append(df[period_col].iloc[0])
                beginning_values.append(starting_value)
                gross_returns.append(0.0)
                pnl_values.append(0.0)
                addback_perf.append(0.0)
                adjusted_gav.append(starting_value)
                mgmt_fees.append(0.0)
                mgmt_charged_list.append(False)
                nav_before_pf_list.append(starting_value)
                accrued_pf_list.append(0.0)
                incremental_pf_list.append(0.0)
                cumulative_uncryst_list.append(0.0)
                crystallized_list.append(False)
                crystallization_amount_list.append(0.0)
                closing_nav_list.append(starting_value)
                net_return_pct_list.append(0.0)
                hwm_list.append(hwm)

            for idx in range(start_idx, len(returns_decimal)):
                r = returns_decimal.iloc[idx]
                if pd.isna(r):
                    continue
                r = float(r)

                # Date/month
                try:
                    month_dt = pd.to_datetime(df[period_col].iloc[idx])
                    m = int(month_dt.month)
                    is_year_end = (m == 12)
                except Exception:
                    m = ((idx - start_idx) % 12) + 1
                    is_year_end = (m == 12)

                months.append(df[period_col].iloc[idx])

                opening_nav = current_value
                beginning_values.append(opening_nav)
                gross_returns.append(r)

                # 1) P&L
                pnl = opening_nav * r
                pnl_values.append(pnl)

                # 2) Add back prior accrued PF into GAV (sheet mechanism) [file:2]
                addback_perf.append(prev_accrued_pf)

                # 3) Adjusted GAV
                adj_gav = opening_nav + pnl + prev_accrued_pf
                adjusted_gav.append(adj_gav)

                # 4) Mgmt fee
                mgmt_charged = is_calc_month(mgmt_freq, m, is_year_end)
                mgmt_fee_amount = (adj_gav * mgmt_fee_monthly) if mgmt_charged else 0.0
                nav_before_pf = adj_gav - mgmt_fee_amount

                mgmt_fees.append(mgmt_fee_amount)
                mgmt_charged_list.append(mgmt_charged)
                nav_before_pf_list.append(nav_before_pf)

                # 5) Accrued PF MUST be computed monthly to match the workbook NAV logic [file:2]
                # NOTE: pfm_freq kept for display, but NAV-matching method accrues monthly.
                if use_hwm:
                    accrued_pf = max(0.0, (nav_before_pf - hwm)) * carry_decimal
                else:
                    period_ret = (nav_before_pf / opening_nav - 1.0) if opening_nav > 0 else 0.0
                    excess = max(0.0, period_ret - hurdle_monthly)
                    accrued_pf = opening_nav * excess * carry_decimal

                accrued_pf_list.append(accrued_pf)
                incremental_pf_list.append(accrued_pf - prev_accrued_pf)

                # 6) Closing NAV is net of the FULL accrued PF each month [file:2]
                closing_nav = nav_before_pf - accrued_pf
                closing_nav_list.append(closing_nav)

                # 7) Crystallization: reset accrual going forward, no additional NAV hit [file:2]
                crystallize = is_calc_month(crystal_freq, m, is_year_end)
                crystallized_list.append(crystallize)

                crystallization_amount = accrued_pf if (crystallize and accrued_pf > 0) else 0.0
                crystallization_amount_list.append(crystallization_amount)

                if crystallize and accrued_pf > 0:
                    prev_accrued_pf = 0.0
                    cumulative_uncryst_list.append(0.0)
                    if use_hwm:
                        hwm = closing_nav  # HWM after crystallization should be post-fee NAV [file:2]
                else:
                    prev_accrued_pf = accrued_pf
                    cumulative_uncryst_list.append(accrued_pf)

                # Net Return % based on NAV movement
                net_return_pct = ((closing_nav / opening_nav) - 1.0) * 100.0 if opening_nav > 0 else 0.0
                net_return_pct_list.append(net_return_pct)

                hwm_list.append(hwm)
                current_value = closing_nav

            result_df = pd.DataFrame({
                "Month": months,
                "Input Return %": [x * 100 for x in gross_returns],
                "Beginning NAV": beginning_values,
                "P&L (Before Mgmt)": pnl_values,
                "Add Back Uncryst PF": addback_perf,
                "Adjusted GAV": adjusted_gav,
                "Mgmt Fee": mgmt_fees,
                "Mgmt Charged?": mgmt_charged_list,
                "NAV before PF": nav_before_pf_list,
                "Accrued PF (Liability)": accrued_pf_list,
                "Incremental PF (Δ Liability)": incremental_pf_list,
                "Cumulative Uncryst PF": cumulative_uncryst_list,
                "Crystallized?": crystallized_list,
                "Crystallization Amount (Reset)": crystallization_amount_list,
                "Closing NAV": closing_nav_list,
                "Net Return %": net_return_pct_list,
                "HWM": hwm_list
            })

            st.subheader("📈 Detailed Results")
            st.dataframe(result_df.round(6), use_container_width=True)

            st.subheader("📊 Summary Statistics")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("Avg Net Return %", f"{result_df['Net Return %'].mean():.2f}%")
            with c2:
                st.metric("Total Mgmt Fees", f"{float(np.nansum(mgmt_fees)):.6f}")
            with c3:
                st.metric("Total Crystallization Amount", f"{float(np.nansum(crystallization_amount_list)):.6f}")
            with c4:
                st.metric("Uncrystallized PF", f"{float(cumulative_uncryst_list[-1]) if cumulative_uncryst_list else 0.0:.6f}")
            with c5:
                st.metric("Final NAV", f"{float(closing_nav_list[-1]) if closing_nav_list else starting_value:.6f}")

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                result_df.to_excel(writer, index=False, sheet_name="Results")

            st.download_button(
                "📥 Download Excel",
                output.getvalue(),
                f"fund_fees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ File error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
else:
    st.info("👆 Please upload an Excel file to begin")
