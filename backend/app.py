import os
import json
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from pypdf import PdfReader
from groq import Groq
from report_generator import generate_report

# Load .env file if it exists (optional dependency)
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass  # python-dotenv not installed — rely on system environment variables

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise EnvironmentError(
        "\n\n❌  GROQ_API_KEY not found!\n"
        "   Set it in a .env file at the project root:\n"
        "   GROQ_API_KEY=your_key_here\n"
        "   Get a free key at: https://console.groq.com\n"
    )

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

client = Groq(api_key=GROQ_API_KEY)

# ── Serve Frontend ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ── PDF Text Extraction ───────────────────────────────────────────────────────
def extract_text_from_pdf(file_storage) -> str:
    reader = PdfReader(file_storage)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


# ── Groq Analysis ─────────────────────────────────────────────────────────────
def analyze_with_groq(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    You are an advanced Applicant Tracking System (ATS) optimization expert.
    Analyze the following resume text against the provided job description.

    Provide your analysis strictly in a valid JSON format with the following exact keys:
    - "score": an integer from 0 to 100
    - "matched_skills": a list of strings (skills found in both resume and JD)
    - "missing_skills": a list of strings (skills in JD but missing from resume)
    - "feedback": a concise paragraph with specific, actionable optimization advice.

    Do not include markdown blocks or conversational text. Return only raw JSON.

    Resume Text:
    {resume_text}

    Job Description:
    {job_description}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return json.loads(completion.choices[0].message.content.strip())


# ── Analyze Endpoint ──────────────────────────────────────────────────────────
@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded."}), 400

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if not resume_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported."}), 400

    if not job_description:
        return jsonify({"error": "Job description is required."}), 400

    try:
        resume_text = extract_text_from_pdf(resume_file)
    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 422

    if not resume_text:
        return jsonify({"error": "Could not extract text. Please upload a text-based (non-scanned) PDF."}), 422

    try:
        result = analyze_with_groq(resume_text, job_description)
    except Exception as e:
        return jsonify({"error": f"AI analysis failed: {str(e)}"}), 500

    # Attach filename for the PDF report
    result["filename"] = resume_file.filename

    # Cache analysis in result for /download endpoint
    # Store in app context temporarily using a simple in-memory store
    app.config["LAST_RESULT"] = result

    return jsonify(result)


# ── Download PDF Report Endpoint ──────────────────────────────────────────────
@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided."}), 400

    try:
        pdf_bytes = generate_report(
            score=data.get("score", 0),
            feedback=data.get("feedback", ""),
            matched_skills=data.get("matched_skills", []),
            missing_skills=data.get("missing_skills", []),
            filename=data.get("filename", "Resume"),
        )
    except Exception as e:
        return jsonify({"error": f"Report generation failed: {str(e)}"}), 500

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=ats_analysis_report.pdf",
            "Content-Length": str(len(pdf_bytes)),
        },
    )


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
