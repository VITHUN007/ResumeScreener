from langchain_google_genai import ChatGoogleGenerativeAI
from utils.helper import extract_text_from_response
from config.settings import api_key

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0
    )


def get_clean_jd_requirements(jd_text, llm):
    prompt = f"""
    Extract ONLY:
    - Technical skills
    - Required tools
    - Minimum years of experience

    Return in short bullet format.

    Job Description:
    {jd_text}
    """
    response = llm.invoke(prompt)
    return extract_text_from_response(response.content)