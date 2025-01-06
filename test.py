# Libraries
import joblib
import numpy as np
import streamlit as st
from data import *  # Data
from graphs import *  # Graph Functions
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu

# Defining Functions

def nextpage():
    if username == "admin" and password == "123":
        st.session_state.page += 1
    else:
        st.error("Incorrect username or password")

def restart():
    st.session_state.page = 0

def predict(data, amt):
    encoded_values = encoder.transform([data])
    encoded_data = np.insert(encoded_values, 0, amt)
    prediction = model.predict([encoded_data])
    return prediction

def display_graph(graph_type):
    if graph_type == 'fraud transaction':
        d = df["is_fraud"].value_counts().reset_index()
        d.columns = ['is_fraud', 'count']
        fig = px.pie(d, values="count", names=['No', 'Yes'], hole=0.40, opacity=0.9)
        st.plotly_chart(fig)
    elif graph_type == 'gender analysis':
        df_fraud = df[df['is_fraud'] == 1]
        plt.figure(figsize=(5, 2))
        sns.countplot(x=df_fraud['gender'], color='tomato', width=0.3)
        st.pyplot(plt)
    elif graph_type == 'category analysis':
        df_fraud = df[df['is_fraud'] == 1]
        plt.figure(figsize=(10, 5))
        sns.countplot(x='category', data=df_fraud, palette='winter')
        st.pyplot(plt)
    elif graph_type == 'amount distribution':
        df_fraud = df[df['is_fraud'] == 1]
        amounts = df_fraud['amt']
        bins = [0, 100, 500, 1000, 5000]
        labels = ['0-100', '101-500', '501-1000', '1001-5000']
        df_fraud['amount_range'] = pd.cut(amounts, bins=bins, labels=labels)
        plt.figure(figsize=(8, 4))
        sns.countplot(x='amount_range', data=df_fraud, palette='summer')
        st.pyplot(plt)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 0

# Load models (only once)
model = joblib.load('model.pkl')
encoder = joblib.load('encoder_model.pkl')

