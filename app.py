import streamlit as st
from deep_translator import GoogleTranslator


st.set_page_config(
    page_title="Verba - Translation Studio",
    page_icon="V",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------------
# Visual system
# -----------------------------------------------------------------------------

st.html(
    """
    <style>
        :root {
            --navy: #06152b;
            --navy-soft: #0a2146;
            --blue: #2f6bff;
            --blue-bright: #59a5ff;
            --cyan: #a9edff;
            --ice: #eff5fb;
            --paper: #ffffff;
            --ink: #0b1728;
            --muted: #627087;
            --line: #dce5ef;
        }

        * {
            box-sizing: border-box;
        }

        html,
        body,
        [class*="css"] {
            font-family: Inter, "SF Pro Display", "Segoe UI", Arial, sans-serif;
        }

        body {
            color: var(--ink);
        }

        [data-testid="stAppViewContainer"] {
            min-height: 100vh;
            background:
                radial-gradient(circle at 78% 9%, rgba(64, 126, 255, 0.26), transparent 25%),
                linear-gradient(180deg, var(--navy) 0 570px, var(--ice) 570px 100%);
        }

        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            inset: 0 0 auto 0;
            height: 570px;
            pointer-events: none;
            opacity: 0.13;
            background-image:
                linear-gradient(rgba(255,255,255,.11) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,.11) 1px, transparent 1px);
            background-size: 64px 64px;
            mask-image: linear-gradient(to bottom, black, transparent 90%);
        }

        header[data-testid="stHeader"],
        #MainMenu,
        footer {
            display: none;
        }

        [data-testid="stAppViewContainer"] > .main {
            position: relative;
            z-index: 1;
        }

        .block-container {
            max-width: 1240px;
            padding: 24px 28px 64px;
        }

        /* Navigation */

        .site-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 54px;
            color: white !important;
        }

        .wordmark {
            display: flex;
            align-items: center;
            gap: 11px;
            font-size: 16px;
            font-weight: 800;
            letter-spacing: -0.3px;
        }

        .wordmark-symbol {
            position: relative;
            width: 31px;
            height: 31px;
            border: 1px solid rgba(255,255,255,.35);
            border-radius: 10px;
            background: linear-gradient(145deg, #54c9ff, #2854ff);
            box-shadow: 0 8px 24px rgba(42, 106, 255, .34);
        }

        .wordmark-symbol::before,
        .wordmark-symbol::after {
            content: "";
            position: absolute;
            border: 1.5px solid white;
            border-radius: 50%;
        }

        .wordmark-symbol::before {
            inset: 7px 5px;
            transform: rotate(37deg);
        }

        .wordmark-symbol::after {
            inset: 5px 8px;
            transform: rotate(-37deg);
        }

        .nav-meta {
            display: flex;
            align-items: center;
            gap: 22px;
            color: rgba(230, 240, 255, .72);
            font-size: 11px;
            font-weight: 650;
            letter-spacing: .5px;
        }

        .live-state {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border: 1px solid rgba(255,255,255,.14);
            border-radius: 999px;
            background: rgba(255,255,255,.06);
        }

        .live-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #72e8bb;
            box-shadow: 0 0 12px rgba(114, 232, 187, .8);
        }

        /* Hero */

        .hero-shell {
            display: grid;
            grid-template-columns: minmax(0, 1.08fr) minmax(360px, .92fr);
            align-items: center;
            min-height: 395px;
            padding: 36px 0 112px;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 20px;
            color: #9ec8ff;
            font-size: 10px;
            font-weight: 750;
            letter-spacing: 1.7px;
        }

        .hero-badge-line {
            width: 27px;
            height: 1px;
            background: #63a4ff;
        }

        .hero-title {
            max-width: 690px;
            margin: 0;
            color: white !important;
            font-size: clamp(54px, 5.2vw, 76px);
            line-height: .98;
            font-weight: 680;
            letter-spacing: -4.2px;
        }

        .hero-title em {
            color: #84b7ff !important;
            font-style: normal;
        }

        .hero-description {
            max-width: 570px;
            margin: 24px 0 0;
            color: rgba(221, 234, 253, .67);
            font-size: 15px;
            line-height: 1.7;
        }

        /* Original language-orbit artwork */

        .orbit-stage {
            position: relative;
            width: 390px;
            height: 280px;
            margin-left: auto;
        }

        .orbit-glow {
            position: absolute;
            inset: 25px 55px 5px;
            border-radius: 50%;
            background: rgba(38, 112, 255, .26);
            filter: blur(42px);
        }

        .language-core {
            position: absolute;
            top: 63px;
            left: 133px;
            width: 132px;
            height: 132px;
            border: 1px solid rgba(191, 232, 255, .45);
            border-radius: 50%;
            background:
                radial-gradient(circle at 34% 27%, #c7f6ff 0 5%, transparent 17%),
                radial-gradient(circle at 62% 65%, #2b63ff, transparent 47%),
                linear-gradient(145deg, #69d7ff, #2244d4 58%, #081a49);
            box-shadow:
                0 0 26px rgba(87, 185, 255, .55),
                0 0 75px rgba(42, 97, 255, .38),
                inset -16px -17px 32px rgba(4, 17, 61, .52),
                inset 12px 9px 20px rgba(186, 241, 255, .3);
            animation: coreFloat 5s ease-in-out infinite;
        }

        .language-core::before {
            content: "Aa";
            position: absolute;
            inset: 0;
            display: grid;
            place-items: center;
            color: rgba(255,255,255,.94);
            font-size: 36px;
            font-weight: 500;
            text-shadow: 0 4px 20px rgba(0,0,0,.2);
        }

        .orbit-ring {
            position: absolute;
            top: 49px;
            left: 75px;
            width: 250px;
            height: 158px;
            border: 1px solid rgba(131, 190, 255, .38);
            border-radius: 50%;
            transform: rotate(-14deg);
        }

        .orbit-ring.second {
            top: 43px;
            left: 118px;
            width: 164px;
            height: 196px;
            transform: rotate(55deg);
            border-color: rgba(143, 222, 255, .22);
        }

        .language-chip {
            position: absolute;
            min-width: 52px;
            padding: 9px 12px;
            border: 1px solid rgba(255,255,255,.18);
            border-radius: 14px;
            background: rgba(9, 31, 72, .68);
            box-shadow: 0 12px 35px rgba(0,0,0,.22);
            color: #eaf4ff;
            text-align: center;
            font-size: 10px;
            font-weight: 750;
            letter-spacing: .8px;
            backdrop-filter: blur(12px);
        }

        .chip-en { top: 17px; left: 57px; }
        .chip-ur { top: 38px; right: 34px; }
        .chip-es { bottom: 27px; left: 52px; }
        .chip-de { right: 43px; bottom: 15px; }

        @keyframes coreFloat {
            0%, 100% { transform: translateY(0) rotate(-2deg); }
            50% { transform: translateY(-9px) rotate(3deg); }
        }

        /* Translation studio */

        .st-key-translation_workspace {
            position: relative;
            z-index: 5;
            margin-top: -96px;
            padding: 0 28px !important;
            overflow: hidden;
            border: 1px solid rgba(14, 41, 77, .07) !important;
            border-radius: 28px !important;
            background: var(--paper);
            box-shadow:
                0 34px 80px rgba(20, 48, 83, .16),
                0 3px 8px rgba(20, 48, 83, .05);
        }

        .st-key-translation_workspace > div {
            padding: 0 !important;
        }

        .studio-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 24px 28px 21px;
            margin: 0 -28px;
            border-bottom: 1px solid var(--line);
        }

        .studio-eyebrow {
            margin-bottom: 5px;
            color: #52709a;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 1.6px;
        }

        .studio-title {
            color: var(--ink);
            font-size: 19px;
            font-weight: 720;
            letter-spacing: -.4px;
        }

        .engine-status {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 11px;
            border-radius: 999px;
            background: #edf8f3;
            color: #18704e;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: .6px;
        }

        .studio-content {
            height: 22px;
        }

        .language-row-label {
            margin-bottom: 10px;
            color: #8491a3;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 1.4px;
        }

        .stSelectbox label,
        .stTextArea label {
            color: #758399 !important;
            font-size: 9px !important;
            font-weight: 800 !important;
            letter-spacing: 1.3px !important;
            text-transform: uppercase;
        }

        div[data-baseweb="select"] > div {
            min-height: 50px;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: #f8fafc;
            box-shadow: none;
        }

        div[data-baseweb="select"] span {
            color: #17253a;
            font-size: 13px;
            font-weight: 650;
        }

        .st-key-swap_button {
            padding-top: 25px;
        }

        .st-key-swap_button button {
            width: 44px !important;
            min-height: 44px !important;
            padding: 0 !important;
            border: 1px solid var(--line) !important;
            border-radius: 13px !important;
            background: white !important;
            color: #386ddd !important;
            font-size: 18px !important;
            box-shadow: 0 5px 13px rgba(32, 69, 122, .07) !important;
        }

        .st-key-swap_button button:hover {
            border-color: #8bb1ff !important;
            transform: translateY(-1px);
        }

        div[data-testid="stTextArea"] textarea {
            min-height: 230px;
            padding: 18px;
            resize: none;
            border: 1px solid var(--line);
            border-radius: 17px;
            background: #fbfcfe;
            color: #142238;
            font-size: 15px;
            line-height: 1.65;
            box-shadow: none;
        }

        div[data-testid="stTextArea"] textarea:focus {
            border-color: #6a9aff;
            box-shadow: 0 0 0 3px rgba(47, 107, 255, .09);
        }

        div[data-testid="stTextArea"] textarea:disabled {
            background:
                linear-gradient(145deg, rgba(239, 247, 255, .88), rgba(248, 251, 255, .96));
            color: #10213a;
            -webkit-text-fill-color: #10213a;
            opacity: 1;
        }

        .stCaption {
            color: #8794a6 !important;
            font-size: 10px !important;
        }

        .studio-action-bar {
            margin-top: 2px;
            padding-top: 18px;
            border-top: 1px solid #edf1f5;
        }

        .st-key-translate_button button {
            width: 100%;
            min-height: 54px;
            border: 0 !important;
            border-radius: 15px !important;
            background: var(--navy) !important;
            color: white !important;
            font-size: 12px !important;
            font-weight: 760 !important;
            letter-spacing: .6px !important;
            box-shadow: 0 12px 25px rgba(6, 21, 43, .2) !important;
        }

        .st-key-translate_button button:hover {
            background: #153b79 !important;
            transform: translateY(-1px);
            box-shadow: 0 15px 29px rgba(18, 61, 123, .24) !important;
        }

        .result-meta {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            min-height: 54px;
            color: #66758a;
            font-size: 10px;
            font-weight: 650;
        }

        .result-meta strong {
            color: #2f6bff;
            font-weight: 800;
        }

        .output-tools {
            margin: 18px 0 0;
            padding-top: 18px;
            border-top: 1px solid #edf1f5;
        }

        div[data-testid="stCode"] {
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 14px;
        }

        div[data-testid="stCode"] pre {
            background: #f7f9fc;
        }

        .stDownloadButton button {
            width: 100%;
            min-height: 44px;
            border: 1px solid var(--line) !important;
            border-radius: 13px !important;
            background: white !important;
            color: #18304f !important;
            font-size: 10px !important;
            font-weight: 800 !important;
            letter-spacing: .5px !important;
        }

        .stDownloadButton button:hover {
            border-color: #78a4ff !important;
            color: #245dcc !important;
        }

        .studio-footer {
            display: flex;
            justify-content: space-between;
            margin-top: 22px;
            margin-left: -28px;
            margin-right: -28px;
            padding: 17px 28px;
            background: #f8fafc;
            border-top: 1px solid var(--line);
            color: #7a8799;
            font-size: 9px;
            font-weight: 750;
            letter-spacing: .8px;
        }

        /* Supporting feature strip */

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 24px;
        }

        .feature-card {
            padding: 21px;
            border: 1px solid #dce5ef;
            border-radius: 18px;
            background: rgba(255,255,255,.72);
        }

        .feature-index {
            margin-bottom: 20px;
            color: #3c72e8;
            font-size: 9px;
            font-weight: 850;
            letter-spacing: 1px;
        }

        .feature-value {
            color: #0d1d32;
            font-size: 19px;
            font-weight: 720;
            letter-spacing: -.5px;
        }

        .feature-copy {
            margin-top: 7px;
            color: #6f7d90;
            font-size: 11px;
            line-height: 1.5;
        }

        .page-footer {
            display: flex;
            justify-content: space-between;
            margin-top: 32px;
            padding-top: 19px;
            border-top: 1px solid #d8e2ec;
            color: #78879a;
            font-size: 9px;
            font-weight: 750;
            letter-spacing: .7px;
        }

        @media (max-width: 900px) {
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(180deg, var(--navy) 0 690px, var(--ice) 690px 100%);
            }

            .hero-shell {
                grid-template-columns: 1fr;
                padding: 46px 0 136px;
            }

            .hero-copy {
                text-align: center;
            }

            .hero-description {
                margin-left: auto;
                margin-right: auto;
            }

            .orbit-stage {
                display: none;
            }

            .st-key-translation_workspace {
                margin-top: -112px;
            }
        }

        @media (max-width: 640px) {
            .block-container {
                padding: 17px 14px 42px;
            }

            .nav-meta > span {
                display: none;
            }

            .hero-title {
                font-size: 48px;
                letter-spacing: -3px;
            }

            .studio-header,
            .studio-content {
                padding-left: 18px;
                padding-right: 18px;
            }

            .st-key-translation_workspace {
                padding-left: 18px !important;
                padding-right: 18px !important;
            }

            .studio-header,
            .studio-footer {
                margin-left: -18px;
                margin-right: -18px;
            }

            .studio-footer {
                padding-left: 18px;
                padding-right: 18px;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }

            .page-footer {
                gap: 16px;
                flex-direction: column;
            }
        }
    </style>
    """,
)


# -----------------------------------------------------------------------------
# Translation state and behavior
# -----------------------------------------------------------------------------


@st.cache_data
def load_languages():
    return GoogleTranslator().get_supported_languages(as_dict=True)


languages = load_languages()
language_names = sorted(languages.keys())
source_options = ["Auto Detect"] + language_names

if "source_language" not in st.session_state:
    st.session_state.source_language = "Auto Detect"

if "target_language" not in st.session_state:
    st.session_state.target_language = (
        "urdu" if "urdu" in language_names else language_names[0]
    )

if "source_text" not in st.session_state:
    st.session_state.source_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "translation_error" not in st.session_state:
    st.session_state.translation_error = ""


def swap_languages():
    source = st.session_state.source_language
    target = st.session_state.target_language

    if source == "Auto Detect":
        st.session_state.translation_error = (
            "Choose a source language before swapping."
        )
        return

    st.session_state.source_language = target
    st.session_state.target_language = source
    st.session_state.translation_error = ""


def translate_text():
    text = st.session_state.source_text.strip()
    source = st.session_state.source_language
    target = st.session_state.target_language
    st.session_state.translation_error = ""

    if not text:
        st.session_state.translation_error = "Enter some text to translate."
        return

    if source != "Auto Detect" and source == target:
        st.session_state.translation_error = (
            "Choose two different languages."
        )
        return

    source_code = "auto" if source == "Auto Detect" else languages[source]
    target_code = languages[target]

    try:
        st.session_state.translated_text = GoogleTranslator(
            source=source_code,
            target=target_code,
        ).translate(text)
    except Exception:
        st.session_state.translation_error = (
            "Translation could not be completed. Check your internet "
            "connection and try again."
        )


# -----------------------------------------------------------------------------
# Page
# -----------------------------------------------------------------------------

st.html(
    """
    <nav class="site-nav">
        <div class="wordmark">
            <span class="wordmark-symbol"></span>
            <span>VERBA</span>
        </div>
        <div class="nav-meta">
            <span>TRANSLATION STUDIO</span>
            <span class="live-state">
                <span class="live-dot"></span>
                ENGINE ONLINE
            </span>
        </div>
    </nav>

    <section class="hero-shell">
        <div class="hero-copy">
            <div class="hero-badge">
                <span class="hero-badge-line"></span>
                INTELLIGENT LANGUAGE ENGINE
            </div>
            <h1 class="hero-title">
                Meaning travels<br><em>better here.</em>
            </h1>
            <p class="hero-description">
                A focused workspace for translating ideas across languages
                with speed, clarity and none of the usual friction.
            </p>
        </div>

        <div class="orbit-stage" aria-hidden="true">
            <div class="orbit-glow"></div>
            <div class="orbit-ring"></div>
            <div class="orbit-ring second"></div>
            <div class="language-core"></div>
            <div class="language-chip chip-en">EN</div>
            <div class="language-chip chip-ur">UR</div>
            <div class="language-chip chip-es">ES</div>
            <div class="language-chip chip-de">DE</div>
        </div>
    </section>
    """,
)


with st.container(border=True, key="translation_workspace"):
    st.html(
        """
        <div class="studio-header">
            <div>
                <div class="studio-eyebrow">WORKSPACE / 01</div>
                <div class="studio-title">Translate your text</div>
            </div>
            <div class="engine-status">
                <span class="live-dot"></span>
                READY
            </div>
        </div>
        <div class="studio-content">
        """,
    )

    language_from, swap_column, language_to = st.columns(
        [1, 0.12, 1],
        gap="small",
    )

    with language_from:
        st.selectbox(
            "Translate from",
            source_options,
            format_func=lambda item: item.title(),
            key="source_language",
        )

    with swap_column:
        st.button("SWAP", key="swap_button",
            help="Swap languages",
            on_click=swap_languages,
        )

    with language_to:
        st.selectbox(
            "Translate to",
            language_names,
            format_func=lambda item: item.title(),
            key="target_language",
        )

    source_panel, output_panel = st.columns(2, gap="medium")

    with source_panel:
        st.text_area(
            "Original text",
            height=230,
            placeholder="Type or paste your text here...",
            key="source_text",
        )
        st.caption(f"{len(st.session_state.source_text)} characters")

    with output_panel:
        st.text_area(
            "Translation",
            value=st.session_state.translated_text,
            height=230,
            placeholder="Your translation will appear here.",
            disabled=True,
        )

        if st.session_state.translated_text:
            st.caption("Translation ready")
        else:
            st.caption("Waiting for input")

    action_column, meta_column = st.columns([1, 1], gap="medium")

    with action_column:
        st.button("Translate now ->", key="translate_button",
            use_container_width=True,
            on_click=translate_text,
        )

    with meta_column:
        st.html(
            """
            <div class="result-meta">
                <span><strong>130+</strong> supported languages</span>
            </div>
            """,
        )

    if st.session_state.translation_error:
        st.error(st.session_state.translation_error)

    if st.session_state.translated_text:
        st.html(
            '<div class="output-tools"></div>',
        )

        st.html(
            f"""
            <div style="
                margin-bottom: 10px;
                color: #758399;
                font-size: 9px;
                font-weight: 800;
                letter-spacing: 1.3px;
            ">
                COPY OR EXPORT RESULT
            </div>
            """,
        )

        copy_column, download_column = st.columns([1.35, 0.65], gap="medium")

        with copy_column:
            st.code(st.session_state.translated_text, language=None)

        with download_column:
            st.download_button(
                "DOWNLOAD .TXT",
                data=st.session_state.translated_text,
                file_name="translation.txt",
                mime="text/plain",
                use_container_width=True,
            )

    st.html(
        """
        </div>
        <div class="studio-footer">
            <span>SECURE SESSION</span>
            <span>POWERED BY PYTHON + STREAMLIT</span>
        </div>
        """,
    )


