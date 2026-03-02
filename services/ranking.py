import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


def rank_candidates(candidates, clean_jd, embeddings, min_exp):

    docs = [
        Document(
            page_content=f"Experience: {c.years_of_experience}. Skills: {', '.join(c.skills)}. {c.summary}",
            metadata={"name": c.name},
        )
        for c in candidates
    ]

    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")

    vector_db = Chroma.from_documents(docs, embeddings)

    search_results = vector_db.similarity_search_with_score(
        clean_jd, k=len(candidates)
    )

    final_ranking = []

    for doc, v_score in search_results:
        cand = next(c for c in candidates if c.name == doc.metadata["name"])

        vector_pct = max(0, min(100, int((1 - (v_score / 1.5)) * 100)))
        llm_pct = cand.relevance_score * 10

        combined_score = (vector_pct + llm_pct) / 2

        if cand.years_of_experience < min_exp:
            combined_score -= 15

        final_ranking.append({
            "cand": cand,
            "score": max(0, min(100, combined_score))
        })

    return sorted(final_ranking, key=lambda x: x["score"], reverse=True)