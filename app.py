import os
import re
import io
import traceback
from typing import Optional, Dict
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

# Configure page with minimal, whimsical metadata
st.set_page_config(
    page_title="AI Wardrobe Stylist",
    page_icon=":material/checkroom:",
    layout="centered",
    initial_sidebar_state="auto",
)

def inject_whimsical_styles() -> None:
    """Injects custom CSS for a whimsical, anti-vibe-coded editorial aesthetic optimized for PC and iPad Safari."""
    st.markdown(
        """
        <style>
        /* Import Whimsical & Editorial Typography */
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        /* Root color tokens */
        :root {
            --bg-canvas: #FAF7F2;
            --bg-card: #FFFFFF;
            --bg-accent: #F3ECE1;
            --text-primary: #2C2623;
            --text-secondary: #6B625B;
            --text-muted: #8E847C;
            --terracotta: #D96B43;
            --terracotta-soft: #FDF5F0;
            --sage: #4E6851;
            --sage-soft: #EEF3EE;
            --border-soft: #E8E1D7;
            --border-warm: #DECFC0;
        }

        /* Typography overrides */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
            -webkit-font-smoothing: antialiased;
        }

        h1, h2, h3, .serif-heading {
            font-family: 'Fraunces', Georgia, serif !important;
            font-feature-settings: "liga" 1, "calt" 1;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        /* iPad Safari & Mobile touch smoothness */
        * {
            -webkit-tap-highlight-color: transparent;
        }

        button, input, select, textarea {
            touch-action: manipulation;
        }

        /* App Title & Subtitle Banner */
        .header-container {
            text-align: center;
            padding: 1.5rem 0.5rem 1.5rem 0.5rem;
            margin-bottom: 1.25rem;
            border-bottom: 1px dashed var(--border-warm);
        }
        .header-tagline {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 0.85rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--terracotta);
            margin-bottom: 0.35rem;
            display: inline-block;
            font-weight: 600;
        }
        .header-title {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 2.35rem;
            font-weight: 600;
            line-height: 1.15;
            color: var(--text-primary);
            margin: 0 0 0.5rem 0;
        }
        .header-desc {
            font-size: 1.0rem;
            line-height: 1.5;
            color: var(--text-secondary);
            max-width: 520px;
            margin: 0 auto;
        }

        /* API Key Banner */
        .api-key-banner {
            background-color: var(--terracotta-soft);
            border: 1px solid #EAC8BB;
            border-radius: 16px;
            padding: 1.1rem 1.25rem;
            margin-bottom: 1.5rem;
        }
        .api-key-title {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--terracotta);
            margin-bottom: 0.25rem;
        }
        .api-key-desc {
            font-size: 0.9rem;
            line-height: 1.45;
            color: var(--text-secondary);
        }
        .api-key-desc code {
            background: #FFFFFF;
            padding: 0.15rem 0.4rem;
            border-radius: 6px;
            font-size: 0.84rem;
            color: var(--terracotta);
            border: 1px solid #EAC8BB;
        }

        /* Section dividers */
        .step-label {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-top: 1.5rem;
            margin-bottom: 0.65rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .step-num {
            font-family: 'Fraunces', Georgia, serif;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background-color: var(--bg-accent);
            color: var(--terracotta);
            font-size: 0.85rem;
            font-weight: 700;
        }

        /* Selectors & Pills Customization */
        .selector-label {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.92rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-top: 0.75rem;
            margin-bottom: 0.4rem;
        }

        /* Force Streamlit pills to wrap naturally instead of clipping horizontally */
        div[data-testid="stPills"],
        div[data-testid="stPills"] > div,
        div[data-testid="stPills"] div[role="radiogroup"] {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 0.55rem !important;
            overflow-x: visible !important;
            width: 100% !important;
        }

        div[data-testid="stPills"] button {
            white-space: normal !important;
            word-break: normal !important;
            min-height: 40px !important;
            padding: 0.45rem 1.05rem !important;
            font-size: 0.92rem !important;
            border-radius: 20px !important;
            border: 1px solid var(--border-soft) !important;
            background-color: #FFFFFF !important;
            color: var(--text-primary) !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
            transition: all 0.15s ease !important;
        }

        div[data-testid="stPills"] button[aria-checked="true"] {
            background-color: var(--terracotta-soft) !important;
            border-color: var(--terracotta) !important;
            color: var(--terracotta) !important;
            font-weight: 600 !important;
        }

        /* Photo preview wrapper */
        .photo-preview-box {
            background-color: var(--bg-card);
            border: 1px solid var(--border-soft);
            border-radius: 20px;
            padding: 0.75rem;
            box-shadow: 0 4px 16px rgba(44, 38, 35, 0.04);
            margin-top: 0.75rem;
            margin-bottom: 1.25rem;
        }

        /* Stylist Outfit Cards Grid */
        .outfit-grid {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-top: 1.25rem;
            margin-bottom: 2rem;
        }

        .outfit-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-soft);
            border-radius: 18px;
            padding: 1.25rem 1.4rem;
            box-shadow: 0 4px 14px rgba(44, 38, 35, 0.03);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .outfit-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }

        .category-badge {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.25rem 0.65rem;
            border-radius: 30px;
            background-color: var(--bg-accent);
            color: var(--text-secondary);
        }

        .category-badge.top-badge {
            background-color: #F8EFE9;
            color: #C05832;
        }
        .category-badge.bottom-badge {
            background-color: #EBF0EC;
            color: #3F5E45;
        }
        .category-badge.layer-badge {
            background-color: #F5EEF7;
            color: #6C497B;
        }
        .category-badge.note-badge {
            background-color: #F8F5E9;
            color: #7B682E;
        }

        .outfit-card-title {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }

        .outfit-card-content {
            font-size: 0.96rem;
            line-height: 1.55;
            color: var(--text-primary);
            margin-top: 0.35rem;
        }

        /* Large primary button - touch target >= 48px */
        div.stButton > button {
            min-height: 52px !important;
            border-radius: 16px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            background-color: var(--terracotta) !important;
            border: 1px solid #C45B34 !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(217, 107, 67, 0.24) !important;
            transition: all 0.2s ease !important;
            margin-top: 1rem !important;
        }

        div.stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 16px rgba(217, 107, 67, 0.32) !important;
        }

        div.stButton > button:active {
            transform: translateY(1px) !important;
        }

        /* Footer notice */
        .footer-note {
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-soft);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def clean_text_encoding(text: Optional[str]) -> str:
    """Removes invisible unicode characters, zero-width spaces, and control characters."""
    if not text:
        return ""
    # Strip zero-width space (\u200b), zero-width joiner (\u200d), zero-width non-joiner (\u200c), BOM (\ufeff), etc.
    return re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', text).strip()

def get_gemini_api_key() -> Optional[str]:
    """Retrieves Gemini API key with priority: st.secrets -> os.environ -> st.session_state."""
    # 1. Check Streamlit Secrets (.streamlit/secrets.toml)
    try:
        if "GEMINI_API_KEY" in st.secrets:
            key = str(st.secrets["GEMINI_API_KEY"]).strip()
            if key and key != "your-google-gemini-api-key-here" and key != "":
                return clean_text_encoding(key)
    except Exception:
        pass

    # 2. Check Environment Variables
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return clean_text_encoding(env_key)

    # 3. Check Session State (entered via UI input or sidebar)
    if "gemini_api_key" in st.session_state and st.session_state["gemini_api_key"]:
        key = str(st.session_state["gemini_api_key"]).strip()
        if key:
            return clean_text_encoding(key)

    return None

def parse_styling_response(text: str) -> Dict[str, str]:
    """Parses Gemini's markdown response into structured outfit segments without relying on emojis."""
    cleaned_input = clean_text_encoding(text)
    parsed = {
        "top": "",
        "bottom": "",
        "layer": "",
        "advice": "",
        "raw": cleaned_input,
    }

    # Flexible pattern matching headers (e.g. ### Top, ### 👕 Top, ### ?? Top)
    top_match = re.search(r"###[^\w\n]*Top[:\s]*(.*?)(?=###|\Z)", cleaned_input, re.IGNORECASE | re.DOTALL)
    bottom_match = re.search(r"###[^\w\n]*Bottom[:\s]*(.*?)(?=###|\Z)", cleaned_input, re.IGNORECASE | re.DOTALL)
    layer_match = re.search(r"###[^\w\n]*(?:Layer\s*(?:/\s*Outerwear)?|Outerwear)[:\s]*(.*?)(?=###|\Z)", cleaned_input, re.IGNORECASE | re.DOTALL)
    advice_match = re.search(r"###[^\w\n]*(?:Stylist\s*Advice|Stylist\s*Note|Advice|Why\s*This\s*Works)[:\s]*(.*?)(?=###|\Z)", cleaned_input, re.IGNORECASE | re.DOTALL)

    if top_match:
        parsed["top"] = top_match.group(1).strip()
    if bottom_match:
        parsed["bottom"] = bottom_match.group(1).strip()
    if layer_match:
        parsed["layer"] = layer_match.group(1).strip()
    if advice_match:
        parsed["advice"] = advice_match.group(1).strip()

    return parsed

def render_single_card(title: str, badge_label: str, badge_class: str, content: str, is_advice: bool = False) -> None:
    """Renders an individual outfit card cleanly without markdown indentation issues."""
    if not content:
        return
    advice_style = ' style="border-left: 4px solid var(--terracotta);"' if is_advice else ''
    card_html = (
        f'<div class="outfit-card"{advice_style}>'
        f'<div class="outfit-card-header">'
        f'<h4 class="outfit-card-title">{title}</h4>'
        f'<span class="category-badge {badge_class}">{badge_label}</span>'
        f'</div>'
        f'<div class="outfit-card-content">{content}</div>'
        f'</div>'
    )
    if hasattr(st, "html"):
        st.html(card_html)
    else:
        st.markdown(card_html, unsafe_allow_html=True)

def render_outfit_cards(parsed: Dict[str, str]) -> None:
    """Renders the parsed outfit items into clean, whimsical cards with minimal emojis."""
    has_structured_parts = any([parsed["top"], parsed["bottom"], parsed["layer"], parsed["advice"]])

    if not has_structured_parts:
        fallback_html = (
            '<div class="outfit-card">'
            '<div class="category-badge note-badge">RECOMMENDED OUTFIT</div>'
            f'<div class="outfit-card-content" style="margin-top: 0.75rem;">{parsed["raw"]}</div>'
            '</div>'
        )
        if hasattr(st, "html"):
            st.html(fallback_html)
        else:
            st.markdown(fallback_html, unsafe_allow_html=True)
        return

    render_single_card("The Top", "Top", "top-badge", parsed["top"])
    render_single_card("The Bottom", "Bottom", "bottom-badge", parsed["bottom"])
    render_single_card("Outerwear & Layer", "Layer", "layer-badge", parsed["layer"])
    render_single_card("Stylist Note", "Stylist Note", "note-badge", parsed["advice"], is_advice=True)

def pil_to_clean_part(img: Image.Image) -> types.Part:
    """Converts a PIL image into a clean, metadata-free JPEG part to prevent ASCII encoding errors."""
    clean_img = Image.new("RGB", img.size, (255, 255, 255))
    clean_img.paste(img)

    # Scale down if very large to prevent memory and payload overflow
    max_dim = 1600
    if max(clean_img.size) > max_dim:
        clean_img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    clean_img.save(buf, format="JPEG", quality=85)
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")

def generate_outfit_suggestion(image: Image.Image, weather: str, occasion: str, api_key: str) -> str:
    """Invokes Gemini 2.5 Flash via google-genai SDK to select an outfit from visible garments."""
    clean_api_key = clean_text_encoding(api_key)
    client = genai.Client(api_key=clean_api_key)

    clean_weather = clean_text_encoding(weather)
    clean_occasion = clean_text_encoding(occasion)

    prompt = f"""You are a helpful, tasteful outfit stylist for a student.
Examine the clothes visible in this image carefully.
Recommend a single, complete matching outfit tailored for:
- Weather: {clean_weather}
- Occasion: {clean_occasion}

Strict instructions:
- Only recommend items that are clearly visible in the photo.
- For each piece, describe the item and pinpoint its physical location in the shot (for example: 'Oversized cream knit sweater folded near the center-left', 'Washed black denim jeans hanging on the right rail').
- Do not use emojis in your response. Keep the tone warm, confident, and direct.
- Structure your response using these exact section headers:

### Top
[Description and physical position in the photo]

### Bottom
[Description and physical position in the photo]

### Layer / Outerwear
[Description and physical position in the photo, or state 'None needed for this weather']

### Stylist Advice
[2-3 sentences explaining why these pieces and colors match the vibe, occasion, and weather]
"""

    image_part = pil_to_clean_part(image)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[image_part, prompt],
    )

    if not response or not response.text:
        raise ValueError("No response received from the Gemini model.")

    return clean_text_encoding(response.text)

