import streamlit as st
from pypdf import PdfReader
from groq import Groq
import json

client = Groq()

st.set_page_config(page_title="AI Resume Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; color: #f1f5f9 !important; }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-left: 6px solid #3b82f6;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .metric-val { font-size: 3rem; font-weight: 800; color: #3b82f6; margin: 5px 0; }
    .metric-lbl { text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.85rem; color: #94a3b8; }
    
    .badge-match {
        display: inline-block; background-color: rgba(16, 185, 129, 0.15); 
        color: #10b981; border: 1px solid #10b981;
        padding: 6px 12px; border-radius: 20px; margin: 4px; font-weight: 500; font-size: 0.85rem;
    }
    .badge-miss {
        display: inline-block; background-color: rgba(239, 68, 68, 0.15); 
        color: #ef4444; border: 1px solid #ef4444;
        padding: 6px 12px; border-radius: 20px; margin: 4px; font-weight: 500; font-size: 0.85rem;
    }
    
    div[data-testid="stTextArea"] textarea { background-color: #1e293b !important; color: #f1f5f9 !important; border: 1px solid #334155 !important; }
    div[data-testid="stFileUploader"] { background-color: #1e293b !important; border: 2px dashed #334155 !important; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text: extracted_text += text + "\n"
    return extracted_text

def analyze_with_groq(resume_text, job_description):
    prompt = f"""
    You are an advanced Applicant Tracking System (ATS) optimization expert. 
    Analyze the following resume text against the provided job description.
    
    Provide your analysis strictly in a valid JSON format with the following exact keys:
    - "score": an integer from 0 to 100
    - "matched_skills": a list of strings
    - "missing_skills": a list of strings
    - "feedback": a concise summary paragraph with actionable optimization advice.
    
    Do not include markdown blocks or conversational text. Return only raw JSON.

    Resume Text: {resume_text}
    Job Description: {job_description}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-specdec",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content.strip())

st.title("⚡ AI Resume Intelligence Dashboard")
st.caption("Enterprise-grade profile scanner powered by high-speed local stream pipelines.")
st.write("---")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown(" 📥 Document Upload & Context")
    uploaded_file = st.file_uploader("Upload Profile Data (PDF Format)", type=["pdf"], label_visibility="collapsed")
    
    st.markdown(" 🎯 Target Job Specifications")
    job_description = st.text_area("Paste the job profile configuration parameters here...", height=300, label_visibility="collapsed")
    
    submit_button = st.button("Execute Profile Analysis Pipeline", type="primary", use_container_width=True)

with col2:
    st.markdown(" 📊 Metrics Engine Analytics")
    
    if submit_button and uploaded_file and job_description:
        try:
            with st.spinner("Parsing operational streams..."):
                resume_text = extract_text_from_pdf(uploaded_file)
            
            if not resume_text.strip():
                st.error("Execution Interrupted: Unreadable or scanned asset metadata profile.")
                st.stop()
                
            with st.spinner("Compiling cross-reference intelligence matrices..."):
                analysis_results = analyze_with_groq(resume_text, job_description)
            
            score = analysis_results.get("score", 0)
            feedback = analysis_results.get("feedback", "No operational feedback parsed.")
            matched = analysis_results.get("matched_skills", [])
            missing = analysis_results.get("missing_skills", [])
            
            accent_color = "#10b981" if score >= 75 else ("#f59e0b" if score >= 50 else "#ef4444")
            
            st.markdown(f"""
                <div class="metric-card" style="border-left-color: {accent_color}">
                    <div class="metric-lbl">Overall Profile Match Optimization Index</div>
                    <div class="metric-val" style="color: {accent_color}">{score}%</div>
                    <div class="metric-lbl">ATS System Threshold Metric</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(" 💡 Structural Strategy Roadmap")
                st.info(feedback)
            
            st.write(" ")
            
            sk_col1, sk_col2 = st.columns(2)
            with sk_col1:
                st.markdown(" ✅ Matched Capabilities")
                if matched:
                    badges_html = "".join([f'<span class="badge-match">{skill}</span>' for skill in matched])
                    st.markdown(badges_html, unsafe_allow_html=True)
                else:
                    st.caption("No semantic overlap keywords isolated.")
                    
            with sk_col2:
                st.markdown("❌ Critical Skill Gaps")
                if missing:
                    badges_html = "".join([f'<span class="badge-miss">{skill}</span>' for skill in missing])
                    st.markdown(badges_html, unsafe_allow_html=True)
                else:
                    st.caption("Perfect structural keyword index alignment mapped.")
                    
        except Exception as e:
            st.error(f"Pipeline Execution Aborted: {str(e)}")
    else:
        st.info("System Ready: Initialize document streaming matrices to populate analytical indicators.")