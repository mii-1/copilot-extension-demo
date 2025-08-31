import os
import streamlit as st
from dotenv import load_dotenv
from connector_mock import search_contracts

# --- LLM helpers (OpenAI or Azure OpenAI) ---
def get_llm_client():
    from openai import OpenAI, AzureOpenAI
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
        return AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-06-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        ), os.getenv("AZURE_OPENAI_DEPLOYMENT") or "gpt-4o-mini"
    else:
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY")), "gpt-4o-mini"

def llm_answer(model_client, model_name, prompt):
    resp = model_client.chat.completions.create(
        model=model_name,
        messages=[{"role":"system","content":"You are a helpful enterprise Copilot."},
                  {"role":"user","content":prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

# --- UI ---
load_dotenv()
st.title("🔎 Copilot Agent Demo (Contracts)")

q = st.text_input("Ask about contracts (e.g., 'Contoso renewal date')")
if st.button("Search & Answer") or (q and st.session_state.get("auto_run") is True):
    found = search_contracts(q)[:3]
    if not found:
        st.warning("No matching contracts found.")
    else:
        st.subheader("Matched Contracts")
        st.json(found)

        # Build context
        ctx = "\n".join(
            [f"Vendor: {c['vendor']}\nContract: {c['contract_id']}\nRenewal: {c['renewal_date']}\nSummary: {c['summary']}"
             for c in found]
        )
        prompt = f"Context:\n{ctx}\n\nQuestion: {q}\nAnswer briefly with dates and reasoning."
        try:
            client, model = get_llm_client()
            answer = llm_answer(client, model, prompt)
            st.success(answer)
        except Exception as e:
            st.error(f"LLM call failed: {e}")
            st.info("You can still use the mock search results above.")

