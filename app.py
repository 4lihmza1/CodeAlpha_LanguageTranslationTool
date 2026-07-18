import streamlit as st
from deep_translator import GoogleTranslator

# Page configuration
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="wide"
)

# Custom design
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #f4f7ff 0%, #eef2ff 100%);
        }

        .main-title {
            text-align: center;
            font-size: 48px;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 18px;
            margin-bottom: 30px;
        }

        .information-box {
            background-color: white;
            border: 1px solid #dbeafe;
            border-radius: 12px;
            padding: 16px;
            margin-top: 25px;
            color: #475569;
        }

        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 17px;
            font-weight: 700;
        }

        .stButton > button:hover {
            color: white;
            border: none;
            background: linear-gradient(90deg, #4338ca, #6d28d9);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load supported languages
@st.cache_data
def load_languages():
    return GoogleTranslator().get_supported_languages(as_dict=True)


languages = load_languages()
language_names = sorted(languages.keys())

# Application heading
st.markdown(
    '<div class="main-title">🌐 AI Language Translator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Translate text instantly between multiple languages</div>',
    unsafe_allow_html=True
)

# Initialize translated result
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# Language selectors
selector_col1, selector_col2 = st.columns(2)

with selector_col1:
    source_options = ["Auto Detect"] + language_names

    source_language = st.selectbox(
        "Source language",
        source_options,
        index=0,
        format_func=lambda language: language.title()
    )

with selector_col2:
    default_target = (
        language_names.index("urdu")
        if "urdu" in language_names
        else 0
    )

    target_language = st.selectbox(
        "Target language",
        language_names,
        index=default_target,
        format_func=lambda language: language.title()
    )

# Translation boxes
input_col, output_col = st.columns(2)

with input_col:
    st.subheader("Original text")

    original_text = st.text_area(
        "Enter the text you want to translate",
        height=220,
        placeholder="Type or paste your text here...",
        label_visibility="collapsed"
    )

    st.caption(f"{len(original_text)} characters")

with output_col:
    st.subheader("Translated text")

    st.text_area(
        "Translation result",
        value=st.session_state.translated_text,
        height=220,
        placeholder="Your translation will appear here...",
        disabled=True,
        label_visibility="collapsed"
    )

    if st.session_state.translated_text:
        st.caption("Use the download button below to save the translation.")

# Translate button
if st.button("✨ Translate Text", use_container_width=True):
    if not original_text.strip():
        st.warning("Please enter some text before translating.")

    elif (
        source_language != "Auto Detect"
        and source_language == target_language
    ):
        st.warning("Please select two different languages.")

    else:
        try:
            source_code = (
                "auto"
                if source_language == "Auto Detect"
                else languages[source_language]
            )

            target_code = languages[target_language]

            with st.spinner("Translating your text..."):
                translation = GoogleTranslator(
                    source=source_code,
                    target=target_code
                ).translate(original_text.strip())

            st.session_state.translated_text = translation
            st.rerun()

        except Exception as error:
            st.error(
                "Translation failed. Please check your internet connection "
                "and try again."
            )

# Copy-friendly and download options
if st.session_state.translated_text:
    st.subheader("Copy or download")

    st.code(st.session_state.translated_text, language=None)

    st.download_button(
        label="⬇️ Download Translation",
        data=st.session_state.translated_text,
        file_name="translation.txt",
        mime="text/plain",
        use_container_width=True
    )

# Project information
st.markdown(
    """
    <div class="information-box">
        <strong>About this project</strong><br>
        This language translation tool uses Python, Streamlit and
        Google Translator technology to translate text between multiple
        languages. It was developed as part of the CodeAlpha Artificial
        Intelligence Internship.
    </div>
    """,
    unsafe_allow_html=True
)