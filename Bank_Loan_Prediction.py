import streamlit as st
import pandas as pd
import pickle
import hashlib
import json
import os

# Load model
model_file_path = '/Users/pravinkumar/Documents/CSP/Loan_Data/Model/ML_Model.pkl'
with open(model_file_path, 'rb') as file:
    model = pickle.load(file)

# Load or create user data
user_data_file = 'user_data.json'
user_data = {}
if os.path.exists(user_data_file):
    try:
        with open(user_data_file, 'r') as file:
            user_data = json.load(file)
    except Exception as e:
        st.error(f"Error loading user data: {e}")

# Load or create user inputs
user_inputs_file = 'user_inputs.json'
user_inputs = {}
if os.path.exists(user_inputs_file):
    try:
        with open(user_inputs_file, 'r') as file:
            user_inputs = json.load(file)
    except Exception as e:
        st.error(f"Error loading user inputs: {e}")
language_data = {
    'English': {
        'title': "Bank Loan Prediction",
        'login': "Login",
        'register': "Register",
        'loan_prediction_form': "Loan Prediction Form",
        'account_no': "Account Number (10 digits)",
        'full_name': "Full Name",
        'gender': "Gender",
        'gender_options': ['Female', 'Male', 'Other'],
        'marital_status': "Marital Status",
        'marital_status_options': ['No', 'Yes'],
        'dependents': "Dependents",
        'dependents_options': ['No', 'One', 'Two', 'More than Two'],
        'education': "Education",
        'education_options': ['Not Graduate', 'Graduate'],
        'employment_status': "Employment Status",
        'employment_status_options': ['Job', 'Business'],
        'property_area': "Property Area",
        'property_area_options': ['Rural', 'Semi-Urban', 'Urban'],
        'credit_score': "Credit Score",
        'credit_score_options': ['Between 300 to 500', 'Above 500'],
        'monthly_income': "Applicant's Monthly Income (Rs)",
        'co_monthly_income': "Co-Applicant's Monthly Income (Rs)",
        'loan_amount': "Loan Amount",
        'loan_duration': "Loan Duration",
        'loan_duration_options': ['2 Months', '6 Months', '8 Months', '1 Year', '16 Months'],
        'password': "Password",
        'submit': "Submit",
        'feedback': "Feedback",
        'feedback_placeholder': "Type your feedback here...",
        'feedback_thank_you': "Thank you for your feedback!",
        'auth_failed': "Authentication failed. Please try again.",
        'auth_success': "Authentication successful!",
        'invalid_account': "Account number must be 10 digits.",
        'loan_denied': "Hello: {fn} || Account number: {account_no} || Loan Denied.",
        'loan_approved': "Hello: {fn} || Account number: {account_no} || Loan Approved.",
        'logout': "Logout",
        'logout_success': "You have been logged out.",
        'fill_required_fields': "Please fill in the required fields.",
        'feedback_word_limit': "Feedback must be at least 100 words.",
        'phone_number': "Phone Number",
        'email_id': "Email ID",
        'address': "Address",
        'pincode': "Pincode",
        'proof': "Proof",
        'proof_options': ["Aadhar Card", "Driving License", "PAN Card", "Others"],
    },
    'Tamil': {
        'title': "வங்கியின் கடன் கணிப்பு",
        'login': "உள்நுழைக",
        'register': "பதிவு செய்க",
        'loan_prediction_form': "கடன் கணிப்பு படிவம்",
        'account_no': "கணக்கு எண் (10 இலக்கங்கள்)",
        'full_name': "முழு பெயர்",
        'gender': "இருப்பிடம்",
        'gender_options': ['பெண்', 'ஆண்', 'மற்றவை'],
        'marital_status': "திருமண நிலை",
        'marital_status_options': ['இல்லை', 'ஆமென்று'],
        'dependents': "உறுப்பினர்கள்",
        'dependents_options': ['இல்லை', 'ஒரு', 'இரண்டு', 'இரண்டுக்கு மேற்பட்டோர்'],
        'education': "கல்வி",
        'education_options': ['இல்லை', 'இறுதிப் பரீட்சை'],
        'employment_status': "வேலை நிலை",
        'employment_status_options': ['வேலை', 'வியாபாரம்'],
        'property_area': "சொத்து பகுதி",
        'property_area_options': ['பட்டணம்', 'அரை-நகர', 'நகரம்'],
        'credit_score': "கடன் மதிப்பீடு",
        'credit_score_options': ['300 முதல் 500 வரை', '500 மேல்'],
        'monthly_income': "அவதானத்தின் மாத வருமானம் (Rs)",
        'co_monthly_income': "கொ-அவதானத்தின் மாத வருமானம் (Rs)",
        'loan_amount': "கடன் தொகை",
        'loan_duration': "கடன் காலம்",
        'loan_duration_options': ['2 மாதங்கள்', '6 மாதங்கள்', '8 மாதங்கள்', '1 ஆண்டு', '16 மாதங்கள்'],
        'password': "கடவுச்சொல்",
        'submit': "சமர்ப்பிக்கவும்",
        'feedback': "விளக்கம்",
        'feedback_placeholder': "உங்கள் கருத்துகளை இங்கே உள்ளிடவும்...",
        'feedback_thank_you': "உங்கள் கருத்துக்கு நன்றி!",
        'auth_failed': "அங்கீகாரம் தோல்வி. மீண்டும் முயற்சிக்கவும்.",
        'auth_success': "அங்கீகாரம் வெற்றிகரமாக!",
        'invalid_account': "கணக்கு எண் 10 இலக்கங்கள் இருக்க வேண்டும்.",
        'loan_denied': "வணக்கம்: {fn} || கணக்கு எண்: {account_no} || கடன் மறுக்கப்பட்டது.",
        'loan_approved': "வணக்கம்: {fn} || கணக்கு எண்: {account_no} || கடன் அங்கீகாரம் செய்யப்பட்டது.",
        'logout': "வெளியேறு",
        'logout_success': "நீங்கள் வெளிநடந்து விட்டீர்கள்.",
        'fill_required_fields': "தயவுசெய்து தேவையான துறைகளை நிரப்பவும்.",
        'feedback_word_limit': "விளக்கத்தில் குறைந்தது 100 வார்த்தைகள் இருக்க வேண்டும்.",
        'phone_number': "தொலைபேசி எண்",
        'email_id': "மின்னஞ்சல் ஐடி",
        'address': "முகவரி",
        'pincode': "பின் குறியீடு",
        'proof': "சாட்சி",
        'proof_options': ["ஆதார் அட்டை", "டிரൈവിങ் லைசென்", "பான் அட்டை", "மற்றவை"],
    },
    'Hindi': {
        'title': "बैंक ऋण अनुमान",
        'login': "लॉगिन",
        'register': "पंजीकरण",
        'loan_prediction_form': "ऋण अनुमान फॉर्म",
        'account_no': "खाता संख्या (10 अंकों का)",
        'full_name': "पूरा नाम",
        'gender': "लिंग",
        'gender_options': ['महिला', 'पुरुष', 'अन्य'],
        'marital_status': "वैवाहिक स्थिति",
        'marital_status_options': ['नहीं', 'हाँ'],
        'dependents': "निर्भर",
        'dependents_options': ['नहीं', 'एक', 'दो', 'दो से अधिक'],
        'education': "शिक्षा",
        'education_options': ['ग्रेजुएट नहीं', 'ग्रेजुएट'],
        'employment_status': "रोज़गार स्थिति",
        'employment_status_options': ['नौकरी', 'व्यापार'],
        'property_area': "सम्पत्ति क्षेत्र",
        'property_area_options': ['ग्रामीण', 'सेमी-शहरी', 'शहरी'],
        'credit_score': "क्रेडिट स्कोर",
        'credit_score_options': ['300 से 500 के बीच', '500 से ऊपर'],
        'monthly_income': "आवेदक की मासिक आय (Rs)",
        'co_monthly_income': "सह-आवेदक की मासिक आय (Rs)",
        'loan_amount': "ऋण राशि",
        'loan_duration': "ऋण की अवधि",
        'loan_duration_options': ['2 महीने', '6 महीने', '8 महीने', '1 साल', '16 महीने'],
        'password': "पासवर्ड",
        'submit': "सबमिट करें",
        'feedback': "प्रतिपुष्टि",
        'feedback_placeholder': "अपनी प्रतिक्रिया यहां लिखें...",
        'feedback_thank_you': "आपकी प्रतिक्रिया के लिए धन्यवाद!",
        'auth_failed': "प्रमाणन असफल। कृपया पुनः प्रयास करें।",
        'auth_success': "प्रमाणन सफल!",
        'invalid_account': "खाता संख्या 10 अंक की होनी चाहिए।",
        'loan_denied': "नमस्ते: {fn} || खाता संख्या: {account_no} || ऋण अस्वीकृत।",
        'loan_approved': "नमस्ते: {fn} || खाता संख्या: {account_no} || ऋण अनुमोदित।",
        'logout': "लॉगआउट",
        'logout_success': "आप लॉगआउट हो गए हैं।",
        'fill_required_fields': "कृपया आवश्यक फ़ील्ड भरें।",
        'feedback_word_limit': "प्रतिपुष्टि में कम से कम 100 शब्द होने चाहिए।",
        'phone_number': "फोन नंबर",
        'email_id': "ईमेल आईडी",
        'address': "पता",
        'pincode': "पिनकोड",
        'proof': "प्रमाण",
        'proof_options': ["आधार कार्ड", "ड्राइविंग लाइसेंस", "पैन कार्ड", "अन्य"],
    },
    'Telugu': {
        'title': "బ్యాంకు లోన్ అంచనావు",
        'login': "లోన్",
        'register': "నమోదు",
        'loan_prediction_form': "లోన్ అంచనా ఫార్మ్",
        'account_no': "ఖాతా సంఖ్య (10 అంకెల)",
        'full_name': "మొత్తం పేరు",
        'gender': "లింగం",
        'gender_options': ['స్త్రీ', 'పురుషుడు', 'ఇతర'],
        'marital_status': "వ్యవహార స్థితి",
        'marital_status_options': ['లేదు', 'అవును'],
        'dependents': "ఆధారితులు",
        'dependents_options': ['లేదు', 'ఒకటి', 'రెండు', 'రెండుకు మించి'],
        'education': "సిక్షణ",
        'education_options': ['గ్రాడ్యుయేట్ కాదు', 'గ్రాడ్యుయేట్'],
        'employment_status': "ఉద్యోగ స్థితి",
        'employment_status_options': ['ఉద్యోగం', 'వ్యాపారం'],
        'property_area': "సంపత్తి ప్రాంతం",
        'property_area_options': ['గ్రామీణ', 'అర్ధ-నగర', 'నగరం'],
        'credit_score': "క్రెడిట్ స్కోరు",
        'credit_score_options': ['300 నుంచి 500 మధ్య', '500 పైగా'],
        'monthly_income': "అవేదకుని నెలవారీ ఆదాయం (Rs)",
        'co_monthly_income': "కో-అవేదకుని నెలవారీ ఆదాయం (Rs)",
        'loan_amount': "లోన్ మొత్తం",
        'loan_duration': "లోన్ వ్యవధి",
        'loan_duration_options': ['2 నెలలు', '6 నెలలు', '8 నెలలు', '1 సంవత్సరం', '16 నెలలు'],
        'password': "పాస్వర్డ్",
        'submit': "సమర్పించు",
        'feedback': "ఫీడ్‌బ్యాక్",
        'feedback_placeholder': "మీ అభిప్రాయాన్ని ఇక్కడ రాయండి...",
        'feedback_thank_you': "మీ అభిప్రాయానికి ధన్యవాదాలు!",
        'auth_failed': "అంగీకారం విఫలమైంది. దయచేసి మళ్లీ ప్రయత్నించండి.",
        'auth_success': "అంగీకారం విజయవంతమైంది!",
        'invalid_account': "ఖాతా సంఖ్య 10 అంకెల్ ఉండాలి.",
        'loan_denied': "నమస్కారం: {fn} || ఖాతా సంఖ్య: {account_no} || లోన్ తిరస్కరించబడింది.",
        'loan_approved': "నమస్కారం: {fn} || ఖాతా సంఖ్య: {account_no} || లోన్ ఆమోదించబడింది.",
        'logout': "లాగౌట్",
        'logout_success': "మీరు లాగౌట్ అయ్యారు.",
        'fill_required_fields': "దయచేసి అవసరమైన ఫీల్డ్స్ నింపండి.",
        'feedback_word_limit': "ఫీడ్‌బ్యాక్ కనీసం 100 పదాలు ఉండాలి.",
        'phone_number': "ఫోన్ నంబర్",
        'email_id': "ఇమెయిల్ ఐడీ",
        'address': "చిరునామా",
        'pincode': "పిన్ కోడ్",
        'proof': "సాక్ష్యం",
        'proof_options': ["ఆధార్ కార్డు", "డ్రైవింగ్ లైసెన్స్", "పాన్ కార్డు", "ఇతర"],
    },
    'Malayalam': {
        'title': "ബാങ്ക് വായ്പാ കണക്കാക്കൽ",
        'login': "ലോഗിൻ",
        'register': "രജിസ്റ്റർ",
        'loan_prediction_form': "വായ്പാ കണക്കാക്കൽ ഫോം",
        'account_no': "അക്കൗണ്ട് നമ്പർ (10 അക്കങ്ങൾ)",
        'full_name': "പൂർണ്ണനാമം",
        'gender': "ലിംഗം",
        'gender_options': ['സ്ത്രീ', 'പുരുഷൻ', 'മറ്റത്'],
        'marital_status': "വിവാഹസ്ഥിതി",
        'marital_status_options': ['അല്ല', 'അതെ'],
        'dependents': "ആധാരിതർ",
        'dependents_options': ['അല്ല', 'ഒന്നും', 'രണ്ട്', 'രണ്ടിന് മുകളിൽ'],
        'education': "വിദ്യാഭ്യാസം",
        'education_options': ['അനധികൃത', 'സ്നാതകം'],
        'employment_status': "തൊഴിൽ നില",
        'employment_status_options': ['ജോലി', 'വ്യാപാരം'],
        'property_area': "സ്വത്തുവിഭാഗം",
        'property_area_options': ['ഗ്രാമീണ', 'അർദ്ധ-നഗര', 'നഗരം'],
        'credit_score': "ക്രെഡിറ്റ് സ്കോർ",
        'credit_score_options': ['300 മുതൽ 500 വരെ', '500-ൽ കൂടുതലാണ്'],
        'monthly_income': "അവേദകന്റെ മാസ വരുമാനം (Rs)",
        'co_monthly_income': "കോ-അവേദകന്റെ മാസ വരുമാനം (Rs)",
        'loan_amount': "വായ്പാ തുക",
        'loan_duration': "വായ്പാ കാലാവധി",
        'loan_duration_options': ['2 മാസം', '6 മാസം', '8 മാസം', '1 വർഷം', '16 മാസം'],
        'password': "പാസ്സ്‌വേഡ്",
        'submit': "സമർപ്പിക്കുക",
        'feedback': "ഫീഡ്‌ബാക്ക്",
        'feedback_placeholder': "നിങ്ങളുടെ അഭിപ്രായം ഇവിടെ ടൈപ്പ് ചെയ്യുക...",
        'feedback_thank_you': "നിങ്ങളുടെ അഭിപ്രായത്തിന് നന്ദി!",
        'auth_failed': "പ്രാമാണികത പരാജയപ്പെട്ടു. ദയവായി വീണ്ടും ശ്രമിക്കുക.",
        'auth_success': "പ്രാമാണികത വിജയകരമായി!",
        'invalid_account': "അക്കൗണ്ട് നമ്പർ 10 അക്കങ്ങൾ ആയിരിക്കണം.",
        'loan_denied': "ഹലോ: {fn} || അക്കൗണ്ട് നമ്പർ: {account_no} || വായ്പ നിരസിച്ചു.",
        'loan_approved': "ഹലോ: {fn} || അക്കൗണ്ട് നമ്പർ: {account_no} || വായ്പ അംഗീകരിച്ചു.",
        'logout': "ലോഗ് ഔട്ട്",
        'logout_success': "നിങ്ങൾ ലോഗ് ഔട്ടായി.",
        'fill_required_fields': "ദയവായി ആവശ്യമായ ഫീൽഡുകൾ പൂരിപ്പിക്കുക.",
        'feedback_word_limit': "ഫീഡ്‌ബാക്കിൽ കുറഞ്ഞത് 100 വാക്കുകൾ ഉണ്ടായിരിക്കണം.",
        'phone_number': "ഫോൺ നമ്പർ",
        'email_id': "ഇമെയിൽ ഐഡി",
        'address': "വിലാസം",
        'pincode': "പിൻ കോഡ്",
        'proof': "സാക്ഷ്യം",
        'proof_options': ["ആധാർ കാർഡ്", "ഡ്രൈവിങ് ലൈസൻസ്", "പാൻ കാർഡ്", "മറ്റത്"],
    },
}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Function to check if account exists
def account_exists(account_no):
    return account_no in user_data


