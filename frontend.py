import streamlit as st
import requests
import json

# Backend API URL (Update with your deployed backend URL)
BACKEND_URL = "http://127.0.0.1:5000/bfhl"

# Set website title to roll number
st.set_page_config(page_title="ABCD123")

# App Title
st.title("Data Processor - BFHL API 22BCS11920")

# Input text area for JSON
st.subheader("Enter JSON Input")
user_input = st.text_area("Example: { \"data\": [\"A\", \"C\", \"z\"] }", height=150)

# Submit button
if st.button("Submit"):
    try:
        # Validate JSON format
        data = json.loads(user_input)

        # Ensure "data" key is present and is a list
        if "data" not in data or not isinstance(data["data"], list):
            st.error("Invalid JSON format! 'data' field must be a list.")
        else:
            st.info("Processing request...")
            
            # Send request to backend
            response = requests.post(BACKEND_URL, json=data)
            
            if response.status_code == 200:
                result = response.json()
                st.success("API Response Received!")
                
                # Store response in session state
                st.session_state["api_response"] = result
            else:
                st.error(f"API Error: {response.status_code}")
    except json.JSONDecodeError:
        st.error("Invalid JSON format! Please enter valid JSON.")

# Display API Response (only if available)
if "api_response" in st.session_state:
    response_data = st.session_state["api_response"]

    # Multi-Select Dropdown (only appears after API response is received)
    st.subheader("Select Data to Display")
    options = st.multiselect(
        "Choose categories:", 
        ["Alphabets", "Numbers", "Highest Alphabet"]
    )

    # Show response based on selection
    if "Alphabets" in options:
        st.write("**Alphabets:**", response_data.get("alphabets", []))
    if "Numbers" in options:
        st.write("**Numbers:**", response_data.get("numbers", []))
    if "Highest Alphabet" in options:
        st.write("**Highest Alphabet:**", response_data.get("highest_alphabet", []))

# Button to check GET request response
if st.button("Check Operation Code (GET Request)"):
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch operation code")