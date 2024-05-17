import streamlit as st
import pandas as pd
import pickle

# Konfigurasi Page
st.set_page_config("By Firdita", page_icon=':moneyback:', layout='wide')

# Konfigurasi markdown Header
style = "<style>h2 {text-align: center ; }<style>"
st.markdown(style, unsafe_allow_html=True)

# Session state configuration
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Function
def load_model():
    with open("RFClassifier.sav", 'rb') as file:
        model = pickle.load(file)
        return model

def predict(data:pd.DataFrame):
    model = load_model()
    prob = model.predict_proba(data)
    prob = prob [:, 1]
    return prob


# Title
st.title("By Firdita")
st.write("Welcome to the By Firdita Desaigner")
st.divider()

with st.sidebar:
    st.header("MENU")
    st.divider()
    st.button("Home", use_container_width=True)
    st.button("Setting", use_container_width=True)
    st.button("About", use_container_width=True)

# Main Pages
# Membuat 2 kolom
left_panel, right_panel = st.columns(2, gap = "medium")

# left Panel
left_panel.header("Information Kebaya")
# Membuat Tabs Overview di Left Panel
tabs1, tabs2 = left_panel.tabs(['Overview', 'Benefits'])

# Tabs 1: Overview
tabs1.subheader("Overview")
tabs1.write("---Contoh saja---")
# Tabs 1: Benefits
tabs2.subheader("Benefits")
tabs2.write("---Contoh saja---")

# Right Panel
right_panel.header("Customer")

placeholder = right_panel.empty()
btn_placeholder = right_panel.empty()
feature_container = placeholder.container()

cust_name = feature_container.text_input("Customer Name", label_visibility='hidden', placeholder="Please input your Name")


feature_left, feature_right = feature_container.columns(2)
# Feature left 
feature_left.write("**Information**")
feature_left.divider()
age = feature_left.number_input("Age", min_value=17, max_value=60, step=1)
need_for = feature_left.selectbox("Need For", options=["Wedding", "Graduate", "Important event"])
income = feature_left.number_input("Annual Income", step=10)
family = feature_left.number_input("Family Size", min_value=1, max_value=50)
experience = feature_left.number_input("Profesional Experience", step=1)
mortgage = feature_left.number_input("Mortgage Value of house", step=10)

# Feature Right
feature_right.write("**Bank Account Information**")
feature_right.divider()
ccavg = feature_right.number_input("Monthly Credit Spending", step=10)
ccd = feature_right.selectbox("Have Credit Card Account", options=['Yes', 'No'])
cce = feature_right.selectbox("Have Certificate Deposit Account", options=['Yes', 'No'])
security = feature_right.selectbox("Have Security Account", options=['Yes', 'No'])
online = feature_right.selectbox("Using Internet banking", options=['Yes', 'No'])

# Mapping
Need_for_mapping = {"Wedding":1, "Graduate":2, "Important event":3}
need_for = Need_for_mapping[need_for]

bool_map ={"Yes":1, "No":0}
ccd = bool_map[ccd]
cce = bool_map[cce]
security = bool_map[security]
online = bool_map[online]


# Submit Button
feature_container.divider()
btn_submit = btn_placeholder.button("Submit", use_container_width=True)

if btn_submit:
    st.session_state['submitted'] = True

if st.session_state['submitted']:
    data = pd.DataFrame(data =[cust_name, age, need_for, income, family, experience, mortgage, ccavg,
                            ccd, cce, security, online],
                        columns=['Value'],
                        index=['Customer Name', 'Age', 'Education', 'Income', 'Family',
                                'Experience', 'Mortgage', 'CCAvg',
                                'CreditCard', 'CD Account', 'Securities Account',
                                'Online'])
    placeholder.dataframe(data, use_container_width=True)
    
    btn_placeholder.empty()
    btn_cancel = right_panel.button("Cancel", use_container_width=True)
    btn_predict = right_panel.button("Predict", use_container_width=True)

    if btn_cancel:
        st.session_state['submitted'] = False
        st.rerun()

    if btn_predict:
        data = data.T.drop('Customer Name', axis=1)
        pred = round(predict(data)[0] * 100, 2)
        right_panel.success(f'Customer With Name [cust_name] have (pred)% to accept the Personal Loan')
        st.balloons()
    