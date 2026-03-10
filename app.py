import streamlit as st
from PIL import Image
from predict import predict

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Potato Disease Detection",
    page_icon="🥔",
    layout="centered",
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* Hide default Streamlit header & footer */
    header[data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .hero-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4ade80, #22d3ee, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Upload card */
    .upload-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(12px);
    }
    .upload-card h3 {
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .upload-card p {
        color: #64748b;
        font-size: 0.9rem;
    }

    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
    }
    [data-testid="stFileUploader"] label {
        color: #cbd5e1 !important;
    }
    [data-testid="stFileUploader"] section {
        border: 2px dashed rgba(74, 222, 128, 0.25) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        background: rgba(74, 222, 128, 0.03) !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"] section:hover {
        border-color: rgba(74, 222, 128, 0.5) !important;
        background: rgba(74, 222, 128, 0.06) !important;
    }

    /* Result card */
    .result-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(12px);
        animation: fadeIn 0.6s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Prediction badge */
    .prediction-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .prediction-value {
        font-size: 1.6rem;
        font-weight: 700;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        display: inline-block;
        margin-top: 0.3rem;
    }
    .prediction-healthy {
        background: rgba(74, 222, 128, 0.12);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.25);
    }
    .prediction-diseased {
        background: rgba(248, 113, 113, 0.12);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.25);
    }

    /* Info cards */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        margin-top: 1.2rem;
    }
    .info-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .info-item:hover {
        background: rgba(255,255,255,0.06);
        transform: translateY(-2px);
    }
    .info-item .icon {
        font-size: 1.8rem;
        margin-bottom: 0.4rem;
    }
    .info-item .label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    .info-item .value {
        color: #e2e8f0;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    /* Tips section */
    .tips-card {
        background: rgba(129, 140, 248, 0.06);
        border: 1px solid rgba(129, 140, 248, 0.15);
        border-radius: 12px;
        padding: 1.4rem;
        margin-top: 1rem;
    }
    .tips-card h4 {
        color: #a5b4fc;
        font-weight: 600;
        margin: 0 0 0.6rem;
        font-size: 0.95rem;
    }
    .tips-card ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    .tips-card li {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }

    /* Image styling */
    [data-testid="stImage"] {
        border-radius: 12px;
        overflow: hidden;
    }
    [data-testid="stImage"] img {
        border-radius: 12px;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 1.5rem 0;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        color: #475569;
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-icon"><h1 class="herox-title">Potato Disease Detection</h1></div>
    <p class="hero-subtitle">AI-powered leaf analysis to detect Early Blight, Late Blight & Healthy leaves</p>
</div>
""", unsafe_allow_html=True)

# ─── Info Cards ────────────────────────────────────────────────
st.markdown("""
<div class="info-grid">
    <div class="info-item">
        <div class="icon">🧠</div>
        <div class="label">Model</div>
        <div class="value">Custom CNN</div>
    </div>
    <div class="info-item">
        <div class="icon">🎯</div>
        <div class="label">Classes</div>
        <div class="value">3 Categories</div>
    </div>
    <div class="info-item">
        <div class="icon">⚡</div>
        <div class="label">Inference</div>
        <div class="value">Real-time</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─── Upload Section ────────────────────────────────────────────
st.markdown("""
<div class="upload-card">
    <h3>Upload Leaf Image</h3>
    <p>Drag and drop or browse to upload a potato leaf image for analysis</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

# ─── Prediction Section ───────────────────────────────────────
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.image(image, caption="Uploaded Leaf", use_container_width=True)

    with col2:
        with st.spinner("🔍 Analysing leaf..."):
            result = predict(image)

        is_healthy = "Healthy" in result
        display_name = result.replace("Potato___", "").replace("_", " ")
        badge_class = "prediction-healthy" if is_healthy else "prediction-diseased"
        status_icon = "✅" if is_healthy else "⚠️"

        st.markdown(f"""
        <div class="result-card">
            <div class="prediction-label">Diagnosis Result</div>
            <div class="prediction-value {badge_class}">
                {status_icon} {display_name}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Disease info
        disease_info = {
            "Potato___Early_Blight": {
                "desc": "Caused by **Alternaria solani**. Appears as dark brown, concentric-ring spots on older leaves.",
                "action": "Apply fungicides like chlorothalonil or mancozeb. Remove infected leaves promptly.",
            },
            "Potato___Late_Blight": {
                "desc": "Caused by **Phytophthora infestans**. Shows water-soaked, dark lesions that spread rapidly.",
                "action": "Use copper-based fungicides. Ensure good air circulation and avoid overhead irrigation.",
            },
            "Potato___Healthy": {
                "desc": "The leaf appears healthy with no visible signs of disease.",
                "action": "Continue regular care — proper watering, fertilization, and crop rotation.",
            },
        }

        info = disease_info.get(result, {})
        if info:
            st.markdown(f"""
            <div class="tips-card">
                <h4>📋 About This Condition</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(info["desc"])
            st.markdown(f"**💊 Recommended Action:** {info['action']}")

# ─── Tips (when no image uploaded) ─────────────────────────────
else:
    st.markdown("""
    <div class="tips-card">
        <h4>💡 Tips for Best Results</h4>
        <ul>
            <li>Use clear, well-lit images of individual leaves</li>
            <li>Avoid blurry or heavily shadowed photos</li>
            <li>Supported formats: JPG, JPEG, PNG</li>
            <li>Capture both upper and lower leaf surfaces for accuracy</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="app-footer">
    Built with Streamlit & PyTorch &nbsp;·&nbsp; Potato Disease Classification using Deep Learning
</div>
""", unsafe_allow_html=True)