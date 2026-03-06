import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="English Phrase Trainer", page_icon="🇬🇧")

# Inicialização da API via Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Chave GROQ_API_KEY não encontrada nos Secrets.")
    st.stop()

st.title("🇬🇧 English Phrase Trainer")

tab1, tab2 = st.tabs(["🔍 Tradutor & 5 Exemplos", "👨‍🏫 Treino Básico"])

# --- ABA 1: TRADUTOR ---
with tab1:
    st.header("Tradutor Inteligente")
    texto = st.text_area("Digite sua frase em PT ou EN:", key="txt_trad")
    
    if texto:
        with st.spinner('Analisando...'):
            try:
                # Formatando a chamada de forma simples e direta
                completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "Você é um professor de inglês. Traduza a frase, explique a gramática em português e dê 5 exemplos curtos em inglês com tradução."
                        },
                        {
                            "role": "user", 
                            "content": texto
                        }
                    ],
                    model="llama3-8b-8192",
                )
                st.markdown("---")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Erro na análise: {e}")

# --- ABA 2: TREINO ---
with tab2:
    st.header("Treino Iniciante")
    st.info("Pratique termos do seu dia a dia profissional!")
    st.markdown("**Desafio:** Como se diz 'Eu sou um analista de processos' em inglês?")
    
    res = st.text_input("Sua resposta:", key="txt_treino")
    if st.button("Validar"):
        if "i am a process analyst" in res.lower().strip():
            st.balloons()
            st.success("Correct! 🎉")
        else:
            st.warning("Dica: Use 'I am a process analyst'.")
