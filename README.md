<div align="center">

# 🏥 MediCare AI
### Your Personal AI-Powered Health Companion

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medicare-ai.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Groq](https://img.shields.io/badge/Powered%20by-Groq-orange?style=flat)
![LLaMA](https://img.shields.io/badge/Model-LLaMA%203.3%2070B-green?style=flat)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat)

**A full-stack AI medical assistant that helps normal people understand their health —**
**prescriptions, lab reports, symptoms, medicines and nearby care — all in one place.**

[🚀 Live App](https://medicare-ai.streamlit.app/) &nbsp;•&nbsp;
[📂 Repository](https://github.com/DHAMMADEEPRAMTEKE30/medicare-ai) &nbsp;•&nbsp;
[🐛 Report Bug](https://github.com/DHAMMADEEPRAMTEKE30/medicare-ai/issues)

---

</div>

## 📌 What is MediCare AI?

MediCare AI is a **one-stop health companion** designed for everyday people who want to understand their health better — without needing a medical degree. It combines the power of **Groq's ultra-fast inference** with **Meta's LLaMA 3.3 70B** language model to provide instant, accurate, and easy-to-understand health information.

Whether you have a prescription you can't read, a lab report full of confusing numbers, or symptoms you're worried about — MediCare AI explains everything in **plain, simple language.**

> ⚠️ **Disclaimer:** MediCare AI is for general health information only. It is not a substitute for professional medical advice. Always consult a qualified healthcare provider for medical concerns.

---

## ✨ Features

### 💬 AI Health Chat
Have a full conversation about any health topic. The AI remembers your entire conversation so follow-up questions are always answered in context — just like talking to a knowledgeable friend.

### 🔍 Symptom Checker
Describe your symptoms along with duration and severity. The AI gives you a structured assessment of possible causes, red flag warnings, and clear guidance on whether to see a doctor today or monitor at home.

### 📋 Prescription Reader
Upload any prescription — photo, PDF, DOCX, or TXT. The AI reads every medicine, explains what it is for in simple words, states the dosage, and flags important warnings. Then ask follow-up questions about your prescription in a dedicated chat.

### 🧪 Lab Report Analyser
Upload your blood test, thyroid report, lipid profile, or any other lab report. The AI explains every value, marks what is normal vs abnormal, and tells you what it means for your health — in language anyone can understand. Includes a follow-up chat for deeper questions.

### 💊 Medicine Info
Search any medicine by name and instantly get its uses, how it works, standard dosage, how to take it, common side effects, important warnings, and storage instructions.

### 🏥 Find Nearby Care
Find hospitals, clinics, pharmacies, diagnostic labs, dentists, and eye specialists near you. Supports both **live GPS location** and **manual address entry**. Results show name, address, timing, open/closed status, distance, and a direct Google Maps directions link — powered by OpenStreetMap (completely free, no API key needed).

### 💬 Follow-up Chat on Documents
After analysing a prescription or lab report, ask as many follow-up questions as you want. The AI remembers the full analysis and gives answers specific to your actual document.

---

## 🤖 AI Model & Technology

| Component | Technology |
|---|---|
| **AI Engine** | [Groq](https://groq.com) — ultra-fast LLM inference |
| **Language Model** | Meta LLaMA 3.3 70B Versatile (`llama-3.3-70b-versatile`) |
| **Vision Model** | Meta LLaMA 4 Scout 17B (`meta-llama/llama-4-scout-17b-16e-instruct`) |
| **Framework** | [Streamlit](https://streamlit.io) |
| **Maps & Location** | OpenStreetMap + Nominatim + Overpass API |
| **Language** | Python 3.10+ |

### Why Groq?
Groq uses custom **LPU (Language Processing Unit)** hardware that makes AI inference **10-20x faster** than traditional GPU-based APIs. This means responses appear in **1-2 seconds** instead of 10-15 seconds — making the chat feel instant and natural.

### Why LLaMA 3.3 70B?
LLaMA 3.3 70B is Meta's most capable open-weight model. At 70 billion parameters it delivers deep reasoning and nuanced understanding, excellent medical knowledge, clear structured responses, and strong multilingual ability.

### Why LLaMA 4 Scout for Vision?
LLaMA 4 Scout is used for prescription and lab report image analysis. It is a multimodal model capable of reading text from photos with high accuracy — making it ideal for reading handwritten or printed medical documents.

---

## 🏗️ Architecture

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

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A free [Groq API key](https://console.groq.com)

### 1. Clone the Repository
```bash
git clone https://github.com/DHAMMADEEPRAMTEKE30/medicare-ai.git
cd medicare-ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at: https://console.groq.com

### 5. Run the App
```bash
streamlit run app.py
```
The app will open at `http://localhost:8501`

---

## 📦 Dependencies

```
streamlit       — Web app framework
groq            — Groq AI API client
python-dotenv   — Environment variable management
pypdf           — PDF text extraction
python-docx     — Word document text extraction
requests        — HTTP requests for maps API
```

---

## ☁️ Deployment

This app is deployed on **Streamlit Cloud** — free hosting for Streamlit apps.

**Live App:** https://medicare-ai.streamlit.app/

### Deploy Your Own Copy

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

## 📁 Project Structure

```
medicare-ai/
├── app.py              # Main application — all features
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from git
└── README.md           # This file
```

---

## 🔒 Privacy & Security

- ✅ Your API key is stored securely in `.env` (locally) or Streamlit Secrets (deployed)
- ✅ `.env` is in `.gitignore` — never uploaded to GitHub
- ✅ No user data is stored or logged anywhere
- ✅ Uploaded documents are processed in memory only — never saved to disk
- ✅ All AI conversations exist only in the current session

---

## 🗺️ Roadmap

- [ ] Multi-language support (Hindi, Marathi, Tamil, etc.)
- [ ] Voice input for health questions
- [ ] Export prescription/report analysis as PDF
- [ ] Health history tracking across sessions
- [ ] Drug interaction checker
- [ ] BMI and health metrics calculator

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

**Built with ❤️ using Groq + LLaMA 3 + Streamlit**

⭐ If you found this useful, please star the repository!

[🚀 Try the Live App](https://medicare-ai.streamlit.app/)

</div>
