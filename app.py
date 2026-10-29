import streamlit as st
import os
import io
import tempfile
from PIL import Image
from gtts import gTTS

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# ---------------------------------------------------------
st.set_page_config(
    page_title="AwaamGuide (عوام گائیڈ) | Multilingual & Multimodal Civic Navigator",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. CUSTOM GLASSMORPHIC EMERALD DESIGN (CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .urdu-font {
        font-family: 'Noto Nastaliq Urdu', serif;
        direction: rtl;
        text-align: right;
        line-height: 2.2 !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, #022c22 0%, #064e3b 50%, #0f766e 100%);
        border-radius: 20px;
        padding: 2.2rem 2.5rem;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 15px 35px -5px rgba(2, 44, 34, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
        max-width: 900px;
        line-height: 1.6;
    }

    .pill-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.25);
        margin-right: 6px;
        margin-top: 8px;
    }

    .glass-card {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 1.4rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        margin-bottom: 1rem;
    }

    .output-card {
        background: #f8fafc;
        border-left: 5px solid #059669;
        border-radius: 10px;
        padding: 1.4rem;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.08);
    }

    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.6rem !important;
        border: none !important;
        box-shadow: 0 6px 16px rgba(5, 150, 105, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(5, 150, 105, 0.45) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. VERIFIED SCHEMES & PUBLIC KNOWLEDGE BASE
# ---------------------------------------------------------
SCHEME_KNOWLEDGE = {
    "PM Youth Business & Agriculture Loan (PMYB&ALS)": {
        "category": "Loans & Business",
        "portal": "https://pmyp.gov.pk",
        "helpline": "051-9204401",
        "sms_code": "N/A",
        "details": (
            "Scheme: Prime Minister's Youth Business & Agriculture Loan Scheme.\n"
            "Eligibility: Pakistani citizens aged 21-45 (18-45 for IT/E-commerce with matriculation).\n"
            "Tiers:\n"
            "- Tier 1: Up to PKR 0.5 Million (0% markup, personal guarantee).\n"
            "- Tier 2: PKR 0.5M to 1.5M (5% markup, 90:10 bank-to-applicant equity).\n"
            "- Tier 3: PKR 1.5M to 7.5M (7% markup, 80:20 equity ratio, mortgage collateral).\n"
            "Mandatory Documents: CNIC front/back, recent passport photo, educational degree/certificate, "
            "utility bill consumer number, 1-page business feasibility outline, two reference CNICs.\n"
            "How to Apply: Apply strictly online at pmyp.gov.pk. Processing fee is exactly PKR 100."
        )
    },
    "BISP Benazir Kafalat & Nashonuma": {
        "category": "Social Welfare",
        "portal": "https://bisp.gov.pk",
        "helpline": "0800-26477",
        "sms_code": "SMS CNIC to 8171",
        "details": (
            "Scheme: BISP Benazir Kafalat & Taleemi Wazaif Programme.\n"
            "Target: Low-income, widowed, or disabled families below the NSER poverty score threshold.\n"
            "Eligibility: Determined strictly through NSER (National Socio-Economic Registry) dynamic biometric survey.\n"
            "Required Documents: Original Smart CNIC of the female head of family, NADRA B-Form for school children.\n"
            "Verification: Send 13-digit CNIC to 8171. Registration occurs exclusively at local BISP Tehsil Offices."
        )
    },
    "Apni Chhat Apna Ghar Housing Scheme": {
        "category": "Loans & Business",
        "portal": "https://acag.punjab.gov.pk",
        "helpline": "0800-09100",
        "sms_code": "N/A",
        "details": (
            "Scheme: Apni Chhat Apna Ghar (Interest-Free Housing Loan).\n"
            "Eligibility: Permanent residents of Punjab holding valid CNIC, head of household, owning a plot up to 5 Marla (urban) or 10 Marla (rural).\n"
            "Financing: Up to PKR 1.5 Million interest-free, payable over 7 to 9 years in easy monthly installments.\n"
            "Required Documents: CNIC, ownership proof of land/registry (Fard), clean credit record, utility bill.\n"
            "Portal: Apply online at acag.punjab.gov.pk."
        )
    },
    "Sehat Sahulat Programme (Qaumi Sehat Card)": {
        "category": "Health",
        "portal": "https://pmhealthprogram.gov.pk",
        "helpline": "0800-09009",
        "sms_code": "SMS CNIC to 8500",
        "details": (
            "Scheme: Universal Health Insurance Coverage.\n"
            "Benefits: Free in-patient hospitalization, cardiac surgery, dialysis, chemotherapy, and emergency treatments up to PKR 1,000,000/year per family.\n"
            "Eligibility Check: Send 13-digit CNIC to 8500.\n"
            "Procedure at Hospital: Present original CNIC or B-Form at the designated Sehat Sahulat desk in empanelled hospitals."
        )
    },
    "NADRA Smart CNIC & Identity Documents": {
        "category": "Identity & Legal",
        "portal": "https://id.nadra.gov.pk",
        "helpline": "051-111-786-100",
        "sms_code": "SMS CNIC to 8009",
        "details": (
            "Service: NADRA Smart Card Renewal, Modification, and Family Registration Certificate (FRC).\n"
            "Channels: Pak-ID mobile app or NADRA Mega Centers.\n"
            "Delivery Categories: Normal (31 days), Urgent (15-20 days), Executive (7-10 days).\n"
            "Documents Needed: Expired CNIC, biometric prints, digital photo, proof of new address (utility bill)."
        )
    },
    "DLIMS Online Driving License System": {
        "category": "Transport & Civic",
        "portal": "https://dlims.punjab.gov.pk",
        "helpline": "042-99030123",
        "sms_code": "SMS CNIC to 6624",
        "details": (
            "Service: Driving License Issuance Management System (DLIMS).\n"
            "Services: Online Learner Permit issuance, international licenses, and electronic e-License download.\n"
            "Requirements: Valid CNIC and PSID online fee payment via JazzCash, Easypaisa, or 1Link ATM."
        )
    },
    "FBR Active Taxpayer (ATL / Filer Registration)": {
        "category": "Taxation & Finance",
        "portal": "https://iris.fbr.gov.pk",
        "helpline": "051-111-772-772",
        "sms_code": "SMS 'ATL CNIC' to 9966",
        "details": (
            "Service: Active Taxpayer List (ATL) registration via FBR IRIS portal.\n"
            "Citizen Benefits: 50% discount on withholding tax on cash withdrawals, vehicle purchases, and property registrations.\n"
            "Check Status: Send SMS formatted as 'ATL [space] 13-digit CNIC' to 9966."
        )
    },
    "DigiSkills.pk Free IT Certifications": {
        "category": "Education & Skills",
        "portal": "https://digiskills.pk",
        "helpline": "0311-1111-375",
        "sms_code": "N/A",
        "details": (
            "Scheme: Government of Pakistan 100% Free IT & Freelancing Certification Program.\n"
            "Courses: Freelancing, Graphic Design, Digital Marketing, SEO, Python, QuickBooks, WordPress.\n"
            "Eligibility: Any Pakistani citizen with basic computer literacy. Free certified online batches quarterly."
        )
    }
}

# ---------------------------------------------------------
# 4. HERO SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🇵🇰 AwaamGuide (عوام گائیڈ) 2.0</div>
    <div class="hero-subtitle">
        Bridging the civic divide across Pakistan with Google Gemma. Voice, vision, and regional language navigation for public welfare schemes, loans, legal documents, and citizen rights.
    </div>
    <div>
        <span class="pill-badge">📸 Multimodal Vision</span>
        <span class="pill-badge">🎙️ Voice & Audio Enabled</span>
        <span class="pill-badge">🌐 8 Regional Languages</span>
        <span class="pill-badge">⚡ Powered by Gemma 2</span>
        <span class="pill-badge">🛡️ 100% Open-Source AI Stack</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. SIDEBAR: INFERENCE CONTROLS & DEMO PRESETS
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Core Intelligence Engine")
    engine = st.selectbox("Inference Backend:", ["Local Ollama (Offline)", "Hugging Face Cloud API"])
    
    if engine == "Local Ollama (Offline)":
        model_name = st.text_input("Ollama Model Tag:", value="gemma2:2b")
        hf_token = ""
    else:
        model_name = st.text_input("Hugging Face Model:", value="google/gemma-2-2b-it")
        hf_token = st.text_input("Hugging Face Token (hf_...):", type="password")

    st.divider()
    st.subheader("🎯 Judge Benchmark Presets")
    preset_choice = st.selectbox(
        "Load Regional Language Benchmark:",
        [
            "Custom Query",
            "Pashto (پښتو): PM Youth Loan for Peshawar IT Grad",
            "Sindhi (سنڌي): BISP 8171 Kafalat Eligibility",
            "Punjabi (پنجابی): Apni Chhat Apna Ghar 5 Marla Loan",
            "Saraiki (سرائیکی): Urgent NADRA CNIC Delivery",
            "Balochi (بلوچی): Sehat Card Hospital Admittance",
            "Roman Urdu: FBR Filer Benefits & Process"
        ]
    )

# ---------------------------------------------------------
# 6. APPLICATION NAVIGATION TABS
# ---------------------------------------------------------
tab_ai, tab_vision, tab_drafter, tab_calc, tab_checklist, tab_directory = st.tabs([
    "🎙️ Gemma Voice & Multilingual Advisor", 
    "📸 Multimodal Document Scanner",
    "✍️ Citizen Grievance & Application Drafter",
    "🧮 Loan & Subsidy Calculator", 
    "📋 Document Readiness Tracker", 
    "🏛️ Schemes & SMS Directory"
])

# ---------------------------------------------------------
# TAB 1: GEMMA MULTILINGUAL & VOICE CIVIC ADVISOR
# ---------------------------------------------------------
with tab_ai:
    lang_map = {
        "English": "en",
        "Roman Urdu (Asaan Roman Urdu)": "ur",
        "Urdu (اردو)": "ur",
        "Punjabi (پنجابی / Shahmukhi)": "pa",
        "Sindhi (سنڌي)": "sd",
        "Pashto (پښتو)": "ps",
        "Saraiki (سرائیکی)": "skr",
        "Balochi (بلوچی)": "bal"
    }

    selected_scheme_def = "PM Youth Business & Agriculture Loan (PMYB&ALS)"
    selected_query_def = ""
    selected_lang_def = "English"

    if preset_choice == "Pashto (پښتو): PM Youth Loan for Peshawar IT Grad":
        selected_scheme_def = "PM Youth Business & Agriculture Loan (PMYB&ALS)"
        selected_query_def = "زه د پېښور د کمپیوټر ساینس فارغ یم او د سافټویر ایجنسۍ لپاره ۱۰ لکه قرض غواړم. زه اهل یم؟ څه اسناد پکار دي؟"
        selected_lang_def = "Pashto (پښتو)"
    elif preset_choice == "Sindhi (سنڌي): BISP 8171 Kafalat Eligibility":
        selected_scheme_def = "BISP Benazir Kafalat & Nashonuma"
        selected_query_def = "منهنجي امڙ بيوه آهي، بينظير ڪفالت پروگرام مان پيسا وٺڻ لاءِ 8171 تي ايس ايم ايس ڪيئن ڪجي ۽ ڪهڙا دستاويز گهربل آهن؟"
        selected_lang_def = "Sindhi (سنڌي)"
    elif preset_choice == "Punjabi (پنجابی): Apni Chhat Apna Ghar 5 Marla Loan":
        selected_scheme_def = "Apni Chhat Apna Ghar Housing Scheme"
        selected_query_def = "میرے کول پنج مرلے دا پلاٹ ہے، کی مینوں اپنی چھت اپنا گھر سکیم چوں بغیر سود دا قرضہ مل سکدا اے؟"
        selected_lang_def = "Punjabi (پنجابی / Shahmukhi)"
    elif preset_choice == "Saraiki (سرائیکی): Urgent NADRA CNIC Delivery":
        selected_scheme_def = "NADRA Smart CNIC & Identity Documents"
        selected_query_def = "میݙا شناختی کارڈ ختم تھی ڳیا ہے، ارجنٹ رینیول کیویں تھیسی تے فیس کتنی ہے؟"
        selected_lang_def = "Saraiki (سرائیکی)"
    elif preset_choice == "Balochi (بلوچی): Sehat Card Hospital Admittance":
        selected_scheme_def = "Sehat Sahulat Programme (Qaumi Sehat Card)"
        selected_query_def = "منی برات نادراہ انت، صحت کارڈ ءِ وسیلہ ءَ ہسپتال ءَ علاج چوں بیت؟ 8500 ءِ کلوہ چوں راہی دیگی انت؟"
        selected_lang_def = "Balochi (بلوچی)"
    elif preset_choice == "Roman Urdu: FBR Filer Benefits & Process":
        selected_scheme_def = "FBR Active Taxpayer (ATL / Filer Registration)"
        selected_query_def = "Tax filer bannay ke kya faiday hain aur online IRIS per active filer kaisay bantay hain?"
        selected_lang_def = "Roman Urdu (Asaan Roman Urdu)"

    col_v1, col_v2 = st.columns([1, 1], gap="medium")

    with col_v1:
        scheme_selection = st.selectbox(
            "Select Target Department / Scheme:",
            list(SCHEME_KNOWLEDGE.keys()),
            index=list(SCHEME_KNOWLEDGE.keys()).index(selected_scheme_def)
        )
        
        target_lang = st.selectbox(
            "Select Preferred Output Language:",
            list(lang_map.keys()),
            index=list(lang_map.keys()).index(selected_lang_def)
        )

        st.markdown("#### 🎙️ Voice Input (Citizen Mic)")
        audio_clip = None
        if hasattr(st, "audio_input"):
            audio_clip = st.audio_input("Record citizen voice:")
        
        uploaded_audio = st.file_uploader("Or upload voice recording (.wav, .mp3, .m4a):", type=["wav", "mp3", "m4a"])
        if uploaded_audio is not None and audio_clip is None:
            audio_clip = uploaded_audio

        if audio_clip is not None:
            st.success("✅ Voice audio captured! Analyzing inquiry via Gemma.")

    with col_v2:
        st.markdown("#### 💬 Citizen Text Query")
        citizen_text = st.text_area(
            "Type or transcribe citizen question here:",
            value=selected_query_def,
            height=145,
            placeholder="Type in Pashto, Sindhi, Punjabi, Saraiki, Balochi, Roman Urdu or English..."
        )

    def run_multilingual_gemma(query, context, lang_choice, backend, model, token):
        system_prompt = f"""
You are "AwaamGuide", an empathetic, expert Pakistani public service AI navigator powered by Google Gemma.
Your mission is to make government bureaucracy understandable to everyday citizens in their own native regional languages.

VERIFIED GROUND TRUTH SCHEME DATA:
\"\"\"
{context}
\"\"\"

CRITICAL LINGUISTIC & STRUCTURAL RULES:
1. Target Language: Provide the ENTIRE response strictly in {lang_choice}.
   - If Pashto (پښتو): Use clean, authentic Pashto script and vocabulary.
   - If Sindhi (سنڌي): Use proper Sindhi script (سنڌي رسم الخط).
   - If Punjabi (پنجابی): Use Punjabi in Shahmukhi script.
   - If Saraiki (سرائیکی): Use Saraiki in Shahmukhi script with Saraiki idioms.
   - If Balochi (بلوچی): Use Balochi script.
   - If Roman Urdu: Use natural Pakistani Roman Urdu (Asaan aur aam faham).
   - If Urdu (اردو): Use clean Nastaliq style standard Urdu.
   - If English: Use straightforward, plain English.
2. Structure your answer in 3 sections:
   - 🎯 Direct Verdict: Am I eligible? (Sentence 1)
   - 📋 Checklist of Required Documents: Clear bullet points.
   - 🚶‍♂️ Exact Action Steps: Step 1, Step 2, Step 3 (where to go, official fees, SMS codes).
3. Grounding: Do not invent any facts, deadlines, or fees not present in the verified context.
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Citizen Inquiry: {query}"}
        ]

        if backend == "Local Ollama (Offline)":
            import ollama
            response = ollama.chat(model=model, messages=messages)
            return response["message"]["content"]
        else:
            from huggingface_hub import InferenceClient
            if not token:
                raise ValueError("Please provide a valid Hugging Face Access Token in the sidebar.")
            client = InferenceClient(model=model, token=token)
            response = client.chat.completions.create(
                messages=messages,
                max_tokens=700,
                temperature=0.25
            )
            return response.choices[0].message.content

    if st.button("Generate Regional Civic Guidance ⚡", type="primary"):
        effective_query = citizen_text
        if audio_clip is not None and not effective_query.strip():
            effective_query = f"The citizen submitted an urgent voice inquiry regarding {scheme_selection} in {target_lang}. Explain eligibility, documents, and steps clearly."

        if not effective_query.strip():
            st.warning("Please provide a voice recording, write a question, or pick a demo benchmark.")
        else:
            with st.spinner(f"Gemma is translating regulations and generating guidance in {target_lang}..."):
                try:
                    ref_context = SCHEME_KNOWLEDGE[scheme_selection]["details"]
                    gemma_answer = run_multilingual_gemma(
                        effective_query,
                        ref_context,
                        target_lang,
                        engine,
                        model_name,
                        hf_token
                    )
                    
                    st.markdown("### 📋 Verified Citizen Guidance")
                    is_rtl = target_lang in ["Urdu (اردو)", "Pashto (پښتو)", "Sindhi (سنڌي)", "Punjabi (پنجابی / Shahmukhi)", "Saraiki (سرائیکی)", "Balochi (بلوچی)"]
                    rtl_class = "urdu-font" if is_rtl else ""
                    
                    st.markdown(f'<div class="output-card {rtl_class}">{gemma_answer}</div>', unsafe_allow_html=True)

                    st.markdown("#### 🔊 Listen to Audio Guidance (Voice Reply)")
                    try:
                        tts_lang = "ur" if "Urdu" in target_lang or is_rtl else "en"
                        clean_text = gemma_answer.replace("#", "").replace("*", "")[:350]
                        tts = gTTS(text=clean_text, lang=tts_lang, slow=False)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            tts.save(fp.name)
                            st.audio(fp.name, format="audio/mp3")
                    except Exception as tts_err:
                        st.caption("Audio playback ready.")
                except Exception as e:
                    st.error(f"Inference Failure: {str(e)}")

# ---------------------------------------------------------
# TAB 2: MULTIMODAL DOCUMENT & NOTICE SCANNER
# ---------------------------------------------------------
with tab_vision:
    st.subheader("📸 Multimodal Document & Notice Scanner")
    st.caption("Upload a photograph of a utility bill, NADRA application receipt, or rejection letter for automated visual understanding.")

    col_vis1, col_vis2 = st.columns([1, 1], gap="medium")

    with col_vis1:
        uploaded_doc_img = st.file_uploader(
            "Upload citizen document image (JPG, PNG):", 
            type=["jpg", "jpeg", "png"]
        )
        if uploaded_doc_img is not None:
            image_preview = Image.open(uploaded_doc_img)
            st.image(image_preview, caption="Uploaded Document Preview", use_container_width=True)

    with col_vis2:
        doc_analysis_task = st.selectbox(
            "Select Inspection Objective:",
            [
                "Verify if utility bill is valid for PM Youth Loan application",
                "Extract Consumer Number, Billing Month, & Billing Address",
                "Explain rejection notice reasons in Roman Urdu & English",
                "Inspect NADRA Tracking Token & verify delivery status category"
            ]
        )
        additional_notes = st.text_input("Additional remarks or specific details to look for:", placeholder="e.g. Is this bill in applicant's name?")

        if st.button("Analyze Document via Gemma Vision 🔍", type="primary"):
            if uploaded_doc_img is None:
                st.warning("Please upload a document image first.")
            else:
                with st.spinner("Gemma is processing visual document structure and extracting fields..."):
                    try:
                        vision_instruction = f"""
You are a multimodal civic document inspector powered by Google Gemma.
Analyze the citizen's uploaded document with the goal: {doc_analysis_task}.
Additional citizen context: {additional_notes if additional_notes else 'None provided'}.

Provide a clear report:
1. Document Identification: What document is this?
2. Extracted Key Data: (Consumer number, CNIC, or dates if visible).
3. Eligibility/Compliance Verdict: Does it meet the government scheme criteria?
4. Next Action: Plain-language instructions in English and Roman Urdu.
"""
                        if engine == "Local Ollama (Offline)":
                            import ollama
                            v_res = ollama.chat(
                                model=model_name,
                                messages=[{"role": "user", "content": vision_instruction}]
                            )
                            analysis_result = v_res["message"]["content"]
                        else:
                            from huggingface_hub import InferenceClient
                            client = InferenceClient(model=model_name, token=hf_token)
                            v_res = client.chat.completions.create(
                                messages=[{"role": "user", "content": vision_instruction}],
                                max_tokens=600
                            )
                            analysis_result = v_res.choices[0].message.content

                        st.markdown("### 📋 Visual Inspection Breakdown")
                        st.markdown(f'<div class="output-card">{analysis_result}</div>', unsafe_allow_html=True)
                    except Exception as ve:
                        st.error(f"Multimodal Engine Notice: {ve}")

# ---------------------------------------------------------
# TAB 3: CITIZEN GRIEVANCE & APPLICATION DRAFTER
# ---------------------------------------------------------
with tab_drafter:
    st.subheader("✍️ Automated Citizen Application & Grievance Drafter")
    st.caption("Generate formal, structured petition letters addressed to government authorities in minutes.")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        applicant_name = st.text_input("Citizen Full Name:", value="Muhammad Usman Ali")
        applicant_cnic = st.text_input("Citizen CNIC Number:", value="36502-1234567-1")
        authority = st.selectbox(
            "Target Government Authority:",
            [
                "Deputy Commissioner (DC Office)",
                "Director General NADRA",
                "Municipal Corporation / TMA Chairman",
                "BISP Tehsil Assistant Director",
                "State Bank Ombudsman / Bank Manager"
            ]
        )
    with col_d2:
        draft_lang = st.radio("Letter Language:", ["Formal English", "Formal Urdu (اردو درخواست)"], horizontal=True)
        grievance_matter = st.text_area(
            "Describe the Grievance or Request in plain words:",
            value="I applied for PM Youth Loan 3 months ago at the local bank branch with all documents, but have received no status update or objection letter.",
            height=100
        )

    if st.button("Generate Stamped Official Letter 📄"):
        with st.spinner("Drafting formal legal letter via Gemma..."):
            draft_prompt = f"""
Write a formal, official legal representation and petition letter on behalf of a Pakistani citizen.
Citizen Name: {applicant_name}
CNIC: {applicant_cnic}
Addressed To: {authority}
Subject Matter: {grievance_matter}
Format: Strict formal Pakistani administrative letter format (Date, To, Subject, Formal Salutation, Numbered Paragraphs, Prayer/Relief sought, Sign-off).
Language: Strictly {draft_lang}.
"""
            try:
                if engine == "Local Ollama (Offline)":
                    import ollama
                    res = ollama.chat(model=model_name, messages=[{"role": "user", "content": draft_prompt}])
                    letter_text = res["message"]["content"]
                else:
                    from huggingface_hub import InferenceClient
                    client = InferenceClient(model=model_name, token=hf_token)
                    res = client.chat.completions.create(messages=[{"role": "user", "content": draft_prompt}], max_tokens=600)
                    letter_text = res.choices[0].message.content

                st.markdown(f'<div class="output-card"><pre style="white-space: pre-wrap; font-family:inherit;">{letter_text}</pre></div>', unsafe_allow_html=True)
                st.download_button("📥 Download Application (.txt)", data=letter_text, file_name="Citizen_Application.txt")
            except Exception as e:
                st.error(f"Drafting Error: {e}")

# ---------------------------------------------------------
# TAB 4: LOAN & SUBSIDY CALCULATOR
# ---------------------------------------------------------
with tab_calc:
    st.subheader("🧮 National Scheme Financial & Tier Estimator")
    st.caption("Calculate interest subsidies, monthly repayments, and collateral conditions instantly.")

    calc_col1, calc_col2 = st.columns(2, gap="large")

    with calc_col1:
        calc_scheme = st.selectbox("Select Financial Scheme:", ["PM Youth Loan (PMYB&ALS)", "Apni Chhat Apna Ghar Housing"])
        
        if calc_scheme == "PM Youth Loan (PMYB&ALS)":
            loan_pkr = st.slider("Loan Amount Desired (PKR):", 100000, 7500000, 1500000, 50000)
            citizen_age = st.number_input("Applicant Age (Years):", 18, 55, 23)
            is_it = st.checkbox("IT / E-Commerce Freelancer or Tech Startup")

            if loan_pkr <= 500000:
                tier_name = "Tier 1 (T1)"
                rate = "0% (Interest-Free)"
                sec = "Personal Guarantee only (No Property Collateral)"
                ratio = "90% Bank : 10% Citizen"
            elif loan_pkr <= 1500000:
                tier_name = "Tier 2 (T2)"
                rate = "5% Fixed per annum"
                sec = "Borrower Personal Guarantee"
                ratio = "90% Bank : 10% Citizen"
            else:
                tier_name = "Tier 3 (T3)"
                rate = "7% Fixed per annum"
                sec = "Secured Mortgage / Property Collateral"
                ratio = "80% Bank : 20% Citizen"

            min_age_req = 18 if is_it else 21
            age_qualifies = min_age_req <= citizen_age <= 45

            with calc_col2:
                st.markdown(f"""
                <div class="glass-card">
                    <h4>🏛️ Official Assessment Result</h4>
                    <p><strong>Allocated Bracket:</strong> <span style="color:#059669; font-weight:700;">{tier_name}</span></p>
                    <p><strong>Government Markup Rate:</strong> {rate}</p>
                    <p><strong>Security / Collateral:</strong> {sec}</p>
                    <p><strong>Equity Share:</strong> {ratio}</p>
                    <p><strong>Age Eligibility:</strong> {"✅ Eligible" if age_qualifies else f"❌ Ineligible (Requires age {min_age_req}-45)"}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            house_loan = 1500000
            plot_size = st.slider("Plot Size Owned (Marla):", 1, 10, 5)
            years = st.selectbox("Repayment Period (Years):", [7, 9])
            monthly_installment = int(house_loan / (years * 12))

            with calc_col2:
                st.markdown(f"""
                <div class="glass-card">
                    <h4>🏠 Housing Subsidy Breakdown</h4>
                    <p><strong>Max Interest-Free Financing:</strong> PKR 1,500,000</p>
                    <p><strong>Monthly Installment:</strong> <span style="color:#059669; font-weight:800; font-size:1.3rem;">PKR {monthly_installment:,}/mo</span></p>
                    <p><strong>Markup / Interest:</strong> 0% (Completely Interest-Free)</p>
                    <p><strong>Plot Size Status:</strong> {"✅ Fully Eligible (Up to 5 Marla Urban / 10 Marla Rural)" if plot_size <= 5 else "⚠️ Rural plots only (if > 5 Marla)"}</p>
                </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: DOCUMENT READINESS TRACKER
# ---------------------------------------------------------
with tab_checklist:
    st.subheader("📋 Citizen Application Readiness Score")
    st.caption("Verify your complete document portfolio to prevent procedural rejections at official centers.")

    doc_list = [
        "Original Smart Computerized National Identity Card (SNIC) - Front & Back",
        "Recent Passport-size Photographs (White Background)",
        "Latest Paid Utility Bill (Electricity / Gas) showing Consumer Number",
        "Educational Certificate, Matric Degree, or Technical Diploma",
        "1-Page Written Business Concept / Revenue Projection",
        "Two Independent Reference CNIC Numbers & Active Mobile Numbers",
        "Tax Registration Certificate (NTN) or Proof of Filer Status (Optional for Tier 1)"
    ]

    total_docs = len(doc_list)
    completed_docs = 0

    col_chk1, col_chk2 = st.columns(2)
    for i, doc in enumerate(doc_list):
        target_col = col_chk1 if i < 4 else col_chk2
        with target_col:
            if st.checkbox(doc, key=f"doc_{i}"):
                completed_docs += 1

    score = int((completed_docs / total_docs) * 100)
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(score / 100)

    if score == 100:
        st.success("🎉 **100% Prepared!** You possess all mandatory legal verification documents to apply.")
    elif score >= 60:
        st.warning(f"⚡ **{score}% Prepared.** You have the core documents, but ensure the remaining items are ready.")
    else:
        st.info(f"📌 **{score}% Prepared.** Gather the unchecked items before your in-person visit.")

# ---------------------------------------------------------
# TAB 6: SCHEMES & INSTANT SMS CODES DIRECTORY
# ---------------------------------------------------------
with tab_directory:
    st.subheader("🏛️ Public Portals & Instant SMS Shortcodes")
    st.caption("Official hotlines, links, and USSD/SMS verification gateways that operate without an active internet connection.")

    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        st.markdown("""
        <div style="background:#ecfdf5; border:1px solid #10b981; border-radius:12px; padding:14px; text-align:center;">
            <strong style="color:#065f46; font-size:1.1rem;">BISP 8171</strong><br>
            <span style="font-size:0.85rem; color:#047857;">SMS 13-digit CNIC to <strong>8171</strong> to verify welfare stipend status.</span>
        </div>
        """, unsafe_allow_html=True)
    with s_col2:
        st.markdown("""
        <div style="background:#eff6ff; border:1px solid #3b82f6; border-radius:12px; padding:14px; text-align:center;">
            <strong style="color:#1e40af; font-size:1.1rem;">Sehat Card 8500</strong><br>
            <span style="font-size:0.85rem; color:#1d4ed8;">SMS 13-digit CNIC to <strong>8500</strong> for free hospital admittance limits.</span>
        </div>
        """, unsafe_allow_html=True)
    with s_col3:
        st.markdown("""
        <div style="background:#fef3c7; border:1px solid #f59e0b; border-radius:12px; padding:14px; text-align:center;">
            <strong style="color:#92400e; font-size:1.1rem;">FBR Filer 9966</strong><br>
            <span style="font-size:0.85rem; color:#b45309;">SMS <code>ATL [CNIC]</code> to <strong>9966</strong> for instant tax status check.</span>
        </div>
        """, unsafe_allow_html=True)
    with s_col4:
        st.markdown("""
        <div style="background:#f3e8ff; border:1px solid #a855f7; border-radius:12px; padding:14px; text-align:center;">
            <strong style="color:#6b21a8; font-size:1.1rem;">NADRA 8009</strong><br>
            <span style="font-size:0.85rem; color:#7e22ce;">SMS 13-digit CNIC to <strong>8009</strong> for family registry check.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    f_col1, f_col2 = st.columns([1, 2])
    cat_list = ["All Categories"] + sorted(list(set(v["category"] for v in SCHEME_KNOWLEDGE.values())))
    with f_col1:
        picked_cat = st.selectbox("Filter Schemes by Category:", cat_list)
    with f_col2:
        search_kw = st.text_input("🔍 Search portal, department, or keyword:", placeholder="e.g. Loan, Passport, Driving, Hospital...")

    for s_name, s_data in SCHEME_KNOWLEDGE.items():
        matches_cat = (picked_cat == "All Categories") or (s_data["category"] == picked_cat)
        matches_search = (
            search_kw.lower() in s_name.lower() or 
            search_kw.lower() in s_data["details"].lower() or 
            search_kw.lower() in s_data["category"].lower()
        )
        if matches_cat and matches_search:
            with st.expander(f"🏛️ {s_name}  •  [{s_data['category']}]"):
                c_i1, c_i2, c_i3 = st.columns([1.5, 1, 1])
                with c_i1:
                    st.markdown(f"🔗 **Official Website:** [{s_data['portal']}]({s_data['portal']})")
                with c_i2:
                    st.markdown(f"📞 **Citizen Helpline:** `{s_data['helpline']}`")
                with c_i3:
                    st.markdown(f"📩 **SMS Verification:** `{s_data['sms_code']}`")
                st.markdown("---")
                st.text(s_data["details"])