if st.session_state.page == 0:
    # Code 1's Login Page
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(45deg, #FF0000, #FF7F00, #FF1493, #0000FF, #4B0082, #8B00FF);
            background-size: 400% 400%;
            animation: gradient 10s ease infinite;
            color: white;
        }
        # @keyframes gradient {
        #     0% { background-position: 0% 50%; }
        #     50% { background-position: 100% 50%; }
        #     100% { background-position: 0% 50%; }
        # }
        .header {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        .subheading {
            font-size: 20px;
            text-align: center;
            margin-bottom: 30px;
        }
        /* Make text input labels white */
        div[data-testid="stTextInput"] label {
            color: white !important;
            font-size: 16px;
            font-weight: bold;
        }
            /* Style for the Login button */
        div.stButton > button {
            color: red !important; /* Text color red */
            background-color: white !important; /* Optional: Change button background */
            font-size: 16px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px 20px;
            border: 2px solid red; /* Optional: Add a border */
        }
        # div.stButton > button:hover {
        #     background-color: red !important; /* Optional: Background changes on hover */
        #     color: white !important; /* Optional: Text color changes on hover */
        # }
        </style>
        """,
        unsafe_allow_html=True
    )

    image_path = r"./ch_prev_ui.png"  # Update the path if necessary

    try:
        logo = Image.open(image_path)
        logo = logo.convert("RGBA")
        data = logo.getdata()
        new_data = [
            (255, 255, 255, 0) if item[0] in list(range(200, 256)) and item[1] in list(range(200, 256)) and item[2] in list(range(200, 256)) else item
            for item in data
        ]
        logo.putdata(new_data)

        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(logo, width=150)
            st.markdown("<div style='text-align: left; margin-left: -30px;'> </div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="header">Smart Defence for Your Funds</div>', unsafe_allow_html=True)
            st.markdown('<div class="subheading">Why Choose Us?</div>', unsafe_allow_html=True)

        left_col, right_col = st.columns(2)
        with left_col:
            st.markdown('<h3 style="color: white;">About Our App</h3>', unsafe_allow_html=True)
            st.write(
                "Many credit cards are lost, stolen, or expired. But these cards can still be used by others. "
                "This app provides AI-powered immediate detection and prevention of fraudulent transactions, ensuring precision with minimal false positives."
            )
        with right_col:
            st.markdown('<h3 style="color: white;">Login</h3>', unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if username == "admin" and password == "123":
                    st.session_state.page += 1
                else:
                    st.error("Invalid username or password")
    except Exception as e:
        st.error(f"Error loading the image: {e}")

elif st.session_state.page == 1:
    page_bg_img = f'''
    <style>
            /* Minimalist Sidebar styling */
            [data-testid=stSidebar] {{
                background-color: white;
                padding: 20px;
                border: 2px solid black;
                margin-top: -100px;
            }}
            /* Sidebar link styling */
            .sidebar-link {{
                display: block;
                padding: 10px 0;
                font-size: 18px;
                color: #333;
                text-decoration: none;
            }}
            .sidebar-link:hover {{
                color: #ff0000;
            }}
            /* Add margin to move the images down by 50px */
            .image-container img {{
                margin-top: 50px;
            }}
    </style>
    '''

    # Inject custom CSS
    st.markdown(page_bg_img, unsafe_allow_html=True)

    with st.sidebar:
        # Custom CSS to adjust the logo position
        st.markdown(
            '''
            <style>
                /* Move the logo upwards by 100px */
                img {{
                    margin-top: -100px;  
                }}
            </style>
            ''',
            unsafe_allow_html=True
        )
        # Increase logo width
        st.image("./logo.jpg", width=200, use_column_width=False, output_format="auto", caption="")  # Increase logo width
        
        # Sidebar with menu options
        selected = option_menu("Main Menu", ["Home", 'Analytics', 'About', 'Contact Us'],
                               icons=['house', 'file-earmark-check', 'cloud-arrow-down', 'info-square', 'envelope'],
                               menu_icon="cast", default_index=0,
                               styles={"nav-link-selected": {"background-color": "green"}})

    if selected == "Home":
        st.header(':blue[Transaction Fraud Prediction]')

        # Streamlit page content
        amt = st.number_input('**:green[Amount of Transaction in K]**', min_value=0.0, step=1.0)

        cat = st.selectbox("**:green[Category]**", [""] + categories)  # Add a blank option
        gen = st.selectbox("**:green[Gender]**", [""] + genders)       # Add a blank option
        city = st.selectbox("**:green[City]**", [""] + cities)         # Add a blank option
        state_name = st.selectbox("**:green[State]**", [""] + list(states_dict.values()))  # Add a blank option

        job = st.selectbox("**:green[Job]**", [""] + jobs)  # Add a blank option
        state = [abbr for abbr, name in states_dict.items() if name == state_name][0] if state_name else ""

        sub = st.button('**Check Transaction**')

        # Validate inputs
        if sub:
            if (
                amt <= 0 or 
                not cat or 
                not gen or 
                not city or 
                not state_name or 
                not job
            ):
                st.error("Please fill out all inputs before proceeding.")
            else:
                # Prepare data for prediction
                data = [cat, gen, city, state, job]
                predictions = predict(data, amt)
                if predictions[0] == 0:
                    st.success('This Transaction is Safe.', icon="✅")
                else:
                    st.error('This Transaction may be Fraudulent.', icon="⚠️")
    elif selected == "Analytics":
        st.header('Analytics', divider='rainbow')
        # Sample dataset (you can replace this with actual data)

        data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Values': [4, 3, 2, 1]
        })

        # Display an option menu above the graph
        selected_graph = option_menu(
            menu_title=None,
            options=['fraud transaction', 'gender analysis', 'category analysis', 'amount distribution'],
            icons=['housscse', 'filecsc-earmark-check', 'cloudcsc-arrow-down', 'infocscs-square', 'envelopecsc'],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0px",
                    "background-color": "#f0f0f0", 
                    "margin-bottom": "20px"  # Set margin-bottom to 20px for more space below nav
                },
                "nav-link": {
                    "font-size": "16px", 
                    "color": "black",
                    "min-width": "fit-content",
                    "text-align": "center", 
                    "font-weight": "normal"  # Ensure text is normal weight
                },
                "nav-link-selected": {
                    "background-color": "#4a90e2", 
                    "color": "white", 
                    "font-weight": "normal"  # Prevent bold on selection
                },
            }
        )

        # Display the selected graph
        display_graph(selected_graph)

    elif selected == "About":
        st.header('About', divider='rainbow')
        st.write(''':blue[A web Based Application which requires some features about the transaction such as Transaction amount,
Transaction Purpose, Previous loan, G. Then, it predicts whether the transaction is fraudulent or safe.]''')

    elif selected == "Contact Us":
        st.header('Contact Us', divider='rainbow')
        st.write(':blue[If you have any questions about this Progressive Web App. You can contact us:]')
        st.write(':green[**By email: motubas@gmail.com**]')
