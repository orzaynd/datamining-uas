from recommendation import generate_recommendation
from who_module import (
    get_haz_table,
    calculate_haz_zscore,
    get_haz_status,

    get_waz_table,
    calculate_waz_zscore,
    get_waz_status,

    get_whz_table,
    calculate_whz_zscore,
    get_whz_status
)

import joblib
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Prediksi Stunting",
    page_icon="🌷",
    layout="wide"
)

# ---------------------------------------------------------------
# THEME: Pink & White — "Buku Kesehatan Anak" inspired
# ---------------------------------------------------------------
PRIMARY = "#e0457b"      # rose utama
PRIMARY_DARK = "#a31545" # rose tua (teks/aksen kuat)
PRIMARY_SOFT = "#ffe1ec" # pink pastel (background card)
ACCENT = "#ff8fab"       # pink terang (highlight, garis chart)
INK = "#5c2336"          # warna teks gelap keunguan
PAPER = "#fffaf9"        # putih hangat

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

    /* ===== FORCE LIGHT THEME (override dark mode) ===== */
    :root, [data-testid="stAppViewContainer"], .stApp {{
        color-scheme: light !important;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {INK} !important;
    }}

    .stApp {{
        background: linear-gradient(180deg, {PAPER} 0%, #fff 35%) !important;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}

    /* ===== ALL TEXT DEFAULT TO INK (overrides dark-mode auto white) ===== */
    p, span, div, label, li {{
        color: {INK};
    }}

    /* ===== WIDGET LABELS (Jenis Kelamin, Usia, dst) ===== */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] {{
        color: {PRIMARY_DARK} !important;
        font-weight: 600 !important;
    }}

    /* ===== MARKDOWN TEXT BLOCKS ===== */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] {{
        color: {INK} !important;
    }}

    /* ===== HERO HEADER ===== */
    .hero {{
        background: linear-gradient(120deg, {PRIMARY} 0%, {ACCENT} 100%);
        border-radius: 24px;
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 12px 30px rgba(224, 69, 123, 0.25);
        position: relative;
        overflow: hidden;
    }}
    .hero::after {{
        content: "";
        position: absolute;
        right: -60px;
        top: -60px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: rgba(255,255,255,0.12);
    }}
    .hero-eyebrow {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.8rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }}
    .hero-title {{
        font-family: 'Fraunces', serif;
        color: white !important;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.15;
    }}
    .hero-sub {{
        color: rgba(255,255,255,0.92) !important;
        font-size: 1rem;
        margin-top: 0.5rem;
        max-width: 640px;
    }}

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4 {{
        font-family: 'Fraunces', serif;
        color: {PRIMARY_DARK} !important;
        font-weight: 700;
    }}

    /* ===== BUTTON ===== */
    .stButton > button {{
        background: linear-gradient(120deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
        color: white !important;
        border: none;
        border-radius: 999px;
        padding: 0.7em 2.2em;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.02em;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 6px 16px rgba(163, 21, 69, 0.3);
    }}
    .stButton > button p {{ color: white !important; }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(163, 21, 69, 0.4);
    }}

    /* ===== INPUT FIELDS (text/number input boxes) ===== */
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input {{
        background-color: white !important;
        color: {INK} !important;
        border: 1.5px solid {PRIMARY_SOFT} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stNumberInput"] button {{
        background-color: {PRIMARY_SOFT} !important;
        color: {PRIMARY_DARK} !important;
    }}

    /* ===== SELECTBOX ===== */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: white !important;
        color: {INK} !important;
        border: 1.5px solid {PRIMARY_SOFT} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stSelectbox"] svg {{
        fill: {PRIMARY_DARK} !important;
    }}
    /* Dropdown menu list */
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background-color: white !important;
    }}
    li[role="option"] {{
        color: {INK} !important;
        background-color: white !important;
    }}
    li[role="option"]:hover {{
        background-color: {PRIMARY_SOFT} !important;
    }}

    /* ===== ALERTS / INFO BOXES ===== */
    div[data-testid="stAlertContainer"] {{
        background-color: {PRIMARY_SOFT} !important;
        border: none !important;
        border-left: 5px solid {PRIMARY} !important;
        border-radius: 14px;
    }}
    .stAlert p, [data-testid="stAlertContainer"] p {{ color: {PRIMARY_DARK} !important; font-weight: 500; }}

    /* ===== METRIC CARDS ===== */
    div[data-testid="stMetric"] {{
        background: white !important;
        border: 1px solid {PRIMARY_SOFT};
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 4px 14px rgba(224, 69, 123, 0.1);
    }}
    div[data-testid="stMetricLabel"] {{ color: {PRIMARY} !important; font-weight: 600; }}
    div[data-testid="stMetricValue"] {{ color: {PRIMARY_DARK} !important; font-weight: 700; }}

    /* ===== PROGRESS BAR ===== */
    div[data-testid="stProgress"] > div > div {{
        background: linear-gradient(90deg, {ACCENT}, {PRIMARY});
        border-radius: 999px;
    }}

    /* ===== DIVIDER ===== */
    hr {{ border-top: 2px dashed {PRIMARY_SOFT}; }}

    /* ===== CAPTION ===== */
    .stCaption, small, [data-testid="stCaptionContainer"] p {{ color: #b06079 !important; }}

    /* ===== SECTION LABEL (eyebrow style) ===== */
    .section-eyebrow {{
        color: {PRIMARY} !important;
        font-size: 0.78rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: -0.4rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {PRIMARY_SOFT} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

model = joblib.load("model/model_stunting_new.pkl")

# ---------------------------------------------------------------
# HERO HEADER
# ---------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-eyebrow">🌷 Tumbuh Kembang Balita</div>
        <div class="hero-title">Prediksi Stunting Balita</div>
        <div class="hero-sub">
            Deteksi dini risiko stunting menggunakan Machine Learning (Random Forest)
            yang dipadukan dengan Standar Antropometri WHO Child Growth 2026 — TB/U, BB/U, dan BB/TB.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="section-eyebrow">Langkah 1</div>', unsafe_allow_html=True)
st.markdown("### 📝 Data Anak")

gender = st.selectbox(
    "Jenis Kelamin",
    ["Laki - Laki", "Perempuan"]
)

age = st.number_input(
    "Usia (Bulan)",
    min_value=0,
    max_value=60,
    value=24
)

weight = st.number_input(
    "Berat Badan (kg)",
    min_value=0.0,
    value=10.0
)

height = st.number_input(
    "Tinggi Badan (cm)",
    min_value=0.0,
    value=80.0
)

if st.button("✨ Prediksi Sekarang"):

    # FIX: pilihan selectbox adalah "Laki - Laki" / "Perempuan",
    # bukan "Male", jadi pengecekan sebelumnya tidak pernah bernilai True.
    gender_encoded = 1 if gender == "Laki - Laki" else 0

    prediction = model.predict(
        [[gender_encoded, age, weight, height]]
    )[0]

    probability = model.predict_proba(
        [[gender_encoded, age, weight, height]]
    )[0]

    confidence = round(max(probability) * 100, 2)

    status = "Stunted" if prediction == 1 else "Not Stunted"

    haz_table = get_haz_table(
        gender,
        age
    )

    haz_zscore = calculate_haz_zscore(
        age_month=age,
        height_cm=height,
        haz_table=haz_table
    )

    haz_status = get_haz_status(
        age_month=age,
        height_cm=height,
        haz_table=haz_table
    )

    waz_table = get_waz_table(
        gender
    )

    waz_zscore = calculate_waz_zscore(
        age_month=age,
        weight_kg=weight,
        waz_table=waz_table
    )

    waz_status = get_waz_status(
        waz_zscore
    )

    whz_table = get_whz_table(
        gender
    )

    whz_zscore = calculate_whz_zscore(
        height_cm=height,
        weight_kg=weight,
        whz_table=whz_table
    )

    whz_status = get_whz_status(
        whz_zscore
    )

    recommendations = generate_recommendation(
        ai_status=status,
        haz_status=haz_status,
        waz_status=waz_status,
        whz_status=whz_status
    )

    st.divider()
    st.markdown('<div class="section-eyebrow">Langkah 2</div>', unsafe_allow_html=True)
    st.markdown("### 🔮 Hasil Prediksi AI")

    is_stunted = (status == "Stunted")
    status_color = PRIMARY_DARK if is_stunted else "#2e9e6b"
    status_bg = "#fff0f4" if is_stunted else "#eafaf1"
    status_emoji = "⚠️" if is_stunted else "✅"
    status_label = "Stunted" if is_stunted else "Tidak Stunting"

    col_status, col_gauge = st.columns([1, 1.2])

    with col_status:
        st.markdown(
            f"""
            <div style="background:{status_bg}; border-radius:18px; padding:1.8rem;
                        border:1px solid {PRIMARY_SOFT}; height: 100%;">
                <div style="font-size:0.8rem; letter-spacing:0.12em; text-transform:uppercase;
                            color:{status_color}; font-weight:700; opacity:0.8;">Status Prediksi</div>
                <div style="font-size:2.1rem; font-weight:700; color:{status_color}; margin-top:0.3rem;">
                    {status_emoji} {status_label}
                </div>
                <div style="margin-top:0.8rem; color:{INK}; font-size:0.95rem;">
                    Berdasarkan data usia <b>{age} bulan</b>, berat <b>{weight} kg</b>,
                    dan tinggi <b>{height} cm</b>, model memprediksi anak
                    <b>{status_label.lower()}</b> dengan tingkat kepercayaan
                    <b>{confidence}%</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_gauge:
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={"suffix": "%", "font": {"size": 40, "color": PRIMARY_DARK}},
            title={"text": "Tingkat Kepercayaan Model", "font": {"size": 14, "color": INK}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": PRIMARY_DARK},
                "bar": {"color": PRIMARY},
                "bgcolor": "white",
                "borderwidth": 1,
                "bordercolor": PRIMARY_SOFT,
                "steps": [
                    {"range": [0, 50], "color": "#ffe1ec"},
                    {"range": [50, 80], "color": "#ffc2d9"},
                    {"range": [80, 100], "color": "#ff8fab"},
                ],
            }
        ))
        gauge_fig.update_layout(
            height=240,
            margin=dict(l=20, r=20, t=50, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"family": "Inter"}
        )
        st.plotly_chart(gauge_fig, use_container_width=True)

    # ---------------------------------------------------------------
    # CHART: Z-Score Comparison (bar chart)
    # ---------------------------------------------------------------
    st.markdown("### 📈 Perbandingan Z-Score WHO")
    st.caption("Rentang normal WHO berada di antara garis putus-putus (-2 SD hingga +2 SD)")

    zscore_labels = ["TB/U (HAZ)", "BB/U (WAZ)", "BB/TB (WHZ)"]
    zscore_values = [haz_zscore, waz_zscore, whz_zscore]
    bar_colors = [
        PRIMARY_DARK if (v < -2 or v > 3) else ACCENT
        for v in zscore_values
    ]

    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(
        x=zscore_labels,
        y=zscore_values,
        marker_color=bar_colors,
        marker_line_color=PRIMARY_DARK,
        marker_line_width=1,
        text=[f"{v:.2f}" for v in zscore_values],
        textposition="outside",
        width=0.5
    ))
    bar_fig.add_hline(y=2, line_dash="dash", line_color="#c97aa0", annotation_text="+2 SD")
    bar_fig.add_hline(y=-2, line_dash="dash", line_color="#c97aa0", annotation_text="-2 SD")
    bar_fig.add_hline(y=0, line_color="#e8c5d4", line_width=1)

    bar_fig.update_layout(
        height=380,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": INK},
        yaxis_title="Z-Score (SD)",
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    # ---------------------------------------------------------------
    # METRIC CARDS
    # ---------------------------------------------------------------
    st.markdown("### 📐 Indikator WHO")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Z-Score TB/U", value=f"{haz_zscore:.2f}")
        st.info(f"**TB menurut Umur**\n\n{haz_status}")

    with col2:
        st.metric(label="Z-Score BB/U", value=f"{waz_zscore:.2f}")
        st.info(f"**BB menurut Umur**\n\n{waz_status}")

    with col3:
        st.metric(label="Z-Score BB/TB", value=f"{whz_zscore:.2f}")
        st.info(f"**BB menurut TB**\n\n{whz_status}")

    # ---------------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------------
    st.markdown("### 💡 Rekomendasi")

    rec_html = "".join(
        f"""
        <div style="background:white; border:1px solid {PRIMARY_SOFT}; border-left:4px solid {PRIMARY};
                    border-radius:10px; padding:0.7rem 1rem; margin-bottom:0.6rem;
                    color:{INK}; font-size:0.95rem;">
            🌸 {item}
        </div>
        """
        for item in recommendations
    )
    st.markdown(rec_html, unsafe_allow_html=True)

    st.divider()
    st.caption("Referensi: WHO Child Growth Standards 2026")