<div align="center">

# 🏥 MediCare AI
### Your Personal AI-Powered Health Companion

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medicare-ai.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Groq](https://img.shields.io/badge/Powered%20by-Groq-orange?style=flat)
![LLaMA](https://img.shields.io/badge/Model-LLaMA%203.3%2070B-green?style=flat)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat)

**A full-stack AI health companion that helps everyday people understand their health —**
**prescriptions, lab reports, symptoms, medicines, and nearby care — all in one place.**

[🚀 Try the Live App](https://medicare-ai.streamlit.app/)

---

</div>

## 📌 Problem Statement

Most people struggle to understand medical documents. Prescriptions are full of shorthand, lab reports are packed with confusing numbers, and symptoms are hard to describe to a doctor. At the same time, searching health questions online gives overwhelming or unreliable results.

There is no single, simple tool that can read a prescription, explain lab values, check symptoms, and help you find a nearby clinic — all without medical jargon.

---

## 🎯 Project Objective

MediCare AI is built to solve exactly that problem. The goal is to give anyone — regardless of their medical knowledge — a smart, easy-to-use health assistant that:

- Explains prescriptions and lab reports in plain language
- Helps understand symptoms and when to seek care
- Provides quick, reliable information about medicines
- Locates nearby hospitals, clinics, and pharmacies
- Responds instantly, like talking to a knowledgeable friend

> ⚠️ **Disclaimer:** MediCare AI is for general health information only. It is not a substitute for professional medical advice. Always consult a qualified healthcare provider for medical concerns.

---

## 🔍 How the App Works

MediCare AI is a **multi-feature Streamlit web app** powered by Groq's ultra-fast AI inference. Here is what each feature does:

### 💬 AI Health Chat
Have a full conversation about any health topic. The AI remembers your entire conversation, so follow-up questions are always answered in context — just like talking to a knowledgeable friend.

### 🔍 Symptom Checker
Describe your symptoms along with how long you have had them and how severe they feel. The AI gives you a structured response — possible causes, warning signs to watch for, and whether you should see a doctor now or monitor at home.

### 📋 Prescription Reader
Upload a prescription as a photo, PDF, DOCX, or TXT file. The AI reads every medicine listed, explains what it is for in simple words, states the correct dosage, and flags important warnings. You can then ask follow-up questions about your prescription.

### 🧪 Lab Report Analyser
Upload any blood test, thyroid report, lipid profile, or other lab report. The AI explains every value, marks what is normal and what is not, and tells you what it means for your health — in language anyone can understand. Includes a follow-up chat for deeper questions.

### 💊 Medicine Info
Search any medicine by name and get its uses, how it works, standard dosage, how to take it, common side effects, important warnings, and storage instructions.

### 🏥 Find Nearby Care
Find hospitals, clinics, pharmacies, diagnostic labs, dentists, and eye specialists near you. Supports both live GPS location and manual address entry. Results show the name, address, timing, open or closed status, distance, and a direct Google Maps directions link.

### 📜 Chat History
View, rename, continue, or delete past AI Health Chat conversations — all within the same session.

---

## 🤖 Technology Used

| Component | Technology |
|---|---|
| **AI Engine** | [Groq](https://groq.com) — ultra-fast LLM inference |
| **Text Model** | Meta LLaMA 3.3 70B (`llama-3.3-70b-versatile`) |
| **Vision Model** | Meta LLaMA 4 Scout 17B (`meta-llama/llama-4-scout-17b-16e-instruct`) |
| **Web Framework** | [Streamlit](https://streamlit.io) |
| **Maps & Location** | OpenStreetMap + Nominatim + Overpass API |
| **Language** | Python 3.10+ |

**Why Groq?**
Groq uses custom LPU (Language Processing Unit) hardware that makes AI responses appear in 1–2 seconds instead of 10–15 seconds. This makes conversations feel fast and natural.

**Why LLaMA 3.3 70B?**
At 70 billion parameters, this is Meta's most capable open-weight model. It delivers strong reasoning, detailed medical knowledge, clear structured responses, and multilingual ability.

**Why LLaMA 4 Scout for Vision?**
LLaMA 4 Scout is a multimodal model capable of reading text from images with high accuracy — ideal for handwritten or printed prescriptions and lab reports.

---

## 🏗️ App Architecture

```
User
 │
 ▼
Streamlit Frontend (app.py)
 │
 ├── Text queries ──────────► Groq API (LLaMA 3.3 70B)
 │
 ├── Image/document uploads ─► Groq API (LLaMA 4 Scout Vision)
 │
 ├── Location search ────────► OpenStreetMap Overpass API
 │
 └── Geocoding ──────────────► Nominatim API
```

The entire app lives in a single file (`app.py`). All AI calls go through Groq's API. Document uploads are processed in memory — nothing is saved to disk or any database.

---

## 🚀 Getting Started (Run Locally)

### Prerequisites
- Python 3.10 or higher
- A free [Groq API key](https://console.groq.com)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/DHAMMADEEPRAMTEKE30/medicare-ai.git
cd medicare-ai
```

### Step 2 — Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add Your API Key
Create a `.env` file in the root folder and add:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at: https://console.groq.com

### Step 5 — Run the App
```bash
streamlit run app.py
```
The app will open at `http://localhost:8501`

---

## ☁️ Deploy Your Own Copy

This app is deployed on **Streamlit Cloud** — free hosting for Streamlit apps.

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository, branch `main`, file `app.py`
5. Go to **Advanced Settings → Secrets** and add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
6. Click **Deploy**

---

## 🔒 Privacy & Security

- Your API key is stored securely in `.env` locally or in Streamlit Secrets when deployed
- `.env` is in `.gitignore` — it is never uploaded to GitHub
- No user data is stored or logged anywhere
- Uploaded documents are processed in memory only — never saved to disk
- All conversations exist only within the current session

---

## 📁 Files in This Repository

```
medicare-ai/
├── app.py              # Main application — all features in one file
├── requirements.txt    # Python package dependencies
├── .gitignore          # Files excluded from version control
└── README.md           # Project documentation
```

---

## 💡 Key Features at a Glance

| Feature | What It Does |
|---|---|
| AI Health Chat | Full conversational chat with memory across turns |
| Symptom Checker | Structured symptom assessment with red flag alerts |
| Prescription Reader | Reads and explains uploaded prescriptions |
| Lab Report Analyser | Breaks down lab values in plain language |
| Medicine Info | Full medicine details by name search |
| Find Nearby Care | GPS or address-based search for clinics and hospitals |
| Chat History | Save, rename, and revisit past conversations |

---

## 🗺️ Roadmap

- [ ] Multi-language support (Hindi, Marathi, Tamil, and more)
- [ ] Voice input for health questions
- [ ] Export prescription and lab report analysis as PDF
- [ ] Drug interaction checker
- [ ] BMI and health metrics calculator
- [ ] Health history tracking across sessions

---

## 🛠️ Skills Demonstrated

- **AI / LLM Integration** — Groq API with LLaMA 3.3 70B and LLaMA 4 Scout (vision)
- **Multimodal AI** — Reading and interpreting images and documents using vision models
- **Full-Stack Python Development** — End-to-end app built with Streamlit
- **REST API Integration** — OpenStreetMap Overpass API and Nominatim for location search
- **Document Processing** — Handling PDF, DOCX, TXT, and image uploads in memory
- **Session State Management** — Multi-conversation history using Streamlit session state
- **UI / UX Design** — Custom dark-theme CSS with responsive card layout and chat bubbles
- **Prompt Engineering** — Structured AI prompts for medical summaries, symptom checks, and document analysis
- **Environment & Security** — Secure API key handling with `.env` and Streamlit Secrets

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Dhammadeep Ramteke**

[![GitHub](https://img.shields.io/badge/GitHub-DHAMMADEEPRAMTEKE30-black?style=flat&logo=github)](https://github.com/DHAMMADEEPRAMTEKE30)

---

## 📄 License

This project is licensed under the MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ using Groq + LLaMA + Streamlit**

⭐ If you found this useful, please star the repository!

[🚀 Try the Live App](https://medicare-ai.streamlit.app/)

</div>

## 👤 Author

**Dhammadeep Anil Ramteke**

- 💼 LinkedIn: https://www.linkedin.com/in/dhammadeep-ramteke/
- 🐙 GitHub: https://github.com/DHAMMADEEPRAMTEKE30
- 📧 Email: ramtekedhamma30@gmail.com / dhammadeepramteke2702@gmail.com

---