# Function to validate login
def validate_login(account_no, password):
    if account_exists(account_no):
        stored_password_hash = user_data[account_no]['password']
        return stored_password_hash == hash_password(password)
    return False


# Function for user authentication
def authenticate_user(account_no, password):
    if validate_login(account_no, password):
        st.session_state['authenticated'] = True
        st.session_state['account_no'] = account_no
        st.success(lang['auth_success'])
    else:
        st.error(lang['auth_failed'])


# Language selection and dictionary setup
lang_options = list(language_data.keys())
selected_language = st.selectbox("Select Language", lang_options)
lang = language_data[selected_language]

st.title(lang['title'])

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'terms_visible' not in st.session_state:
    st.session_state.terms_visible = False

# Terms and Conditions Button
if st.button("Terms and Conditions"):
    st.session_state.terms_visible = not st.session_state.terms_visible


# Show Terms and Conditions based on the button click
if st.session_state.terms_visible:
    st.subheader("Terms and Conditions")
    st.write("""
    **Loan Prediction Terms and Conditions**

    **Introduction**

    By using our Loan Prediction service, you agree to the following terms and conditions, which outline the terms of use, data storage, and communication with the bank.

    **Data Collection and Storage**

    - **Personal Information:** We collect personal information, including but not limited to, your name, email address, phone number, and financial data, to provide loan prediction services.
    - **Data Storage:** We store your data on secure servers, using industry-standard encryption and security measures to protect your information.
    - **Data Retention:** We retain your data for a period of 5 years from the date of last interaction with our service, or as required by applicable laws and regulations.

    **Communication with the Bank**

    - **Contact Information:** By using our service, you consent to the bank contacting you via email, phone, or SMS to discuss loan options, provide updates, and request additional information.
    - **Communication Purpose:** The bank may contact you to:
        - Discuss loan eligibility and options
        - Request additional documentation or information
        - Provide loan approval or rejection notifications
        - Offer alternative financial products or services
    - **Opt-out:** You may opt-out of receiving communications from the bank at any time by contacting us in writing.

    **Data Sharing and Disclosure**

    - **Bank Partners:** We may share your data with our bank partners to facilitate loan processing and communication.
    - **Third-party Service Providers:** We may engage third-party service providers to assist with data processing, storage, and security. These providers are bound by confidentiality agreements and are prohibited from using your data for any other purpose.
    - **Legal Requirements:** We may disclose your data to comply with applicable laws, regulations, or court orders.

    **Security and Confidentiality**

    - **Data Protection:** We implement robust security measures to protect your data from unauthorized access, use, or disclosure.
    - **Confidentiality:** We maintain the confidentiality of your data and ensure that only authorized personnel have access to your information.

    **Governing Law and Jurisdiction**

    These terms and conditions shall be governed by and construed in accordance with the laws of [State/Country]. Any disputes arising out of or related to these terms shall be resolved through binding arbitration in accordance with the rules of the [Arbitration Association].

    **Changes to Terms and Conditions**

    We reserve the right to modify or update these terms and conditions at any time. Changes will be effective immediately upon posting on our website. Your continued use of our service constitutes acceptance of the updated terms.

    **Acceptance**

    By using our Loan Prediction service, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions.

    **Contact Us**

    If you have any questions or concerns about these terms and conditions, please contact us at
                 Email : loan_predction@gmail.com
                 (OR)
                 phone number : +91 9248390132
    """)

