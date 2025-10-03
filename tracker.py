import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Expense Tracker Pro", page_icon=":money_with_wings:", layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .small-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .section-header {
    font-size: 1.8rem;
    color: #2c3e50;
    border-bottom: 3px solid #667eea;  
    padding-bottom: 0.5rem;
    margin: 2rem 0 1rem 0;
    }
    .expense-item {
        background-color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .welcome-card {
        text-align: center; 
        padding: 2rem; 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
        border-radius: 10px; 
        margin: 2rem 0;
    }
    .welcome-title {
        color: #2c3e50; 
        margin-bottom: 1rem;
    }
    .welcome-text {
        color: #7f8c8d; 
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

if "expenses" not in st.session_state:
    st.session_state.expenses=pd.DataFrame(columns=["Date","Category","Description","Amount"])
if "user_goals" not in st.session_state:
    st.session_state.user_goals = {"monthly_budget": 10000, "savings_target": 5000}
if "ai_insights" not in st.session_state:
    st.session_state.ai_insights = ""
st.markdown("<h1 class='main-header'>💰 Expense Tracker</h1>", unsafe_allow_html=True)

def generate_ai_insights(expenses_df):
    if expenses_df.empty:
        return "💡 Add your expense to get insights!"
    total_spent = expenses_df["Amount"].sum()
    insights = []
    if total_spent > st.session_state.user_goals["monthly_budget"]:
        insights.append(
            "🚨 **Budget Alert**: You've exceeded your monthly budget!")
    elif total_spent > st.session_state.user_goals["monthly_budget"] * 0.8:
        insights.append("⚠️ **Budget Warning**: You're approaching your monthly budget limit.")
    else:
        budget_remaining = st.session_state.user_goals["monthly_budget"] - total_spent
        insights.append(f"✅ **On Track**: You have ₹{budget_remaining:,.2f} remaining in your budget.")
    category_totals = expenses_df.groupby("Category")["Amount"].sum()
    if not category_totals.empty:
        top_category = category_totals.idxmax()
        top_amount = category_totals.max()
        insights.append(f"🎯 **Top Spending**: {top_category} is your largest expense at ₹{top_amount:,.2f}")
    return "\n\n".join(insights)

with st.sidebar:
    st.header("🔧 Add your daily expenses details below:")
    st.subheader(" 🎯 Financial Goals")

    with st.form("goals_form"):
        monthly_budget = st.number_input(
            "Monthly Budget (₹)",
            value=st.session_state.user_goals["monthly_budget"],
            min_value=1000,
            step=500
        )
        savings_target = st.number_input(
            "Savings Target (₹)",
            value=st.session_state.user_goals["savings_target"],
            min_value=1000,
            step=500
        )
        goals_submitted = st.form_submit_button("💾 Update Goals")
        if goals_submitted:
            st.session_state.user_goals = {
                "monthly_budget": monthly_budget,
                "savings_target": savings_target
            }
            st.success("Goals updated successfully!")

    st.markdown("---")
    st.subheader("➕ Add New Expense")
    with st.form("expense_form"):
        category = st.selectbox("Select Category",
                                ["🍕Food", "🏠 Rent", "✈️ Travel", "🛍 Shopping", "💳 Bills", "🎬 Entertainment",
                                 "🏥 Healthcare", "💡 Others"])
        amount = st.number_input("Enter Amount:", min_value=0.0, format="%.2f")
        description = st.text_input("Description (Optional):")
        date = st.date_input("Date:", datetime.now())

        submitted = st.form_submit_button("💾 Add Expense")

        if submitted:
            if amount > 0:
                new_expense = pd.DataFrame(
                    {"Category":[category],
                     "Amount":[amount],
                     "Description":[description if description else f"{category} expense"],
                     "Date":[date]
                     })
                st.session_state.expenses=pd.concat([st.session_state.expenses,new_expense],ignore_index=True)
                st.success(f"Added ₹{amount} to {category}!")
                st.session_state.ai_insights = generate_ai_insights(st.session_state.expenses)
            else:
                st.warning("Please enter a valid amount")
    st.subheader("🗑️ Delete Expense")
    if not st.session_state.expenses.empty:
        row_to_delete = st.number_input(
            "Row number to delete:",
            min_value=0,
            max_value=len(st.session_state.expenses) - 1,
            value=0,
            step=1,
            key="delete_row"
        )

        if st.button("🗑️ Delete Row", use_container_width=True):
            expense_to_delete = st.session_state.expenses.iloc[row_to_delete]
            st.session_state.expenses = st.session_state.expenses.drop(row_to_delete).reset_index(drop=True)
            st.session_state.ai_insights = generate_ai_insights(st.session_state.expenses)
            st.success(f"✅ Deleted: {expense_to_delete['Category']} - ₹{expense_to_delete['Amount']:.2f}")
            st.rerun()
    else:
        st.info("No expenses to delete")
    st.markdown("---")

    st.subheader("⚡ Quick Actions")
    if st.button("🗑️ Clear All Expenses"):
        st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount", "Date", "Description"])
        st.success("All expenses cleared!")
        st.rerun()
if not st.session_state.expenses.empty:
    st.markdown('<div class="section-header">📊 Expense Summary</div>',unsafe_allow_html=True)
    st.session_state.expenses = st.session_state.expenses.sort_values("Date", ascending=True)

    total_amount = st.session_state.expenses["Amount"].sum()
    total_expenses = len(st.session_state.expenses)
    weekly_total = total_amount
    monthly_total = weekly_total * 4
    avg_expense = total_amount / total_expenses
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="small-card">
            <h4>💰 Total Amount</h4>
            <h3>₹{total_amount:,.2f}</h3>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="small-card">
            <h4>📈 No. of Expenses</h4>
            <h3>{total_expenses}</h3>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="small-card">
            <h4>📅 Weekly Total</h4>
            <h3>₹{weekly_total:,.2f}</h3>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="small-card">
            <h4>🗓️ Monthly Total</h4>
            <h3>₹{monthly_total:,.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="section-header">🤖 AI Insights</div>', unsafe_allow_html=True)
    if not st.session_state.ai_insights:
        st.session_state.ai_insights = generate_ai_insights(st.session_state.expenses)

    st.info(st.session_state.ai_insights)
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Expense List</div>',unsafe_allow_html=True)
    display_df = st.session_state.expenses[["Date", "Category", "Description", "Amount"]].copy()
    display_df = display_df.sort_values("Date", ascending=False)
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(display_df, use_container_width=True)
    category_summary = st.session_state.expenses.groupby("Category")["Amount"].sum().reset_index()
    st.markdown('<div class="section-header">📈 Visual Analytics</div>', unsafe_allow_html=True)
    category_summary = st.session_state.expenses.groupby("Category")["Amount"].sum().reset_index()
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("**Spending by Category**")
        colors = ["#764ba2", "#ff9a9e", "#36d1dc", "#30e8bf", "#ffd200", "#F44336", "#a7bfe8", "#dce35b"]
        bar_chart = alt.Chart(category_summary).mark_bar().encode(
            x=alt.X("Category:N", title="Category", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Amount:Q", title="Amount (₹)"),
            color=alt.Color("Category:N", scale=alt.Scale(range=colors), legend=alt.Legend(title="Category"))
        ).properties(height=400)
        text = bar_chart.mark_text(align="center", baseline="bottom", dy=-5, color="black").encode(
            text=alt.Text("Amount:Q", format=".2f")
        )
        st.altair_chart(bar_chart + text, use_container_width=True)

    with chart_col2:
        st.write("**Spending Distribution**")
        fig = px.pie(category_summary, values='Amount', names='Category', color_discrete_sequence=colors)
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          marker=dict(line=dict(color='white', width=2)))
        fig.update_layout(height=400, showlegend=True, paper_bgcolor="#f7f9fc", plot_bgcolor="#f7f9fc")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.markdown(
        """<div class="welcome-card"><h3 class="welcome-title">📝 Start Tracking Your Expenses</h3><p class="welcome-text">Use the sidebar to add your first expense and begin your financial journey!</div>""",unsafe_allow_html=True)
