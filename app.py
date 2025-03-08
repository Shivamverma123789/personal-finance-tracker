import streamlit as st
import pandas as pd
import plotly.express as px

# App Title
st.title(" Personal Finance Tracker")

# Sidebar Navigation
menu = ["Home", "Add Transaction", "View Analysis"]
choice = st.sidebar.selectbox("Menu", menu)

# Initialize session state for data storage
if "transactions" not in st.session_state:
    st.session_state["transactions"] = pd.DataFrame(columns=["Date", "Category", "Amount", "Type"])

# Function to add new transaction
def add_transaction(date, category, amount, transaction_type):
    new_data = pd.DataFrame([[date, category, amount, transaction_type]], 
                            columns=["Date", "Category", "Amount", "Type"])
    st.session_state["transactions"] = pd.concat([st.session_state["transactions"], new_data], ignore_index=True)

# Page: Add Transaction
if choice == "Add Transaction":
    st.subheader("Add a New Transaction")

    date = st.date_input("Transaction Date")
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Savings", "Other"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    transaction_type = st.radio("Transaction Type", ["Income", "Expense"])

    if st.button("Add"):
        add_transaction(date, category, amount, transaction_type)
        st.success("Transaction Added!")

# Page: View Analysis
elif choice == "View Analysis":
    st.subheader("Finance Analysis")
    
    if not st.session_state["transactions"].empty:
        df = st.session_state["transactions"]
        
        # Expense Breakdown
        expenses = df[df["Type"] == "Expense"]
        if not expenses.empty:
            st.subheader("Expense Breakdown by Category")
            fig = px.pie(expenses, names="Category", values="Amount", title="Expense Distribution")
            st.plotly_chart(fig)
        
        # Income vs Expense
        summary = df.groupby("Type")["Amount"].sum().reset_index()
        st.subheader("Income vs Expense")
        fig = px.bar(summary, x="Type", y="Amount", title="Income vs Expense", color="Type")
        st.plotly_chart(fig)

    else:
        st.warning("No transactions recorded yet!")

# Page: Home
else:
    st.write("Use the menu to add transactions and analyze your spending.")


# df = pd.DataFrame(data)
# df.to_csv("sales_data.csv")
# st.write(df)
# if name:
#     st.write(f"Hello,{name}")

# uploaded_file=st.file_uploader("Choose a CSV file",type="csv")

# if uploaded_file is not None:
#     df=pd.read_csv(uploaded_file)
#     st.write(df)