# User authentication logic
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


# User authentication logic
if not st.session_state['authenticated']:
    st.header("Login / Register")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login")
        account_no_login = st.text_input("Account Number (10 digits)", key='login_account_no')
        password_login = st.text_input("Password", type='password', key='login_password')

        if st.button("Login", key='login_submit'):
            authenticate_user(account_no_login, password_login)

    with register_tab:
        st.subheader("Register")
        account_no_register = st.text_input("Account Number (10 digits)", key='register_account_no')
        full_name_register = st.text_input("Full Name", key='register_full_name')
        password_register = st.text_input("Password", type='password', key='register_password')

        # Dropdown to select proof type
        proof_type = st.selectbox("Select the type of Proof of Identity",
                                  ["Aadhaar Card", "Driving License", "PAN Card", "Others"])

        # Conditional file uploader with specific messages
        if proof_type == "Aadhaar Card":
            proof_message = "Drag and drop your Aadhaar Card here\nLimit 200MB per file • JPG, JPEG, PNG, PDF"
        elif proof_type == "Driving License":
            proof_message = "Drag and drop your Driving License here\nLimit 200MB per file • JPG, JPEG, PNG, PDF"
        elif proof_type == "PAN Card":
            proof_message = "Drag and drop your PAN Card here\nLimit 200MB per file • JPG, JPEG, PNG, PDF"
        else:
            proof_message = "Drag and drop your proof here\nLimit 200MB per file • JPG, JPEG, PNG, PDF"

        # Identity proof file uploader
        proof_file = st.file_uploader(label=proof_message, type=["jpg", "jpeg", "png", "pdf"])

        # 3-year transaction file uploader
        proofs_type = st.selectbox("Previous 3 years Bank transaction proof", ["pdf", "other document"])
        proofs_message = "Drag and drop your 3-year Bank transaction details\nLimit 200MB per file • JPG, JPEG, PNG, PDF"
        proofs_file = st.file_uploader(label=proofs_message, type=["pdf"])

        # User information input
        phone_number = st.text_input("Phone Number")
        email_id = st.text_input("Email ID")
        address = st.text_area("Address")
        pincode = st.text_input("Pincode")
