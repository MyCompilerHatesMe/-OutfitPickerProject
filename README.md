# AI Wardrobe Stylist

A clean, whimsical, responsive wardrobe styling web app built with Python and Streamlit, powered by the Google Gemini API (`gemini-3.8-flash`). Designed specifically for deployment on Streamlit Community Cloud and seamless touch usage on iPad Safari.

---

## Features

- **Dual Image Capture**: Snap clothes directly via iPad Safari camera or upload existing wardrobe pictures from your photo library.
- **Visual Spatial Localization**: Gemini examines the items in the photo and pinpoints where each recommended item is physically located (e.g., *'Oversized cream knit sweater folded near the center-left'*).
- **Context-Aware Styling**: Outfits are tailored based on current weather (Sunny, Chilly, Rainy, etc.) and occasion (Casual School Day, Sports & PE, Hangout, etc.).
- **Whimsical & Anti-Vibe-Coded Aesthetics**: Designed with soft serif typography (*Fraunces*), clean tactile touch targets (>= 50px), warm linen color tokens, and minimal emojis.
- **Robust API Key Management**: Supports Streamlit Secrets (`st.secrets["GEMINI_API_KEY"]`), environment variables (`GEMINI_API_KEY`), and an in-app fallback input in the sidebar for quick testing.

---

## Project Structure

```text
.
|-- app.py                         # Main Streamlit application
|-- requirements.txt               # Dependencies (streamlit, google-genai, pillow)
|-- .streamlit/
|   |-- config.toml                # Custom Streamlit theme configuration
|   +-- secrets.toml.example       # Example secrets configuration
|-- .gitignore                     # Git ignore rules for secrets and venv
+-- README.md                      # Documentation & deployment guide
```

---

## Local Setup

1. **Clone or navigate to the repository**:
   ```bash
   cd OutfitProject
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key (Optional)**:
   Create `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-google-gemini-api-key"
   ```
   *(Or enter your key directly in the web interface when running the app)*

4. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

---

## Deploying to Streamlit Community Cloud

1. Push your code to a GitHub repository (`app.py`, `requirements.txt`, `.streamlit/config.toml`, `.gitignore`, `README.md`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New App**.
3. Select your repository, branch, and set the main file path to `app.py`.
4. Under **Advanced Settings** -> **Secrets**, paste your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```
5. Click **Deploy!**

---

## iPad Safari Tips

- **Add to Home Screen**: Open the deployed URL in Safari on your iPad, tap the **Share** button, and select **Add to Home Screen** for a full-screen, native-app feel.
- **Camera Permissions**: When prompted, allow camera access so *Take a photo of your clothes* can use your iPad's back or front camera directly.