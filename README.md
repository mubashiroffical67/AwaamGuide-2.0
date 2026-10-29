# 🇵🇰 AwaamGuide (عوام گائیڈ) 2.0
> **An Open-Source, Voice & Multimodal Civic Intelligence Navigator Powered by Google Gemma**

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-blueviolet?style=for-the-badge)](https://mlh.com)
[![Model](https://img.shields.io/badge/Model-Google%20Gemma%202%20%7C%20PaliGemma-orange?style=for-the-badge)](https://huggingface.co/google/gemma-2-2b-it)
[![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge)](LICENSE)
[![Framework](https://img.shields.io/badge/Built%20With-Streamlit%20%7C%20Ollama-red?style=for-the-badge)](https://streamlit.io)

---

## 📌 Problem & Inspiration
Millions of citizens across Pakistan are eligible for interest-free micro-loans (PM Youth Loan), healthcare subsidies (Sehat Card), housing grants, and financial welfare (BISP). However, they miss out because government circulars are published in dense bureaucratic English or standard formal text.

Furthermore, linguistic and literacy diversity means many citizens speak regional languages like **Pashto, Sindhi, Punjabi, Saraiki, or Balochi**, and struggle to decode complex paperwork. **AwaamGuide (عوام گائیڈ)** transforms **Google Gemma** into an empathetic, regional civic companion that can listen, talk, inspect physical documents, and guide citizens in their mother tongue.

---

## 🏆 Prize Category Alignment

1. **Best Use of Gemma:**[cite: 1]
   - **Multimodal Experience:** Incorporates visual document inspection for utility bills, rejection letters, and NADRA receipts alongside conversational generation[cite: 1].
   - **Community Focused:** Solves critical civic access problems for underserved, multilingual populations[cite: 1].
   - **Rapid Prototyping:** Powered by lightweight open weights (`gemma2:2b` via Ollama or Hugging Face Inference API)[cite: 1].

2. **Best Open-Source AI Project (DigitalOcean):**[cite: 1]
   - Built 100% on open weights (Google Gemma), open-source Python frameworks (Streamlit), and free tooling with zero proprietary model dependencies[cite: 1].

---

## ✨ Features

- 🎙️ **Voice-First Input:** Speak inquiries directly using the native browser microphone.
- 🌐 **8 Regional Dialects:** Native script reasoning for **Sindhi (سنڌي)**, **Pashto (پښتو)**, **Punjabi (پنجابی)**, **Saraiki (سرائیکی)**, **Balochi (بلوچی)**, **Roman Urdu**, **Urdu**, and **English**.
- 📸 **Multimodal Document Scanner:** Upload photos of utility bills to extract consumer numbers and verify scheme eligibility criteria[cite: 1].
- 🔊 **Voice Audio Playback (TTS):** Synthesizes guidance aloud for non-literate citizens.
- 🧮 **Interactive Loan Calculator:** Real-time 0% to 7% tier calculation, age verification, and monthly payment estimates.
- ✍️ **Petition & Grievance Drafter:** Formats and outputs downloadable legal representation letters addressed to Deputy Commissioners and bank managers.
- 📱 **Offline USSD Shortcodes:** Built-in offline cards for national SMS verification codes (8171, 8500, 9966, 8009).

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11 (64-bit)
- [Ollama](https://ollama.com/) installed

### 1. Clone & Set Up Virtual Environment
```powershell
git clone [https://github.com/YOUR_USERNAME/awaam-guide.git](https://github.com/YOUR_USERNAME/awaam-guide.git)
cd awaam-guide
py -3.11 -m venv venv
.\venv\Scripts\activate
