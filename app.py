import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="English Phrase Trainer", page_icon="🇬🇧")

# Inicialização segura da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave GROQ_API_KEY não configurada nos Secrets do Streamlit.")
    st.stop()

st.title("🇬🇧 English Phrase Trainer")

# Abas de navegação
tab1, tab2 = st.tabs(["🔍 Tradutor & 5 Exemplos", "👨‍🏫 Treino Básico"])

with tab1:
    st.header("Tradutor Inteligente")
    texto = st.text_area("Digite sua frase em PT ou EN:", key="txt_trad")
    
    if texto:
        with st.spinner('Analisando...'):
            prompt = f"Traduza e analise: '{texto}'. Forneça a tradução, explique erros gramaticais em português e dê 5 exemplos curtos de uso em inglês com tradução."
            
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            st.markdown("---")
            st.markdown(completion.choices[0].message.content)

with tab2:
    st.header("Treino Iniciante")
    st.info("Vamos praticar o que você usa no trabalho!")
    st.markdown("**Desafio:** Como se diz 'Eu sou um analista de processos' em inglês?")
    
    res = st.text_input("Sua resposta:", key="txt_treino")
    if st.button("Validar"):
        if "i am a process analyst" in res.lower().strip():
            st.balloons()
            st.success("Correct! 🎉")
        else:
            st.warning("Tente: 'I am a process analyst'.")
