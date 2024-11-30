# Libraries
import joblib
import numpy as np
import streamlit as st
from data import *  # Data
from graphs import *  # Graph Functions
import base64
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from streamlit_option_menu import option_menu

# Defining Functions

def nextpage():
    if username == "admin" and password == "123":
        st.session_state.page += 1
    else:
        st.error("Incorrect username or password")

def restart():
    st.session_state.page = 0

# Make predictions function
def predict(data, amt):
    encoded_values = encoder.transform([data])
    encoded_data = np.insert(encoded_values, 0, amt)
    print(encoded_data)
    prediction = model.predict([encoded_data])
    return prediction


        # Function to display different graphs
def display_graph(graph_type):
    if graph_type == 'Bar Plot':
        st.header('Bar Plot')
        plt.figure(figsize=(10, 5))
        sns.barplot(x=data['Category'], y=data['Values'])
        st.pyplot(plt)
    
    elif graph_type == 'Line Plot':
        st.header('Line Plot')
        plt.figure(figsize=(10, 5))
        plt.plot(data['Category'], data['Values'], marker='o')
        st.pyplot(plt)
        
    elif graph_type == 'Scatter Plot':
        st.header('Scatter Plot')
        x = np.random.randn(100)
        y = np.random.randn(100)
        plt.figure(figsize=(10, 5))
        plt.scatter(x, y)
        st.pyplot(plt)
    
    elif graph_type == 'Histogram':
        st.header('Histogram')
        values = np.random.randn(1000)
        plt.figure(figsize=(10, 5))
        plt.hist(values, bins=20, color='blue', edgecolor='black')
        st.pyplot(plt)
    
    elif graph_type == 'Heatmap':
        st.header('Heatmap')
        matrix_data = np.random.rand(10, 12)
        plt.figure(figsize=(10, 5))
        sns.heatmap(matrix_data, annot=True, cmap='coolwarm')
        st.pyplot(plt)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 0

# Load models (only once)
model = joblib.load('model.pkl')
encoder = joblib.load('encoder_model.pkl')

# Page Logic
if st.session_state.page == 1:
    # Login page
    st.header(':blue[Login]')
    username = st.text_input("**Username:**")
    password = st.text_input("**Password:**", type="password")
    st.button("**Submit**", on_click=nextpage)

elif st.session_state.page == 0:
    page_bg_img = f'''
    <style>
            /* Minimalist Sidebar styling */
            [data-testid=stSidebar] {{
                background-color: white;
                padding: 20px;
                border: 2px solid black;
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
                img {
                    margin-top: -100px;  
                }
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
        amt = st.number_input('**:green[Amount of Transaction in K]**')

        cat = st.selectbox("**:green[Category]**", categories)

        gen = st.selectbox("**:green[Gender]**", genders)

        city = st.selectbox("**:green[City]**", cities)

        state_name = st.selectbox("**:green[State]**", list(states_dict.values()))
        state = [abbr for abbr, name in states_dict.items() if name == state_name][0]

        job = st.selectbox("**:green[Job]**", jobs)

        sub = st.button('**Check Transaction**')

        data = [cat, gen, city, state, job]

        # Prediction function
        if sub:
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
            options=['Bar Plot', 'Line Plot', 'Scatter Plot', 'Histogram', 'Heatmap'],
            icons=['bar-chart', 'activity', 'scatter-plot', 'bar-chart-fill', 'grid'],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0px", 
                    "background-color": "#f0f0f0", 
                    "margin-bottom": "100px"  # Set margin-bottom to 100px
                },
                "nav-link": {
                    "font-size": "16px", 
                    "color": "black", 
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
        st.write(':blue[**Draikin is a prediagnostic progressive web app that helps to scan and analyse skin pathology.**]')

    elif selected == "Contact Us":
        st.header('Contact Us', divider='rainbow')
        st.write(':blue[If you have any questions about this Progressive Web App. You can contact us:]')
        st.write(':green[**By email: motubas@gmail.com**]')