##############################################################################
        import streamlit as st
        import json
        import os
        from PIL import Image

        # Initialize session states
        if 'staff_logged_in' not in st.session_state:
            st.session_state.staff_logged_in = False
        if 'staff_login_active' not in st.session_state:
            st.session_state.staff_login_active = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "home"
        if 'search_result' not in st.session_state:
            st.session_state.search_result = None


        # Define navigation functions
        def go_to_home():
            st.session_state.current_page = "home"


        # Sidebar content (Staff login, Staff button, and user data search)
        with st.sidebar:
            st.markdown("### Staff Login")

            # Staff login form
            if not st.session_state.staff_logged_in:
                staff_id = st.text_input("Enter Staff ID", value="", key="staff_id_input")
                staff_password = st.text_input("Enter Password", value="", key="staff_password_input", type="password")
                login_button = st.button("Login", key="staff_login_button")

                # Check credentials for staff login
                if login_button:
                    if staff_id == "1234567890" and staff_password == "2005":
                        st.session_state.staff_logged_in = True
                        st.success("Login successful")
                    else:
                        st.error("Invalid Staff ID or Password")

            # Staff Button to navigate to staff dashboard (only shown when logged in)
            if st.session_state.staff_logged_in:
                st.markdown("### Staff Dashboard")

                # Search functionality
                account_number = st.text_input("Enter User Account Number", value="", key="account_number_input")
                search_button = st.button("Search", key="search_button")

                # Load user details from JSON file if available
                json_file_path = "/Users/pravinkumar/Documents/CSP/user_data.json"  # Adjusted to your actual file path

                if search_button and account_number:
                    # Check if file exists
                    if os.path.exists(json_file_path):
                        try:
                            with open(json_file_path, "r") as file:
                                # Attempt to load JSON data
                                all_user_data = json.load(file)

                            # Handle both possible structures: List or Dictionary
                            if isinstance(all_user_data, list):  # Case for List of User Dictionaries
                                user_details = next(
                                    (user for user in all_user_data if user.get("account_number") == account_number),
                                    None)

                            elif isinstance(all_user_data, dict):  # Case for Dictionary with account numbers as keys
                                user_details = all_user_data.get(account_number, None)

                            else:
                                user_details = None

                            # Store the result in session state for display
                            st.session_state.search_result = user_details if user_details else None
                            if st.session_state.search_result:
                                st.success("User data found!")
                            else:
                                st.warning("No user found with that account number.")
                        except json.JSONDecodeError:
                            st.error("Error decoding JSON file. Please check the file format.")
                    else:
                        st.error("User data file not found at the specified path. Please check the file path.")

                # Display user information if found
                user_details = st.session_state.search_result
                if user_details:
                    st.write("### User Details")
                    st.write("Phone Number:", user_details.get("phone_number", "Not provided"))
                    st.write("Email ID:", user_details.get("email_id", "Not provided"))
                    st.write("Address:", user_details.get("address", "Not provided"))
                    st.write("Pincode:", user_details.get("pincode", "Not provided"))

                    # Check for Proof of Identity file and 3-Year Transaction Proof
                    proof_file_path = f"/Users/pravinkumar/Documents/CSP/uploads/{account_number}/Bank_Loan_Prediction.pdf"
                    transaction_proof_file_path = f"/Users/pravinkumar/Documents/CSP/uploads/{account_number}/Transaction_Proof.pdf"

                    # Handle and display Proof of Identity
                    if os.path.exists(proof_file_path):
                        # If the file is a PDF
                        if proof_file_path.lower().endswith('.pdf'):
                            st.write(f"### Proof of Identity Uploaded:")
                            with open(proof_file_path, "rb") as pdf_file:
                                st.download_button(label="Download Proof of Identity", data=pdf_file,
                                                   file_name="Bank_Loan_Prediction.pdf", mime="application/pdf")
                        else:
                            try:
                                img = Image.open(proof_file_path)
                                st.write(f"### Proof of Identity Uploaded:")
                                st.image(img, caption="Proof of Identity", use_column_width=True)
                            except Exception as e:
                                st.error(f"Error displaying image: {e}")
                    else:
                        st.write("No Proof of Identity uploaded.")

                    # Handle and display 3-Year Transaction Proof
                    if os.path.exists(transaction_proof_file_path):
                        # If the file is a PDF
                        if transaction_proof_file_path.lower().endswith('.pdf'):
                            st.write(f"### 3-Year Transaction Proof Uploaded:")
                            with open(transaction_proof_file_path, "rb") as pdf_file:
                                st.download_button(label="Download 3-Year Transaction Proof", data=pdf_file,
                                                   file_name="Transaction_Proof.pdf", mime="application/pdf")
                        else:
                            try:
                                img = Image.open(transaction_proof_file_path)
                                st.write(f"### 3-Year Transaction Proof Uploaded:")
                                st.image(img, caption="3-Year Transaction Proof", use_column_width=True)
                            except Exception as e:
                                st.error(f"Error displaying image: {e}")

                elif search_button:
                    st.info("No user details available for the entered account number.")

                # Staff logout button inside the sidebar
                if st.button("Logout", key="staff_logout_button"):
                    st.session_state.staff_logged_in = False
                    st.session_state.search_result = None  # Clear search result on logout
                    go_to_home()
                    st.sidebar.success("Logged out successfully")

        ##############################################################################
        # Register button
        if st.button("Register", key='register_submit'):
            if len(account_no_register) == 10 and not account_exists(account_no_register):
                password_hash = hash_password(password_register)

                # Save the identity proof file if uploaded
                if proof_file is not None:
                    file_name = proof_file.name
                    save_directory = f"uploads/{account_no_register}/"
                    os.makedirs(save_directory, exist_ok=True)  # Ensure the directory exists
                    file_path = os.path.join(save_directory, file_name)
                    with open(file_path, "wb") as f:
                        f.write(proof_file.getbuffer())
                    st.success(f"File saved successfully: {file_path}")
                else:
                    st.warning("Please upload a proof of identity.")

                # Save the 3-year Bank transaction proof file if uploaded
                if proofs_file is not None:
                    file_name = proofs_file.name
                    save_directory = f"uploads/{account_no_register}/"
                    os.makedirs(save_directory, exist_ok=True)  # Ensure the directory exists
                    file_path = os.path.join(save_directory, file_name)
                    with open(file_path, "wb") as f:
                        f.write(proofs_file.getbuffer())
                    st.success(f"perivous 3-year transaction file saved successfully: {file_path}")
                else:
                    st.warning("Please upload your 3-year transaction proof.")
                # Store user data including the proof type and file path
                user_data[account_no_register] = {
                    'full_name': full_name_register,
                    'password': password_hash,
                    'proof_type': proof_type,
                    'proof_file': file_path,  # Store the path of the saved file
                    'phone_number': phone_number,
                    'email_id': email_id,
                    'address': address,
                    'pincode': pincode
                }
                try:
                    with open(user_data_file, 'w') as file:
                        json.dump(user_data, file)
                    st.success("Registration successful!")
                except Exception as e:
                    st.error(f"Error saving user data: {e}")
            else:
                st.error("Invalid account number or account already exists.")

