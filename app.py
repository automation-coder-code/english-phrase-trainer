import streamlit as st
from groq import Groq

# Configuração da Página - Deve ser o primeiro comando Streamlit
st.set_page_config(page_title="English Phrase Trainer", page_icon="🇬🇧", layout="centered")

# Inicialização Segura do Cliente Groq
try:
    # Busca a chave nos Secrets do Streamlit (Configurações > Secrets)
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro de Configuração: A chave 'GROQ_API_KEY' não foi encontrada nos Secrets do Streamlit.")
    st.info("Para resolver: Vá em Settings > Secrets no Streamlit Cloud e adicione: GROQ_API_KEY = 'sua_chave_aqui'")
    st.stop()

st.title("🇬🇧 English Phrase Trainer")

# Criação das Abas
tab1, tab2 = st.tabs(["🔍 Tradutor & Análise", "👨‍🏫 Treinamento Iniciante"])

# --- ABA 1: TRADUTOR DINÂMICO ---
with tab1:
    st.header("Tradutor Inteligente")
    st.write("Digite abaixo para traduzir, corrigir e ver exemplos.")
    
    texto_usuario = st.text_area("Texto (Português ou Inglês):", placeholder="Ex: Eu gosto de analisar processos...", key="input_tradutor")

    if texto_usuario:
        with st.spinner('O cérebro da IA está pensando...'):
            prompt = f"""
            Atue como um professor de inglês. Analise: '{texto_usuario}'
            
            Responda em PORTUGUÊS seguindo este fluxo:
            1. Tradução exata para o outro idioma.
            2. Se a frase
