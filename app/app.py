import streamlit as st
from PIL import Image
import io

# Try to import rembg, fallback if not available
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    st.warning("⚠️ Background removal not available. "
               "Install rembg with Python ≤3.12 for full functionality.")

st.set_page_config(page_title="Ingredient Selector", layout="centered")
st.title("📸 Ingredient Selector")

image_file = st.camera_input("Take a picture of your ingredients")

if image_file:
    image = Image.open(image_file).convert("RGBA")
    st.image(image, caption="Original image", use_container_width=True)
    
    # Background removal option if available
    if REMBG_AVAILABLE and st.button("Remove Background"):
        with st.spinner("Removing background..."):
            # Convert to bytes for rembg processing
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Remove background
            output = remove(img_bytes.read())
            processed_image = Image.open(io.BytesIO(output))
            
            st.image(processed_image, caption="Background removed",
                     use_container_width=True)
