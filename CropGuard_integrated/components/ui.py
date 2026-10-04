import streamlit as st


def inject_css():
    st.markdown("""
    <style>

    /* =========================================================
       GLOBAL
    ========================================================= */

    :root {
        --green: #1f6f4a;
        --green-dark: #155239;
        --green-light: #eaf5ef;

        --text: #18221d;
        --muted: #66736b;

        --line: #dce5df;
        --bg: #f5f8f5;
        --card: #ffffff;

        --red: #dc2626;
        --red-bg: #fee2e2;

        --yellow: #b45309;
        --yellow-bg: #fef3c7;

        --blue: #2563eb;
        --blue-bg: #dbeafe;

        --shadow: 0 2px 12px rgba(20, 50, 30, 0.06);
        --radius: 16px;
    }


    /* =========================================================
       APP BACKGROUND
    ========================================================= */

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .main {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .block-container {
        max-width: 1450px;
        padding: 2rem 2.5rem 4rem 2.5rem;
    }


    /* =========================================================
       SIDEBAR
    ========================================================= */

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1rem 1rem 2rem 1rem;
    }

    [data-testid="stSidebar"] p {
        color: var(--text);
    }


    /* =========================================================
       BRAND
    ========================================================= */

    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        margin: 0 0 24px 0;
        padding: 4px 2px;
    }

    .brand span {
        font-size: 30px;
        line-height: 1;
        flex-shrink: 0;
    }

    .brand b {
        display: block;
        font-size: 20px;
        line-height: 1.2;
        color: var(--green-dark);
    }

    .brand small {
        display: block;
        margin-top: 3px;
        color: var(--muted);
        font-size: 11px;
    }


    /* =========================================================
       TYPOGRAPHY
    ========================================================= */

    h1, h2, h3, h4 {
        color: var(--text) !important;
        line-height: 1.25 !important;
    }

    h1 {
        font-size: 2rem !important;
    }

    h2 {
        font-size: 1.45rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    p {
        line-height: 1.55;
    }

    .eyebrow {
        color: var(--muted);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }


    /* =========================================================
       GENERAL CARDS
    ========================================================= */

    .metric-card,
    .disease-card,
    .hero-disease,
    .zone-detail,
    .status-panel,
    .technical-card,
    .spray-card,
    .llm-card {

        background: var(--card);

        border: 1px solid var(--line);
        border-radius: var(--radius);

        padding: 20px;

        box-shadow: var(--shadow);

        width: 100%;
        box-sizing: border-box;

        overflow: visible;

        color: var(--text);
    }


    /* =========================================================
       METRIC CARDS
    ========================================================= */

    .metric-card {
        min-height: 145px;

        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .metric-card .label {
        color: var(--muted);
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .metric-card .value {
        color: var(--text);
        font-size: clamp(25px, 2.5vw, 34px);
        line-height: 1.15;
        font-weight: 800;
        margin: 4px 0 7px 0;

        word-break: break-word;
    }

    .metric-card .sub {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.4;
    }


    /* =========================================================
       DISEASE HERO
    ========================================================= */

    .hero-disease {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 24px;

        margin-bottom: 20px;
        min-height: 130px;
    }

    .hero-disease h1 {
        margin: 4px 0 8px 0;
        font-size: clamp(24px, 3vw, 34px) !important;
        overflow-wrap: anywhere;
    }

    .hero-disease p {
        color: var(--muted);
        margin: 0;
    }

    .hero-disease > div:last-child {
        flex-shrink: 0;
    }


    /* =========================================================
       GRIDS
    ========================================================= */

    .mini-grid,
    .detail-grid {
        display: grid;

        grid-template-columns: repeat(2, minmax(0, 1fr));

        gap: 12px;

        margin-top: 18px;

        width: 100%;
    }

    .mini-grid div,
    .detail-grid div {
        background: #f7faf7;

        border: 1px solid #edf2ee;

        border-radius: 10px;

        padding: 13px;

        min-width: 0;

        box-sizing: border-box;

        overflow-wrap: anywhere;
    }

    .mini-grid span,
    .detail-grid span {
        display: block;

        color: var(--muted);

        font-size: 11px;

        margin-bottom: 5px;
    }

    .mini-grid strong,
    .detail-grid strong {
        color: var(--text);

        font-size: 14px;

        line-height: 1.35;

        overflow-wrap: anywhere;
    }


    /* =========================================================
       STATUS
    ========================================================= */

    .status-panel {
        padding: 18px 20px;
    }

    .status-row,
    .tech-line {

        display: flex;

        justify-content: space-between;
        align-items: center;

        gap: 20px;

        padding: 13px 0;

        border-bottom: 1px solid var(--line);

        min-width: 0;
    }

    .status-row:last-child,
    .tech-line:last-child {
        border-bottom: 0;
    }

    .status-row > *,
    .tech-line > * {
        min-width: 0;
    }


    /* =========================================================
       LEGEND
    ========================================================= */

    .legend {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;

        margin: 10px 0;
    }

    .legend-item {
        display: flex;
        align-items: center;

        gap: 7px;

        font-size: 13px;

        color: var(--text);

        white-space: nowrap;
    }

    .dot {
        width: 10px;
        height: 10px;

        border-radius: 50%;

        display: inline-block;

        flex-shrink: 0;
    }

    .dot.low {
        background: #3b82f6;
    }

    .dot.medium {
        background: #eab308;
    }

    .dot.high {
        background: #ef4444;
    }


    /* =========================================================
       BADGES
    ========================================================= */

    .badge {

        display: inline-flex;

        align-items: center;
        justify-content: center;

        padding: 5px 10px;

        border-radius: 999px;

        font-size: 11px;

        font-weight: 800;

        line-height: 1.2;

        white-space: nowrap;

        flex-shrink: 0;
    }

    .high {
        background: var(--red-bg);
        color: #b91c1c;
    }

    .medium {
        background: var(--yellow-bg);
        color: #92400e;
    }

    .low {
        background: var(--blue-bg);
        color: #1d4ed8;
    }

    .connected {
        background: #dcfce7;
        color: #166534;
    }

    .inspecting {
        background: var(--blue-bg);
        color: #1d4ed8;
    }

    .locked {
        background: #dcfce7;
        color: #166534;
    }


    /* =========================================================
       LLM / AI CARDS
    ========================================================= */

    .llm-card {

        line-height: 1.6;

        overflow-wrap: anywhere;

        word-break: normal;
    }

    .llm-card.red {
        border-left: 5px solid #ef4444;
    }

    .llm-card.yellow {
        border-left: 5px solid #eab308;
    }

    .llm-card.green {
        border-left: 5px solid #22c55e;
    }

    .llm-card h4 {
        margin-top: 0;
        margin-bottom: 8px;
    }


    /* =========================================================
       STREAMLIT COLUMNS
       Prevent content from being squeezed/clipped
    ========================================================= */

    [data-testid="column"] {
        min-width: 0 !important;
    }

    [data-testid="stHorizontalBlock"] {
        width: 100%;
        gap: 1rem;
    }


    /* =========================================================
       BUTTONS
    ========================================================= */

    .stButton > button {

        width: 100%;

        min-height: 42px;

        border-radius: 10px;

        border: 1px solid var(--line);

        font-weight: 700;

        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: var(--green);
        color: var(--green-dark);
    }


    /* =========================================================
       INPUTS / SELECTBOX / FILE UPLOADER
    ========================================================= */

    [data-testid="stSelectbox"],
    [data-testid="stFileUploader"],
    [data-testid="stTextInput"],
    [data-testid="stNumberInput"] {
        width: 100%;
    }

    [data-testid="stFileUploader"] section {
        border-radius: 12px;
        border: 1px dashed #cbd8d0;
        background: #fbfdfb;
    }


    /* =========================================================
       DATAFRAMES / TABLES
    ========================================================= */

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
    }


    /* =========================================================
       IMAGES / VIDEO
    ========================================================= */

    img {
        max-width: 100%;
        height: auto;
        border-radius: 12px;
    }

    video {
        max-width: 100%;
        border-radius: 12px;
    }

    [data-testid="stImage"] img {
        object-fit: contain;
    }


    /* =========================================================
       MAPS
    ========================================================= */

    iframe {
        max-width: 100%;
        border-radius: 12px;
    }


    /* =========================================================
       DIVIDERS
    ========================================================= */

    hr {
        border: none;
        border-top: 1px solid var(--line);
        margin: 1.5rem 0;
    }


    /* =========================================================
       CAPTIONS
    ========================================================= */

    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
    }


    /* =========================================================
       MOBILE / SMALL SCREEN
    ========================================================= */

    @media (max-width: 900px) {

        .block-container {
            padding: 1.25rem 1rem 3rem 1rem;
        }

        .hero-disease {
            flex-direction: column;
            align-items: flex-start;
        }

        .hero-disease > div:last-child {
            align-self: flex-start;
        }

        .mini-grid,
        .detail-grid {
            grid-template-columns: 1fr;
        }

        .status-row,
        .tech-line {
            align-items: flex-start;
            flex-direction: column;
            gap: 7px;
        }
    }


    /* =========================================================
       VERY SMALL SCREEN
    ========================================================= */

    @media (max-width: 600px) {

        .block-container {
            padding: 1rem 0.75rem 2.5rem 0.75rem;
        }

        .metric-card,
        .disease-card,
        .hero-disease,
        .zone-detail,
        .status-panel,
        .technical-card,
        .spray-card,
        .llm-card {
            padding: 16px;
            border-radius: 13px;
        }

        .metric-card {
            min-height: 120px;
        }

        .metric-card .value {
            font-size: 27px;
        }

        .hero-disease h1 {
            font-size: 24px !important;
        }
    }


    /* =========================================================
       STREAMLIT EXPANDERS
    ========================================================= */

    [data-testid="stExpander"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        overflow: hidden;
        background: #fff;
    }


    /* =========================================================
       SCROLLBAR
    ========================================================= */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f5f2;
    }

    ::-webkit-scrollbar-thumb {
        background: #c5d1c9;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)


# =============================================================
# REUSABLE UI COMPONENTS
# =============================================================

def metric_card(title, value, sub=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{title}</div>
            <div class="value">{value}</div>
            <div class="sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(title, caption=""):
    st.markdown(
        f"""
        <div style="margin-bottom:8px;">
            <h3 style="margin-bottom:3px;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if caption:
        st.caption(caption)


def severity_badge(severity):

    severity = str(severity).strip().lower()

    # Normalize severity names
    if severity in ["severe", "critical"]:
        severity = "high"

    elif severity in ["moderate", "medium"]:
        severity = "medium"

    elif severity in ["mild", "low"]:
        severity = "low"

    label = severity.capitalize()

    return f'<span class="badge {severity}">{label}</span>'


def status_badge(status):

    status = str(status).strip()

    cls = {
        "Connected": "connected",
        "Inspecting": "inspecting",
        "Locked": "locked"
    }.get(status, "connected")

    return f'<span class="badge {cls}">● {status}</span>'