if st.session_state['authenticated']:
    st.subheader(lang['loan_prediction_form'])

    if 'account_no' in st.session_state:
        account_no = st.session_state['account_no']
        fn = st.text_input(lang['full_name'], value=user_data.get(account_no, {}).get('full_name', ''))
        # Fix by adding a unique key for each text input
        phone_number = st.text_input(lang['phone_number'], value=user_data.get(account_no, {}).get('phone_number', ''),
                                     key="phone_number_input")

        # Similarly for email, address, etc.
        email_id = st.text_input(lang['email_id'], value=user_data.get(account_no, {}).get('email_id', ''),
                                 key="email_id_input")
        address = st.text_area(lang['address'], value=user_data.get(account_no, {}).get('address', ''),
                               key="address_input")
        pincode = st.text_input(lang['pincode'], value=user_data.get(account_no, {}).get('pincode', ''),
                                key="pincode_input")

        # Form for Loan Prediction
        with st.form("loan_form"):
            # Input fields for various parameters
            gen = st.selectbox(lang['gender'], lang['gender_options'])
            mar = st.selectbox(lang['marital_status'], lang['marital_status_options'])
            dep = st.selectbox(lang['dependents'], lang['dependents_options'])
            edu = st.selectbox(lang['education'], lang['education_options'])
            emp = st.selectbox(lang['employment_status'], lang['employment_status_options'])
            prop = st.selectbox(lang['property_area'], lang['property_area_options'])
            cred = st.selectbox(lang['credit_score'], lang['credit_score_options'])

            # Validate numerical inputs
            mon_income = st.number_input(lang['monthly_income'], value=0, min_value=0)
            co_mon_income = st.number_input(lang['co_monthly_income'], value=0, min_value=0)
            loan_amt = st.number_input(lang['loan_amount'], value=0, min_value=0)
            dur_display = st.selectbox(lang['loan_duration'], lang['loan_duration_options'])

            # Submit button for the form
            submit_button = st.form_submit_button(label=lang['submit'])

            if submit_button:
                if fn == "" or account_no == "" or phone_number == "" or email_id == "":
                    st.error(lang['fill_required_fields'])
                else:
                    # Mapping categorical variables to numeric values
                    gen_map = {'Male': 0, 'Female': 1, 'Other': 2}
                    mar_map = {'No': 0, 'Yes': 1}
                    dep_map = {'No': 0, 'One': 1, 'Two': 2, 'More than Two': 3}
                    edu_map = {'Not Graduate': 0, 'Graduate': 1}
                    emp_map = {'Job': 0, 'Business': 1}
                    prop_map = {'Rural': 0, 'Semi-Urban': 1, 'Urban': 2}
                    cred_map = {'Between 300 to 500': 0, 'Above 500': 1}

                    # Constructing the features array (all numeric now)
                    features = [[
                        gen_map[gen],
                        mar_map[mar],
                        dep_map[dep],
                        edu_map[edu],
                        emp_map[emp],
                        mon_income,
                        co_mon_income,
                        loan_amt,
                        int(dur_display.split()[0]),  # Convert duration to integer
                        cred_map[cred],
                        prop_map[prop]
                    ]]

                    # Making predictions with the numeric feature array
                    prediction = model.predict(features)
                    ans = int("".join(map(str, prediction)))

                    # Store user inputs
                    user_inputs[account_no] = {
                        'loan_amount': loan_amt,
                        'loan_duration': int(dur_display.split()[0]),
                        'credit_score': cred_map[cred]
                    }
                    try:
                        with open(user_inputs_file, 'w') as file:
                            json.dump(user_inputs, file)
                        if ans == 1:
                            st.success(lang['loan_approved'].format(fn=fn, account_no=account_no))
                        else:
                            st.error(lang['loan_denied'].format(fn=fn, account_no=account_no))
                    except Exception as e:
                        st.error(f"Error saving user inputs: {e}")

    # Feedback section outside the form
    st.subheader(lang['feedback'])
    feedback_text = st.text_area(lang['feedback'], height=150, placeholder=lang['feedback_placeholder'])

    if st.button("Submit Feedback"):
        if len(feedback_text.split()) < 1:
            st.error(lang['feedback_word_limit'])
        else:
            feedback_data = {}
            feedback_file = 'feedback_data.json'
            if os.path.exists(feedback_file):
                try:
                    with open(feedback_file, 'r') as file:
                        feedback_data = json.load(file)
                except Exception as e:
                    st.error(f"Error loading feedback data: {e}")

            feedback_data[account_no] = feedback_text
            try:
                with open(feedback_file, 'w') as file:
                    json.dump(feedback_data, file)
                st.success(lang['feedback_thank_you'])
            except Exception as e:
                st.error(f"Error saving feedback data: {e}")

    # Logout option
    if st.button(lang['logout']):
        st.session_state['authenticated'] = False
        st.session_state['account_no'] = None
        st.success(lang['logout_success'])


