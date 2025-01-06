import streamlit as st
from PIL import Image

# Set gradient background
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
    </style>
    """,
    unsafe_allow_html=True
)

# Correct image path with raw string
image_path = r"./logo.jpg"  # Update the path if necessary

# Try opening the image and handle errors
try:
    logo = Image.open(image_path)

    # If the image has a background (e.g., white background), make it transparent (optional)
    logo = logo.convert("RGBA")
    data = logo.getdata()

    new_data = []
    for item in data:
        # Change all white (also shades of whites) pixels to transparent
        if item[0] in list(range(200, 256)) and item[1] in list(range(200, 256)) and item[2] in list(range(200, 256)):
            new_data.append((255, 255, 255, 0))  # Transparent background
        else:
            new_data.append(item)

    logo.putdata(new_data)

    # Header and subheading with logo
    col1, col2 = st.columns([1, 4])

    with col1:
        st.image(logo, width=150)  # Decreased logo size to 150
        st.markdown("<div style='text-align: left; margin-left: -30px;'> </div>", unsafe_allow_html=True)  # Adjust logo position to the left

    with col2:
        st.markdown('<div class="header">Smart Defence for Your Funds</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheading">Why Choose Us?</div>', unsafe_allow_html=True)

    # Create two columns: Left for "About Our App" and Right for "Login"
    left_col, right_col = st.columns(2)

    # Left column: About Our App
    with left_col:
        st.markdown("### About Our App")
        st.write(
            "Many credit cards are lost, stolen, or expired. But these cards can still be used by others. "
            "This app provides AI-powered immediate detection and prevention of fraudulent transactions, ensuring precision with minimal false positives."
        )

    # Right column: Login
    with right_col:
        st.markdown("### Login")
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        st.button("Login")

except Exception as e:
    st.error(f"Error loading the image: {e}")

