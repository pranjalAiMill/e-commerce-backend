import sys
import os
import streamlit as st
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from app.config import SUPPORTED_LANGUAGES


# ---------------------------------
# Streamlit configuration
# ---------------------------------
st.set_page_config(
    page_title="Image-to-Text Autogeneration",
    layout="wide"
)

st.title("Image-to-Text Autogeneration")
st.caption("Structured ecommerce content — GPT-4o or MiniCPM-V backend")


# ---------------------------------
# Backend selector (still stored for FastAPI backend use)
# ---------------------------------
backend = st.radio(
    "Select Vision Backend",
    ["GPT-4o (Cloud API)", "MiniCPM-V 2.6 (Local Lightweight)"],
    horizontal=True
)

# Expose backend selection to FastAPI via env flag (optional)
os.environ["VISION_BACKEND"] = "gpt4o" if "GPT" in backend else "minicpm"


# ---------------------------------
# Language selector
# ---------------------------------
language = st.selectbox(
    "Output language",
    list(SUPPORTED_LANGUAGES.keys())
)


# ---------------------------------
# File upload
# ---------------------------------
uploaded = st.file_uploader(
    "Upload product image",
    type=["png", "jpg", "jpeg"]
)


# ---------------------------------
# MAIN FLOW
# ---------------------------------
if uploaded:

    os.makedirs("temp", exist_ok=True)
    img_path = f"temp/{uploaded.name}"

    with open(img_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.image(img_path, width=350, caption="Uploaded image")


    if st.button("Generate Content"):
        with st.spinner(f"Processing image via {backend}…"):

            # ---------------------------------
            # CALL FASTAPI BACKEND INSTEAD OF LOCAL FUNCTION
            # ---------------------------------
            BACKEND_URL = "http://localhost:8010/generate-description"

            files = {"image": open(img_path, "rb")}
            data = {"language": SUPPORTED_LANGUAGES[language]}

            try:
                response = requests.post(
                    BACKEND_URL,
                    files=files,
                    data=data,
                    timeout=300
                )
            except Exception as e:
                st.error(f"Backend connection failed: {e}")
                st.stop()

            if response.status_code != 200:
                st.error(f"Backend error: {response.text}")
                st.stop()

            result = response.json()

        # ---------------------------------
        # PRESENTABLE SECTION OUTPUT
        # ---------------------------------
        st.success("Content generated successfully")

        # Title
        st.header(result.get("title", "Title not generated"))

        # Short description
        st.subheader("Short Description")
        st.write(result.get("short_description", ""))

        # Long description
        st.subheader("Long Description")
        st.write(result.get("long_description", ""))

        # Bullet points
        bullets = result.get("bullet_points", [])
        if bullets:
            st.subheader("Key Features")
            for b in bullets:
                st.markdown(f"- {b}")

        # Attributes table
        attrs = result.get("attributes", {})
        if attrs:
            st.subheader("Attributes")
            st.table(
                {
                    "Attribute": list(attrs.keys()),
                    "Value": list(attrs.values())
                }
            )

        # Raw JSON (debug option)
        with st.expander("View raw JSON output"):
            st.json(result)