def main():
    inject_whimsical_styles()
    api_key = get_gemini_api_key()

    # Sidebar settings & status
    with st.sidebar:
        st.markdown("### Settings & Keys")
        if api_key:
            st.success("API Key is configured")
            if st.button("Reset / Change Key", width="stretch"):
                st.session_state["gemini_api_key"] = ""
                st.rerun()
        else:
            sidebar_input = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="AIzaSy...",
                key="sidebar_key_field",
                help="Paste your Google Gemini API key here.",
            )
            if sidebar_input and sidebar_input.strip():
                st.session_state["gemini_api_key"] = clean_text_encoding(sidebar_input)
                st.rerun()

        st.caption(
            "Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)."
        )

    # App Header
    st.markdown(
        """
        <div class="header-container">
            <span class="header-tagline">Personal Wardrobe Assistant</span>
            <h1 class="header-title">AI Wardrobe Stylist</h1>
            <p class="header-desc">
                Snap your closet or laid-out clothes. Choose your day's weather and occasion, 
                and get an outfit picked directly from what you own.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # If no API key configured, show prominent setup banner directly on main screen
    if not api_key:
        with st.container():
            st.markdown(
                """
                <div class="api-key-banner">
                    <div class="api-key-title">Gemini API Key Required</div>
                    <div class="api-key-desc">
                        To generate outfit recommendations, please paste your Gemini API key below.<br>
                        <em>Tip for running locally:</em> You can also add <code>GEMINI_API_KEY = "your-key"</code> to <code>.streamlit/secrets.toml</code>.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            entered_key = st.text_input(
                "Paste Gemini API Key",
                type="password",
                placeholder="Paste key starting with AIzaSy...",
                key="main_api_key_field",
                help="Get a free key from https://aistudio.google.com/app/apikey",
            )
            if entered_key and entered_key.strip():
                st.session_state["gemini_api_key"] = clean_text_encoding(entered_key)
                st.rerun()

    # Step 1: Capture or Upload Wardrobe Photo
    st.markdown(
        """
        <div class="step-label">
            <span class="step-num">1</span>
            <span>Your Clothes</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cam_image = st.camera_input("Take a photo of your clothes")
    
    with st.expander("Or upload an image from your library", expanded=False):
        uploaded_image = st.file_uploader(
            "Select a photo",
            type=["jpg", "jpeg", "png"],
            help="Choose a clear shot of your wardrobe, bed, or floor layout.",
        )

    # Determine active photo source
    active_photo = cam_image if cam_image is not None else uploaded_image

    if active_photo is not None:
        try:
            pil_image = Image.open(active_photo).convert("RGB")
            st.image(
                pil_image,
                caption="Current wardrobe snapshot",
                width="stretch",
            )
        except Exception as e:
            st.error(f"Could not open image: {e}")
            pil_image = None
    else:
        pil_image = None

    # Step 2: Context Selection (Weather & Occasion)
    st.markdown(
        """
        <div class="step-label">
            <span class="step-num">2</span>
            <span>Weather & Occasion</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    weather_options = [
        "Sunny & Warm",
        "Mild & Breezy",
        "Chilly & Crisp",
        "Rainy & Overcast",
        "Cold & Freezing",
    ]

    occasion_options = [
        "Casual School Day",
        "Weekend Hangout",
        "Sports & PE",
        "Semi-Dressy",
        "Party & Celebration",
    ]

    # Weather selector (Full Width)
    st.markdown('<div class="selector-label">Weather Condition</div>', unsafe_allow_html=True)
    if hasattr(st, "pills"):
        selected_weather = st.pills(
            "Weather Condition",
            options=weather_options,
            default=weather_options[0],
            label_visibility="collapsed",
        )
    else:
        selected_weather = st.selectbox(
            "Weather Condition",
            options=weather_options,
            index=0,
            label_visibility="collapsed",
        )

    # Occasion selector (Full Width)
    st.markdown('<div class="selector-label" style="margin-top: 1rem;">Occasion / Style</div>', unsafe_allow_html=True)
    if hasattr(st, "pills"):
        selected_occasion = st.pills(
            "Occasion / Style",
            options=occasion_options,
            default=occasion_options[0],
            label_visibility="collapsed",
        )
    else:
        selected_occasion = st.selectbox(
            "Occasion / Style",
            options=occasion_options,
            index=0,
            label_visibility="collapsed",
        )

    st.write("")  # Spacing

    # Step 3: Action Trigger
    pick_outfit_btn = st.button("Pick My Outfit", type="primary", width="stretch")

    if pick_outfit_btn:
        if pil_image is None:
            st.warning("Please take a photo or upload an image of your clothes first.")
            return

        active_key = get_gemini_api_key()
        if not active_key:
            st.warning(
                "Gemini API Key not found. Please paste your key above or add it to .streamlit/secrets.toml."
            )
            return

        try:
            with st.spinner("Scanning your wardrobe and styling..."):
                raw_suggestion = generate_outfit_suggestion(
                    image=pil_image,
                    weather=selected_weather or "Sunny & Warm",
                    occasion=selected_occasion or "Casual School Day",
                    api_key=active_key,
                )

            # Store in session state for persistence across reruns
            st.session_state["latest_suggestion"] = raw_suggestion

        except Exception as err:
            traceback.print_exc()
            err_msg = str(err)
            if "API_KEY_INVALID" in err_msg or "invalid api key" in err_msg.lower():
                st.error("The provided Gemini API Key is invalid. Please verify the key and try again.")
            elif "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                st.error("Gemini API quota exceeded. Please try again shortly or check your project quota.")
            else:
                st.error(f"Styling request could not be completed: {err_msg}")

    # Render results if available in session state
    if "latest_suggestion" in st.session_state and st.session_state["latest_suggestion"]:
        st.markdown(
            """
            <div class="step-label" style="margin-top: 2rem;">
                <span class="step-num">3</span>
                <span>Your Curated Outfit</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        parsed_outfit = parse_styling_response(st.session_state["latest_suggestion"])
        render_outfit_cards(parsed_outfit)

        # Expandable raw details
        with st.expander("View Full Text Notes", expanded=False):
            st.text(st.session_state["latest_suggestion"])

    # Whimsical footer
    st.markdown(
        """
        <div class="footer-note">
            AI Wardrobe Stylist &bull; Crafted for iPad & Mobile Safari
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()

