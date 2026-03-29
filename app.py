import streamlit as st
from groq import Groq
import os
import time
import base64
import json
import io
import urllib.parse
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# 🔐 Load API Key
# ─────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ API Key not found. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# ─────────────────────────────────────────────
# 🎨 Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MediCare AI — Your Health Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# 💅 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@600&display=swap');

* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

.stApp { background: #0a0e1a; color: #e2e8f0; }

section[data-testid="stSidebar"] {
    background: #0d1220;
    border-right: 1px solid #1e2840;
}

/* NAV PILLS */
div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
div[data-testid="stRadio"] label {
    background: transparent;
    border: 1px solid #1e2840;
    border-radius: 10px;
    padding: 10px 14px !important;
    cursor: pointer;
    transition: all 0.2s;
    color: #94a3b8 !important;
    font-size: 14px !important;
}
div[data-testid="stRadio"] label:hover {
    background: #1a2235;
    border-color: #3b82f6;
    color: #e2e8f0 !important;
}

/* CARDS */
.card {
    background: linear-gradient(135deg, #111827, #0f172a);
    border: 1px solid #1e2840;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.card:hover { border-color: #3b82f6; }

.stat-card {
    background: linear-gradient(135deg, #1e2840, #162032);
    border: 1px solid #2d3f5e;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

/* CHAT BUBBLES */
.user-wrap { display: flex; justify-content: flex-end; margin: 10px 0; }
.bot-wrap  { display: flex; justify-content: flex-start; margin: 10px 0; }

.user-bubble {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 12px 18px;
    border-radius: 20px 20px 4px 20px;
    max-width: 72%;
    font-size: 14.5px;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(37,99,235,0.25);
}
.bot-bubble {
    background: linear-gradient(135deg, #1a2235, #141c2e);
    color: #e2e8f0;
    padding: 12px 18px;
    border-radius: 20px 20px 20px 4px;
    max-width: 72%;
    font-size: 14.5px;
    line-height: 1.6;
    border: 1px solid #2d3f5e;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

/* BADGES */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-blue  { background: #1e3a5f; color: #60a5fa; border: 1px solid #2563eb; }
.badge-green { background: #14532d; color: #4ade80; border: 1px solid #16a34a; }
.badge-red   { background: #450a0a; color: #f87171; border: 1px solid #dc2626; }
.badge-orange{ background: #431407; color: #fb923c; border: 1px solid #ea580c; }

/* DISCLAIMER */
.disclaimer {
    background: linear-gradient(135deg, #1c1408, #1a1000);
    border: 1px solid #854d0e;
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 14px 18px;
    color: #fcd34d;
    font-size: 13px;
    margin: 16px 0;
}

/* REMINDER ITEM */
.reminder-item {
    background: #111827;
    border: 1px solid #1e2840;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* SECTION HEADER */
.section-header {
    font-size: 22px;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 4px;
}
.section-sub {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 24px;
}

/* RESULT BOX */
.result-box {
    background: #0f172a;
    border: 1px solid #1e2840;
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
    white-space: pre-wrap;
    font-size: 14.5px;
    line-height: 1.8;
    color: #cbd5e1;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(37,99,235,0.4) !important;
}

/* INPUTS */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #111827 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e2840 !important;
    border-radius: 10px !important;
}
.stChatInput textarea {
    background: #111827 !important;
    color: #e2e8f0 !important;
    border: 1px solid #2d3f5e !important;
    border-radius: 12px !important;
}

/* FILE UPLOADER */
.stFileUploader {
    background: #111827 !important;
    border: 2px dashed #2d3f5e !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* SIDEBAR LOGO */
.sidebar-logo {
    text-align: center;
    padding: 20px 0 10px 0;
}
.sidebar-logo .icon { font-size: 40px; }
.sidebar-logo .title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 600;
    color: #f1f5f9;
    margin-top: 6px;
}
.sidebar-logo .sub { font-size: 11px; color: #475569; margin-top: 2px; }

/* HIDE STREAMLIT BRANDING */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🧠 AI MODELS
# ─────────────────────────────────────────────
TEXT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ─────────────────────────────────────────────
# 🧠 SYSTEM PROMPTS
# ─────────────────────────────────────────────
CHAT_SYSTEM = """You are MediCare AI, a knowledgeable, empathetic medical assistant. You:
- Explain health topics in clear, simple language a normal person can understand
- Give practical, actionable advice for common health concerns
- Always mention when someone should see a doctor urgently
- Are warm, supportive, and never alarmist
- End serious symptom discussions with a reminder to consult a healthcare provider
- Never diagnose or prescribe — only educate and guide"""

PRESCRIPTION_SYSTEM = """You are an expert at reading medical prescriptions. When given an image of a prescription, you:
1. List each medicine with its name clearly
2. Explain what each medicine is used for in simple terms
3. State the dosage and timing as written
4. Note any important instructions (with food, avoid alcohol, etc.)
5. Flag any medicines that need special attention
Format your response clearly with sections for each medicine. End with: "⚠️ Always follow your doctor's instructions exactly."
"""

REPORT_SYSTEM = """You are an expert medical report analyst. When given a lab report image, you:
1. Identify the type of report (blood test, urine test, X-ray report, etc.)
2. List each parameter with its value and normal range
3. Clearly mark values as ✅ Normal, ⚠️ Slightly Abnormal, or 🚨 Needs Attention
4. Explain in plain simple language what each abnormal value might mean
5. Give a brief overall summary
6. Recommend whether they should see a doctor soon or if it looks routine
Use simple language — imagine you're explaining to someone with no medical knowledge."""

MEDICINE_SYSTEM = """You are a pharmaceutical expert. When asked about a medicine, provide:
## 💊 Medicine: [Name]
**What it's used for:** (in simple terms)
**How it works:** (brief, simple explanation)
**Common dosage:** (general guidance)
**How to take it:** (with food? water? timing?)
**Common side effects:** (list the most common ones)
**Important warnings:** (who should avoid it, interactions)
**Storage:** (how to store it)
Always end with: "⚠️ Only take medicines as prescribed by your doctor. Do not self-medicate."
"""

SYMPTOM_SYSTEM = """You are a medical triage assistant. When a user describes symptoms:
1. Acknowledge their symptoms with empathy
2. List 3-5 possible conditions that could cause these symptoms (from most to least likely)
3. For each condition, explain briefly what it is
4. Identify RED FLAG symptoms that need IMMEDIATE emergency care
5. Suggest simple home care if appropriate
6. Give clear guidance: "See a doctor today", "Schedule appointment this week", or "Monitor at home"
Be reassuring but honest. Never dismiss symptoms. Always err on the side of caution.
End with: "This is not a diagnosis. Please consult a doctor for proper evaluation."
"""

# ─────────────────────────────────────────────
# 🗂️ SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "chat_histories": {},
    "current_chat_id": None,
    "medicine_history": [],
    "rx_chat": [],        # Prescription follow-up chat
    "rx_result": None,    # Stores last prescription analysis
    "report_chat": [],    # Lab report follow-up chat
    "report_result": None,# Stores last report analysis
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def generate_id():
    return str(int(time.time() * 1000))

# ─────────────────────────────────────────────
# 🤖 AI FUNCTIONS
# ─────────────────────────────────────────────
def chat_with_ai(messages, system=CHAT_SYSTEM):
    try:
        full = [{"role": "system", "content": system}] + messages
        r = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=full,
            temperature=0.7,
            max_tokens=1024,
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def extract_text_from_file(uploaded_file):
    """Extract text content from PDF, DOCX, or TXT files."""
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()
    try:
        if filename.endswith(".txt"):
            return file_bytes.decode("utf-8", errors="ignore")
        elif filename.endswith(".pdf"):
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                return text.strip() or "Could not extract text from this PDF."
            except ImportError:
                return "PDF reading requires pypdf. Run: pip install pypdf"
        elif filename.endswith(".docx"):
            try:
                import docx
                doc = docx.Document(io.BytesIO(file_bytes))
                return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            except ImportError:
                return "DOCX reading requires python-docx. Run: pip install python-docx"
        else:
            return file_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Could not read file: {str(e)}"


def analyse_file(uploaded_file, prompt, system_prompt):
    """Universal file analyser — handles images, PDFs, DOCX, TXT."""
    filename = uploaded_file.name.lower()
    uploaded_file.seek(0)
    if any(filename.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"]):
        try:
            file_bytes = uploaded_file.read()
            if filename.endswith(".png"):
                mime = "image/png"
            elif filename.endswith(".gif"):
                mime = "image/gif"
            elif filename.endswith(".webp"):
                mime = "image/webp"
            else:
                mime = "image/jpeg"
            b64 = base64.standard_b64encode(file_bytes).decode("utf-8")
            r = client.chat.completions.create(
                model=VISION_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                        {"type": "text", "text": prompt}
                    ]}
                ],
                temperature=0.3,
                max_tokens=1500,
            )
            return r.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error analysing image: {str(e)}"
    else:
        text_content = extract_text_from_file(uploaded_file)
        if not text_content or len(text_content.strip()) < 20:
            return "⚠️ Could not extract readable text from this file. Please try a clearer image or a text-based PDF."
        try:
            r = client.chat.completions.create(
                model=TEXT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{prompt}\n\n--- FILE CONTENT ---\n{text_content[:6000]}"}
                ],
                temperature=0.3,
                max_tokens=1500,
            )
            return r.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error analysing file: {str(e)}"

def get_medicine_info(medicine_name):
    try:
        r = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": MEDICINE_SYSTEM},
                {"role": "user", "content": f"Tell me about the medicine: {medicine_name}"}
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def check_symptoms(symptoms):
    try:
        r = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": SYMPTOM_SYSTEM},
                {"role": "user", "content": f"I have these symptoms: {symptoms}"}
            ],
            temperature=0.5,
            max_tokens=1200,
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ─────────────────────────────────────────────
# 🔲 SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="icon">🏥</div>
        <div class="title">MediCare AI</div>
        <div class="sub">Your Personal Health Companion</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    menu = st.radio("Navigation", [
        "🏠  Home",
        "💬  AI Health Chat",
        "🔍  Symptom Checker",
        "📋  Prescription Reader",
        "🧪  Lab Report Analyser",
        "💊  Medicine Info",
        "🏥  Find Nearby Care",
        "📜  Chat History",
    ], label_visibility="collapsed")

    st.markdown("---")
    if st.button("➕  New Chat"):
        st.session_state.current_chat_id = None
        st.rerun()



# ─────────────────────────────────────────────
# 🏠 HOME
# ─────────────────────────────────────────────
if menu == "🏠  Home":
    st.markdown("# 🏥 Welcome to MediCare AI")
    st.markdown("##### Your complete personal health companion — powered by AI")
    st.markdown("---")

    cols = st.columns(4)
    stats = [
        ("💬", "AI Chat", "Ask any health question"),
        ("🔍", "Symptom Check", "Understand your symptoms"),
        ("📋", "Scan Documents", "Prescriptions & reports"),
        ("⏰", "Reminders", "Never miss a medicine"),
    ]
    for col, (icon, title, desc) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:28px">{icon}</div>
                <div style="font-weight:600;color:#f1f5f9;margin:8px 0 4px">{title}</div>
                <div style="font-size:12px;color:#64748b">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 What can I do for you?")

    features = [
        ("💬", "AI Health Chat",        "badge-blue",   "Chat freely about any health topic, medication, or wellness question with our AI doctor."),
        ("🔍", "Symptom Checker",       "badge-orange", "Describe how you're feeling and get an AI-powered analysis of possible causes and next steps."),
        ("📋", "Prescription Reader",   "badge-green",  "Take a photo of your prescription — AI will explain every medicine in plain language."),
        ("🧪", "Lab Report Analyser",   "badge-green",  "Upload your blood test or lab report — AI explains what each value means for your health."),
        ("💊", "Medicine Info",         "badge-blue",   "Search any medicine to learn its uses, dosage, side effects, and important warnings."),
        ("🏥", "Find Nearby Care",      "badge-red",    "Locate hospitals, clinics, pharmacies, and labs near you on an interactive map."),
    ]

    col1, col2 = st.columns(2)
    for i, (icon, title, badge, desc) in enumerate(features):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                    <span style="font-size:22px">{icon}</span>
                    <span style="font-weight:600;color:#f1f5f9;font-size:16px">{title}</span>
                </div>
                <p style="color:#94a3b8;font-size:13.5px;margin:0">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Medical Disclaimer:</strong> MediCare AI provides general health information and educational content only.
        It is <strong>not</strong> a substitute for professional medical advice, diagnosis, or treatment.
        Always consult a qualified healthcare provider for any medical concerns.
        In emergencies, call your local emergency number immediately.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 💬 AI HEALTH CHAT
# ─────────────────────────────────────────────
elif menu == "💬  AI Health Chat":
    st.markdown("## 💬 AI Health Chat")
    st.markdown('<div class="section-sub">Ask me anything about health, medicine, symptoms, or wellness</div>', unsafe_allow_html=True)

    if not st.session_state.current_chat_id:
        new_id = generate_id()
        st.session_state.current_chat_id = new_id
        st.session_state.chat_histories[new_id] = {"title": "New Chat", "messages": []}

    chat_id = st.session_state.current_chat_id
    chat    = st.session_state.chat_histories[chat_id]
    msgs    = chat["messages"]

    if not msgs:
        st.markdown("""
        <div class="bot-wrap">
        <div class="bot-bubble">
        👋 Hi! I'm your AI Health Assistant.<br><br>
        I can help you with:<br>
        • Understanding symptoms & conditions<br>
        • General health & wellness advice<br>
        • First aid guidance<br>
        • Medicine questions<br>
        • Preventive healthcare tips<br><br>
        What's on your mind today?
        </div></div>
        """, unsafe_allow_html=True)

    for m in msgs:
        if m["role"] == "user":
            st.markdown(f'<div class="user-wrap"><div class="user-bubble">{m["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-wrap"><div class="bot-bubble">{m["content"]}</div></div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask a health question...")
    if user_input:
        user_input = user_input.strip()
        if chat["title"] == "New Chat":
            chat["title"] = user_input[:35] + ("..." if len(user_input) > 35 else "")
        msgs.append({"role": "user", "content": user_input})
        st.markdown(f'<div class="user-wrap"><div class="user-bubble">{user_input}</div></div>', unsafe_allow_html=True)
        with st.spinner("🩺 Thinking..."):
            reply = chat_with_ai(msgs)
        msgs.append({"role": "assistant", "content": reply})
        st.markdown(f'<div class="bot-wrap"><div class="bot-bubble">{reply}</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🔍 SYMPTOM CHECKER
# ─────────────────────────────────────────────
elif menu == "🔍  Symptom Checker":
    st.markdown("## 🔍 Symptom Checker")
    st.markdown('<div class="section-sub">Describe your symptoms and get an AI-powered health assessment</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        🚨 <strong>Emergency?</strong> If you have chest pain, difficulty breathing, severe bleeding, or loss of consciousness —
        <strong>call emergency services (112 / 108) immediately.</strong>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        symptoms = st.text_area(
            "Describe your symptoms in detail",
            placeholder="e.g. I have had a headache for 2 days, mild fever of 99°F, and feel very tired. No cough or cold...",
            height=130
        )
    with col2:
        duration   = st.selectbox("How long?", ["Just started", "1-2 days", "3-7 days", "1-2 weeks", "More than 2 weeks"])
        severity   = st.selectbox("Severity",  ["Mild", "Moderate", "Severe"])
        age_group  = st.selectbox("Age group", ["Child (0-12)", "Teen (13-17)", "Adult (18-60)", "Senior (60+)"])

    if st.button("🔍 Analyse Symptoms"):
        if symptoms.strip():
            full_query = f"Symptoms: {symptoms}\nDuration: {duration}\nSeverity: {severity}\nAge group: {age_group}"
            with st.spinner("🔍 Analysing your symptoms..."):
                result = check_symptoms(full_query)
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please describe your symptoms first.")

# ─────────────────────────────────────────────
# 📋 PRESCRIPTION READER
# ─────────────────────────────────────────────
elif menu == "📋  Prescription Reader":
    st.markdown("## 📋 Prescription Reader")
    st.markdown('<div class="section-sub">Upload your prescription — AI explains every medicine in plain language, then ask follow-up questions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="card">
            <strong>📁 Supported file types:</strong><br><br>
            🖼️ <strong>Images:</strong> JPG, JPEG, PNG, WEBP<br>
            📄 <strong>Documents:</strong> PDF, DOCX, TXT<br><br>
            <strong>📸 Tips for best results:</strong><br>
            ✅ Good lighting if using a photo<br>
            ✅ All text clearly visible<br>
            ✅ Use PDF/DOCX for digital prescriptions
        </div>
        """, unsafe_allow_html=True)
        uploaded_rx = st.file_uploader(
            "Upload Prescription (Image, PDF, DOCX, or TXT)",
            type=["jpg", "jpeg", "png", "webp", "pdf", "docx", "txt"],
            key="rx_uploader"
        )

    with col2:
        if uploaded_rx:
            fname = uploaded_rx.name.lower()
            if any(fname.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                st.image(uploaded_rx, caption="Your Prescription", use_container_width=True)
            else:
                st.markdown(
                    f'<div class="card" style="text-align:center;padding:40px">' +
                    '<div style="font-size:48px">📄</div>' +
                    f'<div style="color:#94a3b8;margin-top:12px">{uploaded_rx.name}</div>' +
                    '<div style="color:#64748b;font-size:12px;margin-top:4px">Ready to analyse</div></div>',
                    unsafe_allow_html=True
                )

    if uploaded_rx:
        if st.button("📋 Read & Explain Prescription"):
            with st.spinner("🔍 Reading your prescription..."):
                result = analyse_file(
                    uploaded_rx,
                    "Please read this prescription and explain all medicines clearly.",
                    PRESCRIPTION_SYSTEM
                )
            st.session_state.rx_result = result
            st.session_state.rx_chat   = []   # Reset chat for new prescription

    # ── Show analysis result if exists
    if st.session_state.rx_result:
        st.markdown("### 📋 Prescription Analysis")
        st.markdown(
            '<div class="result-box">' + st.session_state.rx_result + '</div>',
            unsafe_allow_html=True
        )
        st.markdown("""
        <div class="disclaimer">
            ⚠️ This is an AI reading. Always verify with your doctor or pharmacist.
            Never change your dosage based on this analysis alone.
        </div>
        """, unsafe_allow_html=True)

        # ── Follow-up Chat
        st.markdown("---")
        st.markdown("### 💬 Ask a Follow-up Question")
        st.markdown('<div class="section-sub">Ask anything about this prescription — medicines, dosage, side effects, interactions...</div>', unsafe_allow_html=True)

        # Display existing chat
        for msg in st.session_state.rx_chat:
            if msg["role"] == "user":
                st.markdown(
                    '<div class="user-wrap"><div class="user-bubble">' + msg["content"] + '</div></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="bot-wrap"><div class="bot-bubble">' + msg["content"] + '</div></div>',
                    unsafe_allow_html=True
                )

        # Chat input
        rx_question = st.chat_input("e.g. Can I take these medicines together? Any side effects?", key="rx_chat_input")
        if rx_question:
            rx_question = rx_question.strip()
            st.session_state.rx_chat.append({"role": "user", "content": rx_question})
            st.markdown(
                '<div class="user-wrap"><div class="user-bubble">' + rx_question + '</div></div>',
                unsafe_allow_html=True
            )

            # Build context-aware messages — AI knows the prescription result
            context_messages = [
                {
                    "role": "assistant",
                    "content": "I have analysed the prescription. Here is what it contains:\n\n" + st.session_state.rx_result
                }
            ] + st.session_state.rx_chat

            with st.spinner("🩺 Thinking..."):
                rx_reply = chat_with_ai(
                    context_messages,
                    system=PRESCRIPTION_SYSTEM + "\n\nThe user has already uploaded a prescription which you have analysed. Answer their follow-up questions based on that analysis."
                )
            st.session_state.rx_chat.append({"role": "assistant", "content": rx_reply})
            st.markdown(
                '<div class="bot-wrap"><div class="bot-bubble">' + rx_reply + '</div></div>',
                unsafe_allow_html=True
            )

        # Clear chat button
        if st.session_state.rx_chat:
            if st.button("🗑 Clear Chat", key="clear_rx_chat"):
                st.session_state.rx_chat = []
                st.rerun()

# ─────────────────────────────────────────────
# 🧪 LAB REPORT ANALYSER
# ─────────────────────────────────────────────
elif menu == "🧪  Lab Report Analyser":
    st.markdown("## 🧪 Lab Report Analyser")
    st.markdown('<div class="section-sub">Upload your lab report — get a plain-language explanation, then ask follow-up questions</div>', unsafe_allow_html=True)

    report_type = st.selectbox("Report Type", [
        "Blood Test (CBC / Complete Blood Count)",
        "Blood Sugar / HbA1c",
        "Lipid Profile / Cholesterol",
        "Liver Function Test (LFT)",
        "Kidney Function Test (KFT)",
        "Thyroid Test (TSH/T3/T4)",
        "Urine Test",
        "Other / Not Sure"
    ])

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="card">
            <strong>📁 Supported file types:</strong><br><br>
            🖼️ <strong>Images:</strong> JPG, JPEG, PNG, WEBP<br>
            📄 <strong>Documents:</strong> PDF, DOCX, TXT<br><br>
            ✅ Digital lab reports work best as PDF<br>
            ✅ Printed reports — take a clear photo
        </div>
        """, unsafe_allow_html=True)
        uploaded_report = st.file_uploader(
            "Upload Lab Report (Image, PDF, DOCX, or TXT)",
            type=["jpg", "jpeg", "png", "webp", "pdf", "docx", "txt"],
            key="report_uploader"
        )
    with col2:
        if uploaded_report:
            fname = uploaded_report.name.lower()
            if any(fname.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                st.image(uploaded_report, caption="Your Lab Report", use_container_width=True)
            else:
                st.markdown(
                    f'<div class="card" style="text-align:center;padding:40px">' +
                    '<div style="font-size:48px">📄</div>' +
                    f'<div style="color:#94a3b8;margin-top:12px">{uploaded_report.name}</div>' +
                    '<div style="color:#64748b;font-size:12px;margin-top:4px">Ready to analyse</div></div>',
                    unsafe_allow_html=True
                )

    if uploaded_report:
        if st.button("🧪 Analyse My Report"):
            with st.spinner("🔬 Analysing your lab report..."):
                result = analyse_file(
                    uploaded_report,
                    f"This is a {report_type}. Please analyse all values and explain them clearly.",
                    REPORT_SYSTEM
                )
            st.session_state.report_result = result
            st.session_state.report_chat   = []  # Reset chat for new report

    # ── Show analysis result if exists
    if st.session_state.report_result:
        st.markdown("### 🧪 Report Analysis")
        st.markdown(
            '<div class="result-box">' + st.session_state.report_result + '</div>',
            unsafe_allow_html=True
        )
        st.markdown("""
        <div class="disclaimer">
            ⚠️ AI analysis is for educational purposes only. Abnormal values should always be
            discussed with your doctor who knows your full medical history.
        </div>
        """, unsafe_allow_html=True)

        # ── Follow-up Chat
        st.markdown("---")
        st.markdown("### 💬 Ask a Follow-up Question")
        st.markdown('<div class="section-sub">Ask anything about your report — what values mean, what to do next, what food to eat...</div>', unsafe_allow_html=True)

        # Display existing chat
        for msg in st.session_state.report_chat:
            if msg["role"] == "user":
                st.markdown(
                    '<div class="user-wrap"><div class="user-bubble">' + msg["content"] + '</div></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="bot-wrap"><div class="bot-bubble">' + msg["content"] + '</div></div>',
                    unsafe_allow_html=True
                )

        # Chat input
        report_question = st.chat_input("e.g. My sugar is high — what should I eat? Is this serious?", key="report_chat_input")
        if report_question:
            report_question = report_question.strip()
            st.session_state.report_chat.append({"role": "user", "content": report_question})
            st.markdown(
                '<div class="user-wrap"><div class="user-bubble">' + report_question + '</div></div>',
                unsafe_allow_html=True
            )

            # Build context-aware messages — AI knows the report result
            context_messages = [
                {
                    "role": "assistant",
                    "content": "I have analysed the lab report. Here are the findings:\n\n" + st.session_state.report_result
                }
            ] + st.session_state.report_chat

            with st.spinner("🩺 Thinking..."):
                report_reply = chat_with_ai(
                    context_messages,
                    system=REPORT_SYSTEM + "\n\nThe user has already uploaded a lab report which you have analysed. Answer their follow-up questions based on that analysis."
                )
            st.session_state.report_chat.append({"role": "assistant", "content": report_reply})
            st.markdown(
                '<div class="bot-wrap"><div class="bot-bubble">' + report_reply + '</div></div>',
                unsafe_allow_html=True
            )

        # Clear chat button
        if st.session_state.report_chat:
            if st.button("🗑 Clear Chat", key="clear_report_chat"):
                st.session_state.report_chat = []
                st.rerun()

# ─────────────────────────────────────────────
# 💊 MEDICINE INFO
# ─────────────────────────────────────────────
elif menu == "💊  Medicine Info":
    st.markdown("## 💊 Medicine Information")
    st.markdown('<div class="section-sub">Search any medicine to understand its uses, dosage, and side effects</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        med_name = st.text_input("Enter medicine name", placeholder="e.g. Paracetamol, Azithromycin, Metformin, Omeprazole...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search Medicine")

    # Quick search suggestions
    st.markdown("**Common searches:**")
    quick_cols = st.columns(6)
    common = ["Paracetamol", "Ibuprofen", "Amoxicillin", "Metformin", "Omeprazole", "Cetirizine"]
    for col, med in zip(quick_cols, common):
        with col:
            if st.button(med, key=f"quick_{med}"):
                med_name = med
                search_btn = True

    if search_btn and med_name:
        with st.spinner(f"🔍 Looking up {med_name}..."):
            result = get_medicine_info(med_name)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
        # Save to history
        st.session_state.medicine_history.append({
            "name": med_name, "time": datetime.now().strftime("%d %b %Y, %H:%M")
        })

    # Search history
    if st.session_state.medicine_history:
        st.markdown("---")
        st.markdown("### 🕓 Recent Searches")
        for item in reversed(st.session_state.medicine_history[-5:]):
            st.markdown(f'<span class="badge badge-blue">💊 {item["name"]}</span> <span style="color:#475569;font-size:12px">  {item["time"]}</span>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# 🏥 FIND NEARBY CARE
# ─────────────────────────────────────────────
elif menu == "🏥  Find Nearby Care":
    st.markdown("## 🏥 Find Nearby Healthcare")
    st.markdown('<div class="section-sub">Find hospitals, clinics, pharmacies, and labs near you — 100% free, no API key needed</div>', unsafe_allow_html=True)

    # ── Care type selector
    care_type = st.selectbox("What are you looking for?", [
        "🏥 Hospital",
        "🏨 Clinic / Polyclinic",
        "💊 Pharmacy / Medical Store",
        "🧪 Diagnostic Lab / Pathology",
        "🦷 Dentist",
        "👁 Eye Specialist",
    ])
    care_label = care_type.split(" ", 1)[1]

    # OSM amenity tag mapping
    amenity_map = {
        "Hospital":               "hospital",
        "Clinic / Polyclinic":    "clinic",
        "Pharmacy / Medical Store":"pharmacy",
        "Diagnostic Lab / Pathology": "doctors",
        "Dentist":                "dentist",
        "Eye Specialist":         "doctors",
    }
    amenity_tag = amenity_map.get(care_label, "hospital")

    st.markdown("---")
    st.markdown("### 📍 How would you like to share your location?")

    loc_method = st.radio(
        "Location method",
        ["📡 Use My Live Location (GPS)", "✍️ Type My Location Manually"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # ── Session state for coordinates
    if "detected_lat" not in st.session_state:
        st.session_state.detected_lat = None
    if "detected_lng" not in st.session_state:
        st.session_state.detected_lng = None

    user_lat = None
    user_lng = None
    typed_location = ""

    # ────────────────────────────────
    # GPS METHOD
    # ────────────────────────────────
    if loc_method == "📡 Use My Live Location (GPS)":
        st.markdown("""
        <div class="card">
            <strong>📡 Live GPS Location</strong><br>
            <span style="color:#94a3b8;font-size:13px">
                Click <strong>Detect My Location</strong> below.
                Your browser will ask for permission — click <strong>Allow</strong>.
                Results will load automatically once your location is detected.
            </span>
        </div>
        """, unsafe_allow_html=True)

        # JS component — posts coords to Streamlit via query params trick
        import streamlit.components.v1 as components
        components.html("""
        <div style="font-family:'DM Sans',sans-serif;padding:4px 0">
            <button onclick="getLocation()" id="loc_btn" style="
                background:linear-gradient(135deg,#2563eb,#1d4ed8);
                color:white;border:none;padding:14px 28px;
                border-radius:12px;font-size:15px;cursor:pointer;
                font-weight:600;width:100%;letter-spacing:0.3px">
                📡 Detect My Location
            </button>
            <div id="status" style="margin-top:14px;font-size:13px;color:#94a3b8;min-height:20px"></div>
        </div>

        <script>
        function getLocation() {
            var btn    = document.getElementById("loc_btn");
            var status = document.getElementById("status");
            btn.innerText    = "⏳ Detecting...";
            btn.style.opacity = "0.7";
            status.innerHTML  = "Requesting location permission...";

            if (!navigator.geolocation) {
                status.innerHTML = "❌ Geolocation is not supported by your browser.";
                btn.innerText = "📡 Detect My Location";
                btn.style.opacity = "1";
                return;
            }

            navigator.geolocation.getCurrentPosition(
                function(pos) {
                    var lat = pos.coords.latitude.toFixed(7);
                    var lng = pos.coords.longitude.toFixed(7);
                    status.innerHTML = "✅ Location detected! Lat: <strong style='color:#60a5fa'>" + lat +
                        "</strong> &nbsp;|&nbsp; Lng: <strong style='color:#60a5fa'>" + lng + "</strong>" +
                        "<br><span style='color:#4ade80;font-size:12px;margin-top:4px;display:block'>" +
                        "📋 Copy these values into the boxes below and click Find Top 5 Near Me</span>";
                    btn.innerText    = "✅ Location Detected";
                    btn.style.background = "linear-gradient(135deg,#16a34a,#15803d)";

                    // Fill hidden inputs
                    document.getElementById("lat_field").value = lat;
                    document.getElementById("lng_field").value = lng;
                    document.getElementById("coord_box").style.display = "block";
                    document.getElementById("show_lat").innerText = lat;
                    document.getElementById("show_lng").innerText = lng;
                },
                function(err) {
                    var msg = {
                        1: "Permission denied. Please allow location access in your browser settings.",
                        2: "Location unavailable. Check your GPS/internet connection.",
                        3: "Request timed out. Please try again."
                    };
                    status.innerHTML = "❌ " + (msg[err.code] || err.message);
                    btn.innerText    = "📡 Try Again";
                    btn.style.opacity = "1";
                },
                { timeout: 15000, maximumAge: 0, enableHighAccuracy: true }
            );
        }
        </script>

        <div id="coord_box" style="display:none;margin-top:14px;
             background:#0f172a;border:1px solid #2d3f5e;
             border-radius:12px;padding:16px">
            <div style="color:#64748b;font-size:11px;text-transform:uppercase;
                        letter-spacing:1px;margin-bottom:8px">Your Coordinates</div>
            <div style="color:#e2e8f0;font-size:14px">
                📍 Latitude: <strong style="color:#60a5fa" id="show_lat"></strong>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Longitude: <strong style="color:#60a5fa" id="show_lng"></strong>
            </div>
            <input type="hidden" id="lat_field">
            <input type="hidden" id="lng_field">
        </div>
        """, height=200)

        col_lat, col_lng = st.columns(2)
        with col_lat:
            lat_str = st.text_input("Latitude (from above)", placeholder="e.g. 19.0759837",
                                    key="lat_input")
        with col_lng:
            lng_str = st.text_input("Longitude (from above)", placeholder="e.g. 72.8776559",
                                    key="lng_input")

        if lat_str and lng_str:
            try:
                user_lat = float(lat_str.strip())
                user_lng = float(lng_str.strip())
                st.success(f"✅ Location ready: {user_lat:.5f}, {user_lng:.5f}")
            except:
                st.error("❌ Please enter valid coordinates.")

    # ────────────────────────────────
    # MANUAL ADDRESS METHOD
    # ────────────────────────────────
    else:
        st.markdown("""
        <div class="card">
            <strong>✍️ Type Your Location</strong><br>
            <span style="color:#94a3b8;font-size:13px">
                Be specific for best results — include area, landmark, city and state.
            </span>
        </div>
        """, unsafe_allow_html=True)
        typed_location = st.text_input(
            "Your Address",
            placeholder="e.g. Bandra West, Mumbai, Maharashtra  or  Connaught Place, New Delhi"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ────────────────────────────────
    # FIND BUTTON
    # ────────────────────────────────
    find_clicked = st.button("🔍 Find Top 5 Near Me", use_container_width=True)

    if find_clicked:
        has_coords  = user_lat is not None and user_lng is not None
        has_address = typed_location.strip() != ""

        if not has_coords and not has_address:
            st.warning("⚠️ Please share your location first.")
        else:
            # ── Geocode typed address → lat/lng using Nominatim (free)
            if has_address and not has_coords:
                with st.spinner("📍 Finding your location..."):
                    try:
                        geo_url = "https://nominatim.openstreetmap.org/search"
                        geo_params = {
                            "q": typed_location,
                            "format": "json",
                            "limit": 1
                        }
                        geo_headers = {"User-Agent": "MediCareAI/1.0"}
                        geo_resp = requests.get(geo_url, params=geo_params,
                                                headers=geo_headers, timeout=10).json()
                        if geo_resp:
                            user_lat = float(geo_resp[0]["lat"])
                            user_lng = float(geo_resp[0]["lon"])
                            st.success(f"📍 Location found: {geo_resp[0]['display_name'][:60]}...")
                        else:
                            st.error("❌ Could not find that location. Please be more specific.")
                            st.stop()
                    except Exception as e:
                        st.error(f"❌ Location lookup failed: {str(e)}")
                        st.stop()

            # ── Query OpenStreetMap Overpass API
            with st.spinner(f"🔍 Searching for {care_label} nearby..."):
                try:
                    radius = 5000  # 5km radius

                    # Build compact query (GET is more reliable than POST)
                    overpass_query = (
                        f"[out:json][timeout:25];"
                        f"(node[amenity={amenity_tag}](around:{radius},{user_lat},{user_lng});"
                        f"way[amenity={amenity_tag}](around:{radius},{user_lat},{user_lng}););"
                        f"out center tags;"
                    )

                    # Try multiple Overpass mirrors for reliability
                    mirrors = [
                        "https://overpass-api.de/api/interpreter",
                        "https://overpass.kumi.systems/api/interpreter",
                        "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
                    ]

                    raw_resp = None
                    last_error = ""
                    for mirror in mirrors:
                        try:
                            r = requests.get(
                                mirror,
                                params={"data": overpass_query},
                                timeout=25,
                                headers={"User-Agent": "MediCareAI/1.0"}
                            )
                            if r.status_code == 200 and r.text.strip().startswith("{"):
                                raw_resp = r.json()
                                break
                            else:
                                last_error = f"HTTP {r.status_code}"
                        except Exception as ex:
                            last_error = str(ex)[:60]
                            continue

                    if raw_resp is None:
                        # All mirrors failed — show Google Maps fallback
                        loc_str = f"{user_lat},{user_lng}"
                        search_q = requests.utils.quote(f"{care_label} near me")
                        maps_url = f"https://www.google.com/maps/search/{search_q}/@{user_lat},{user_lng},14z"
                        st.warning("⚠️ The map data service is temporarily busy. Here's a direct Google Maps link instead:")
                        st.markdown(
                            f"<a href='{maps_url}' target='_blank' style='"
                            "background:linear-gradient(135deg,#2563eb,#1d4ed8);"
                            "color:white;padding:12px 24px;border-radius:10px;"
                            "text-decoration:none;font-weight:600;font-size:14px;"
                            "display:inline-block;margin-top:8px'>"
                            f"🗺 Find {care_label} on Google Maps</a>",
                            unsafe_allow_html=True
                        )
                        st.stop()

                    resp = raw_resp
                    elements = resp.get("elements", [])

                    # Sort by distance and take top 5
                    import math

                    def haversine(lat1, lng1, lat2, lng2):
                        R = 6371
                        dlat = math.radians(lat2 - lat1)
                        dlng = math.radians(lng2 - lng1)
                        a = (math.sin(dlat/2)**2 +
                             math.cos(math.radians(lat1)) *
                             math.cos(math.radians(lat2)) *
                             math.sin(dlng/2)**2)
                        return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)), 2)

                    def parse_open_status(oh_str):
                        """Parse opening_hours string and return (timing_display, is_open)"""
                        if not oh_str:
                            return "Hours not listed", None
                        # Check for 24/7
                        if oh_str.strip() == "24/7":
                            return "Open 24/7", True
                        return oh_str[:60], None   # show raw string, status unknown

                    def get_coords(el):
                        if el["type"] == "node":
                            return el.get("lat"), el.get("lon")
                        else:
                            c = el.get("center", {})
                            return c.get("lat"), c.get("lon")

                    # Enrich with distance
                    results = []
                    for el in elements:
                        tags = el.get("tags", {})
                        name = tags.get("name") or tags.get("name:en") or tags.get("operator")
                        if not name:
                            continue
                        plat, plng = get_coords(el)
                        if not plat or not plng:
                            continue
                        dist = haversine(user_lat, user_lng, plat, plng)
                        results.append({
                            "name":    name,
                            "tags":    tags,
                            "lat":     plat,
                            "lng":     plng,
                            "dist_km": dist,
                        })

                    results = sorted(results, key=lambda x: x["dist_km"])[:5]

                    if not results:
                        st.warning(f"No {care_label} found within 5km. Try a different location or category.")
                    else:
                        st.markdown(f"### 🏥 Top {len(results)} {care_label} Near You")
                        st.markdown('<div style="color:#64748b;font-size:13px;margin-bottom:20px">Sorted by distance from your location • Data from OpenStreetMap</div>', unsafe_allow_html=True)

                        for i, place in enumerate(results, 1):
                            tags    = place["tags"]
                            name    = place["name"]
                            dist_km = place["dist_km"]
                            plat    = place["lat"]
                            plng    = place["lng"]

                            # Build address
                            addr_parts = []
                            for key in ["addr:housenumber","addr:street",
                                        "addr:suburb","addr:city","addr:state"]:
                                if tags.get(key):
                                    addr_parts.append(tags[key])
                            address = (", ".join(addr_parts)
                                       if addr_parts
                                       else tags.get("addr:full","Address not listed"))

                            # Timing & status
                            oh_raw = tags.get("opening_hours","")
                            timing_str, is_open = parse_open_status(oh_raw)

                            if timing_str == "Open 24/7":
                                status_text = "🟢 Open 24/7"
                                status_color = "#4ade80"
                            elif is_open is True:
                                status_text  = "🟢 Open Now"
                                status_color = "#4ade80"
                            elif is_open is False:
                                status_text  = "🔴 Closed"
                                status_color = "#f87171"
                            else:
                                status_text  = "⏰ Status unknown"
                                status_color = "#94a3b8"

                            # Distance
                            dist_display = (f"{int(dist_km*1000)} m away"
                                            if dist_km < 1 else f"{dist_km} km away")

                            # Google Maps link
                            maps_link = (f"https://www.google.com/maps/dir/?api=1"
                                         f"&destination={plat},{plng}&travelmode=driving")

                            # Build clean HTML with no f-string CSS conflicts
                            html = (
                                "<div style='background:linear-gradient(135deg,#111827,#0f172a);"
                                "border:1px solid #1e2840;border-left:4px solid #2563eb;"
                                "border-radius:16px;padding:22px;margin-bottom:16px'>"

                                # Header row
                                "<div style='display:flex;justify-content:space-between;"
                                "align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:16px'>"
                                "<div style='display:flex;align-items:center;gap:10px'>"
                                "<span style='background:#1e3a5f;color:#60a5fa;font-size:11px;"
                                "font-weight:700;padding:3px 10px;border-radius:20px;"
                                "letter-spacing:1px'>NO " + str(i) + "</span>"
                                "<span style='color:#f1f5f9;font-size:17px;font-weight:700'>"
                                + name + "</span></div>"
                                "<span style='color:#fbbf24;font-size:13px;background:#1c1810;"
                                "padding:4px 12px;border-radius:20px;border:1px solid #854d0e;"
                                "font-weight:600'>📏 " + dist_display + "</span>"
                                "</div>"

                                # Fields
                                "<table style='width:100%;border-collapse:collapse'>"

                                "<tr style='border-bottom:1px solid #1e2840'>"
                                "<td style='color:#64748b;font-size:11px;text-transform:uppercase;"
                                "letter-spacing:1px;padding:8px 0;width:90px'>Address</td>"
                                "<td style='color:#cbd5e1;font-size:14px;padding:8px 0'>"
                                "📍 " + address + "</td></tr>"

                                "<tr style='border-bottom:1px solid #1e2840'>"
                                "<td style='color:#64748b;font-size:11px;text-transform:uppercase;"
                                "letter-spacing:1px;padding:8px 0'>Timing</td>"
                                "<td style='color:#cbd5e1;font-size:14px;padding:8px 0'>"
                                "🕐 " + timing_str + "</td></tr>"

                                "<tr style='border-bottom:1px solid #1e2840'>"
                                "<td style='color:#64748b;font-size:11px;text-transform:uppercase;"
                                "letter-spacing:1px;padding:8px 0'>Status</td>"
                                "<td style='color:" + status_color + ";font-size:14px;"
                                "font-weight:600;padding:8px 0'>" + status_text + "</td></tr>"

                                "<tr>"
                                "<td style='color:#64748b;font-size:11px;text-transform:uppercase;"
                                "letter-spacing:1px;padding:10px 0'>Directions</td>"
                                "<td style='padding:10px 0'>"
                                "<a href='" + maps_link + "' target='_blank' "
                                "style='background:linear-gradient(135deg,#2563eb,#1d4ed8);"
                                "color:white;padding:9px 18px;border-radius:9px;"
                                "text-decoration:none;font-size:13px;font-weight:600;"
                                "display:inline-block'>🗺 Get Directions on Google Maps</a>"
                                "</td></tr>"

                                "</table></div>"
                            )
                            st.markdown(html, unsafe_allow_html=True)

                except requests.exceptions.Timeout:
                    st.error("⏳ Search timed out. Please try again in a moment.")
                except Exception as e:
                    st.error(f"❌ Search failed: {str(e)}")

    # ── Emergency Numbers
    st.markdown("---")
    st.markdown("### 🚨 Emergency Numbers (India)")
    ecols = st.columns(4)
    emergencies = [
        ("🚑", "Ambulance", "108"),
        ("🚒", "Fire",      "101"),
        ("👮", "Police",    "100"),
        ("☎️",  "Helpline",  "112"),
    ]
    for col, (icon, label, num) in zip(ecols, emergencies):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:26px">{icon}</div>
                <div style="font-weight:600;color:#f87171;font-size:22px">{num}</div>
                <div style="color:#64748b;font-size:12px">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 📜 CHAT HISTORY
# ─────────────────────────────────────────────
elif menu == "📜  Chat History":
    st.markdown("## 📜 Chat History")
    st.markdown('<div class="section-sub">View, continue, rename or delete your past conversations</div>', unsafe_allow_html=True)

    if not st.session_state.chat_histories:
        st.info("💬 No chat history yet. Start a conversation in AI Health Chat!")
    else:
        for chat_id, chat in list(st.session_state.chat_histories.items()):
            title     = chat.get("title", "Unnamed Chat")
            msg_count = len(chat.get("messages", []))
            with st.expander(f"💬 {title} — {msg_count} messages"):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    new_title = st.text_input("Rename:", value=title, key=f"rename_{chat_id}")
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("✅ Save", key=f"save_{chat_id}"):
                        st.session_state.chat_histories[chat_id]["title"] = new_title.strip()
                        st.rerun()
                with col3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("▶ Continue", key=f"cont_{chat_id}"):
                        st.session_state.current_chat_id = chat_id
                        st.rerun()

                st.markdown("**Conversation Preview:**")
                for m in chat.get("messages", [])[:6]:
                    role = "👤 You" if m["role"] == "user" else "🩺 AI"
                    preview = m["content"][:150] + ("..." if len(m["content"]) > 150 else "")
                    st.markdown(f'<div style="font-size:13px;color:#94a3b8;padding:4px 0"><strong>{role}:</strong> {preview}</div>', unsafe_allow_html=True)

                if st.button("🗑 Delete Chat", key=f"del_{chat_id}"):
                    del st.session_state.chat_histories[chat_id]
                    st.rerun()

        st.markdown("---")
        if st.button("🗑 Clear ALL History"):
            st.session_state.chat_histories = {}
            st.session_state.current_chat_id = None
            st.success("✅ All history cleared!")
            st.rerun()
