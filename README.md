# 🏥 MediCare AI — Your Personal Health Companion

An AI-powered medical assistant built with **Streamlit** and **Groq (LLaMA 3)**.

## ✨ Features

| Feature | Description |
|---|---|
| 💬 AI Health Chat | Ask any health question with full conversation memory |
| 🔍 Symptom Checker | Describe symptoms → get AI-powered assessment |
| 📋 Prescription Reader | Upload prescription → AI explains every medicine |
| 🧪 Lab Report Analyser | Upload lab report → plain-language explanation |
| 💊 Medicine Info | Search any medicine for uses, dosage, side effects |
| 🏥 Find Nearby Care | Find hospitals, clinics, pharmacies near you |
| 💬 Follow-up Chat | Ask questions about your prescription or report |

## 🚀 Run Locally

1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/medicare-ai.git
cd medicare-ai
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
```
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the app
```bash
streamlit run app.py
```

## ⚙️ Deployment

Deployed on **Streamlit Cloud**.  
Add `GROQ_API_KEY` in Streamlit Cloud → App Settings → Secrets.

## ⚠️ Disclaimer

This app provides general health information only.  
It is **not** a substitute for professional medical advice.  
Always consult a qualified healthcare provider for medical concerns.
