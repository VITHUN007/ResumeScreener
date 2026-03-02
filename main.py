import streamlit as st
from config.settings import api_key
from model.resumeschema import ResumeSchema
from services.llm import get_llm, get_clean_jd_requirements
from services.embeddings import load_embeddings
from services.uploadpdf import extract_text_from_pdfs
from services.ranking import rank_candidates
from utils.helper import safe_json_load

st.set_page_config(page_title="AI Resume Ranker Pro", layout="wide")

st.title("Smart Resume Ranker Pro")

col1, col2 = st.columns([1, 1])

with col1:
    job_desc = st.text_area("Job Description", height=250)
    min_exp = st.number_input(
        "Minimum Years of Experience Required",
        min_value=0,
        value=3
    )

with col2:
    uploaded_files = st.file_uploader(
        "Upload Resumes (PDF)",
        type="pdf",
        accept_multiple_files=True
    )

if st.button("Run Advanced Ranking") and uploaded_files and job_desc:

    llm = get_llm()
    candidates = []

    st.success(f"{len(uploaded_files)} resumes uploaded successfully.")

    with st.status("Processing...", expanded=True):

        clean_jd = get_clean_jd_requirements(job_desc, llm)

        for file in uploaded_files:

            resume_text = extract_text_from_pdfs(file)

            resume_text = resume_text[:12000]

            extraction_prompt = f"""
            Compare this resume against:

            REQUIREMENTS:
            {clean_jd}

            Return STRICT JSON format:
            {{
                "name": "string",
                "skills": ["list"],
                "years_of_experience": int,
                "summary": "short summary",
                "relevance_score": int (1-10),
                "reasoning": "short reason"
            }}

            Resume:
            {resume_text}
            """

            response = llm.invoke(extraction_prompt)
            parsed_json = safe_json_load(response.content)

            if parsed_json:
                candidates.append(ResumeSchema(**parsed_json))

        embeddings = load_embeddings()

        final_ranking = rank_candidates(
            candidates,
            clean_jd,
            embeddings,
            min_exp
        )


    st.subheader("Final Candidate Rankings")

    for entry in final_ranking:
        c = entry["cand"]
        score = entry["score"]

        with st.expander(f"{int(score)}% Match — {c.name}"):
            st.metric("Score", f"{int(score)}%")
            st.write(f"Experience: {c.years_of_experience} years")
            st.write(f"Reasoning: {c.reasoning}")
            st.write(f"Skills: {', '.join(c.skills[:8])}")
            st.progress(score / 100)

            