import streamlit as st
from groq import Groq

# Configuração da Página
st.set_page_config(page_title="English Phrase Trainer", page_icon="🇬🇧", layout="centered")

# Inicialização do Cliente com tratamento de erro e indentação correta
try:
    # O comando abaixo deve estar recuado (com 4 espaços ou 1 TAB)
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave GROQ_API_KEY não configurada nos Secrets do Streamlit.")
    st.stop()

st.title("🇬🇧 English Phrase Trainer")

# Abas do Aplicativo
tab1, tab2 = st.tabs(["🔍 Tradutor & Exemplos", "👨‍🏫 Treinamento Base"])

# --- ABA 1: TRADUTOR ---
with tab1:
    st.header("Tradutor Inteligente")
    texto_usuario = st.text_area("Digite em PT ou EN:", key="input_tradutor")

    if texto_usuario:
        with st.spinner('Analisando...'):
            # Prompt estruturado para evitar erro de aspas triplas
            prompt_content = (
                f"Analise a frase: '{texto_usuario}'. "
                "Retorne em Português: a tradução, se há erros gramaticais e "
                "exatamente 5 exemplos curtos de uso em inglês com tradução."
            )
            
            try:
                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_content}],
                    model="llama3-8b-8192",
                    temperature=0.5
                )
                st.markdown("---")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Erro na API: {e}")

# --- ABA 2: TREINAMENTO ---
with tab2:
    st.header("Treino Iniciante")
    st.info("Pratique frases do dia a dia.")
    
    st.markdown("**Desafio:** Como se diz 'Eu sou um analista de processos' em inglês?")
    resposta = st.text_input("Sua resposta:", key="input_treino")
    
    if st.button("Validar"):
        if "i am a process analyst" in resposta.lower().strip():
            st.balloons()
            st.success("Correto! 🎉")
        else:
            st.warning("Tente: 'I am a process analyst'.")
