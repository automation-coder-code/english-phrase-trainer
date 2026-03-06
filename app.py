import streamlit as st
from groq import Groq

# Configuração da Página
st.set_page_config(page_title="English Phrase Trainer", page_icon="🇬🇧", layout="centered")

# Inicialização do Cliente Groq usando Secrets (Segurança)
try:
    # Em vez de client = Groq(api_key="gsk_..."), use:
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Erro: A chave GROQ_API_KEY não foi encontrada nos Secrets do Streamlit.")
    st.stop()

st.title("🇬🇧 English Phrase Trainer")

# Criação das Abas
tab1, tab2 = st.tabs(["🔍 Tradução e Análise", "👨‍🏫 Treinamento Iniciante"])

# --- ABA 1: TRADUTOR DINÂMICO ---
with tab1:
    st.header("Tradutor e Verificador")
    st.write("Digite uma frase para receber a tradução, correção e exemplos de uso.")
    
    texto_usuario = st.text_area("Texto:", placeholder="Ex: Eu preciso melhorar os processos da empresa", key="input_tradutor")

    if texto_usuario:
        with st.spinner('Analisando frase...'):
            prompt = f"""
            Você é um assistente de ensino de inglês. Analise a seguinte entrada: '{texto_usuario}'
            Regras de resposta:
            1. Forneça a tradução exata para o Inglês (se for PT) ou Português (se for EN).
            2. Se houver erros gramaticais na frase original, explique-os de forma simples em PORTUGUÊS.
            3. Traga exatamente 5 exemplos de frases curtas em inglês usando a palavra principal ou o contexto da frase, com suas traduções.
            4. Não dê notas numéricas.
            5. Use emojis para destacar as seções.
            """
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                    temperature=0.5
                )
                st.markdown("---")
                st.markdown(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Erro na chamada da API: {e}")

# --- ABA 2: TREINAMENTO (BÁSICO) ---
with tab2:
    st.header("Treino: Primeiros Passos")
    st.info("Aqui vamos construir sua base no inglês, começando do zero. 💡")
    
    st.markdown("""
    ### Lição de Hoje: Apresentações Profissionais
    Como você é um **Analista de Processos**, vamos aprender a dizer seu cargo.
    
    **Vocabulário:**
    * *Process Analyst* = Analista de Processos
    * *I am* = Eu sou / Eu estou
    
    **Desafio:** Como você diria "Eu sou um analista de processos" em inglês?
    """)
    
    resposta_treino = st.text_input("Sua resposta:", key="input_treino")
    
    if st.button("Verificar"):
        # Lógica simples de verificação (pode ser expandida via IA também)
        correta = "i am a process analyst"
        if correta in resposta_treino.lower():
            st.balloons()
            st.success("Perfect! Você acertou! 🎉")
        else:
            st.warning("Quase lá! Tente: 'I am a process analyst'.")
