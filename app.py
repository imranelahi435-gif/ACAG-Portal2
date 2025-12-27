import streamlit as st
import pandas as pd
import os

# App Configuration
st.set_page_config(page_title="ACAG Portal Search", layout="centered")

# Login Details
ADMIN_USER = "Imran.Elahi"
ADMIN_PASS = "Lootlomufta"
# ڈیٹا فائل کا نام (یقینی بنائیں کہ GitHub پر بھی یہی نام ہے)
DATA_FILE = "ACAG Portal Data.xlsx - Sheet1.csv"

# Session State for Login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Login Function
def login_page():
    st.markdown("<h2 style='text-align: center;'>لاگ ان پورٹل</h2>", unsafe_allow_html=True)
    with st.container():
        user = st.text_input("یوزر نیم")
        pas = st.text_input("پاس ورڈ", type="password")
        if st.button("لاگ ان کریں", use_container_width=True):
            if user == ADMIN_USER and pas == ADMIN_PASS:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("غلط یوزر نیم یا پاس ورڈ!")

# Main App Function
def main_app():
    st.sidebar.title("مینیو")
    option = st.sidebar.radio("آپشن منتخب کریں:", ["ریکارڈ سرچ کریں", "نیا ڈیٹا اپ لوڈ کریں"])

    # Load Data function
    def load_data():
        if os.path.exists(DATA_FILE):
            try:
                # 6 لاکھ ریکارڈز کے لیے dtype بتانا ضروری ہے تاکہ میموری کم استعمال ہو
                return pd.read_csv(DATA_FILE, dtype={'ApplicantCNIC': str, 'Batch No.': str, 'ApplicantName': str})
            except Exception as e:
                st.error(f"فائل پڑھنے میں مسئلہ: {e}")
                return None
        return None

    if option == "ریکارڈ سرچ کریں":
        st.header("🔎 ریکارڈ تلاش کریں")
        df = load_data()
        
        cnic_input = st.text_input("امیدوار کا CNIC نمبر لکھیں (بغیر ڈیش کے):")
        
        if st.button("سرچ کریں"):
            if df is not None:
                # سرچ کرنے کا عمل
                result = df[df['ApplicantCNIC'] == str(cnic_input)]
                
                if not result.empty:
                    st.success("ریکارڈ مل گیا!")
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                        <h4 style="color: #333;">نام: {result.iloc[0]['ApplicantName']}</h4>
                        <h4 style="color: #333;">بیچ نمبر: {result.iloc[0]['Batch No.']}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("کوئی ریکارڈ نہیں ملا۔ براہ کرم درست CNIC درج کریں۔")
            else:
                st.error("ڈیٹا فائل نہیں ملی۔ پہلے ڈیٹا اپ لوڈ کریں۔")

    elif option == "نیا ڈیٹا اپ لوڈ کریں":
        st.header("📤 ڈیٹا اپ ڈیٹ کریں")
        uploaded_file = st.file_uploader("نئی CSV فائل منتخب کریں", type=['csv'])
        
        if uploaded_file is not None:
            if st.button("فائل محفوظ کریں"):
                with open(DATA_FILE, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("ڈیٹا کامیابی سے اپ ڈیٹ ہو گیا! اب آپ سرچ کر سکتے ہیں۔")

# Logic to show Login or App
if not st.session_state['logged_in']:
    login_page()
else:
    main_app()
