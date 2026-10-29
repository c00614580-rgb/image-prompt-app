from PIL import Image
import streamlit as st

st.set_page_config(page_title="My Image Prompt App", page_icon="📸")

st.title("📸 Follower Image Prompt App")
st.write(
    "Upload your picture below! The custom Python prompt will process it"
    " instantly."
)

# File uploader for your followers
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  # Open and show the uploaded image
  image = Image.open(uploaded_file)
  st.image(image, caption="Uploaded Picture", use_column_width=True)

  # Button to trigger your prompt/logic
  if st.button("Run Prompt"):
    with st.spinner("Processing image..."):
      # --- YOUR PROMPT LOGIC GOES HERE ---
      # Example: Converting image to black & white
      processed_image = image.convert("L")

    st.success("Done!")
    st.image(
        processed_image, caption="Processed Result", use_column_width=True
    )
