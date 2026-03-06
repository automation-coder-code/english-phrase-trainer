import streamlit as st
from groq import Groq

# 1. Configuração de UX (Design que você gostou)
st.set_page_config(page_title="English Phrase Trainer", page_icon="📖", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 1px solid #007bff; }
    .stButton>button { border-radius: 20px; background-color: #007bff; color: white; height: 3.5em; width: 100%; font-weight: bold; }
    /* Estilo para as caixas de resultado */
    .res-box { padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid; }
    .blue-box { background-color: #eef6ff; border-left-color: #007bff; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Adicione a chave nos Secrets do Streamlit.")
    st.stop()

st.title("📖 English Phrase Trainer")
st.caption("Focado em Estudo Pessoal e Fonética Correta")

tab1, tab2 = st.tabs(["🔍 Tradutor & Análise", "📝 Desafios"])

# --- ABA 1: TRADUTOR ---
with tab1:
    texto = st.text_area("Digite a frase para estudar:", placeholder="Ex: I go to school...", label_visibility="collapsed")
    
    if st.button("Analisar para Estudo"):
        if texto:
            with st.spinner('Analisando...'):
                try:
                    # Prompt Simplificado para não bugar a resposta
                    prompt = f"""Analise a frase: '{texto}'
                    Responda em PORTUGUÊS seguindo exatamente esta ordem:
                    
                    TRADUÇÃO: (tradução natural)
                    
                    FONÉTICA: (Como um brasileiro lê. Ex: 'School' é 'Skul', não 'Skola'. 'I' é 'Ai'. Não coloque 'i' no final de palavras que terminam em consoante).
                    
                    ANATOMIA: (Liste cada palavra e o que ela faz na frase: sujeito, verbo, objeto, etc).
                    
                    EXEMPLOS: (Traga 5 frases curtas usando o contexto com tradução e fonética)."""
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor de inglês didático. Responda de forma curta e organizada."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.2
                    )
                    
                    resposta = completion.choices[0].message.content
                    
                    st.markdown("---")
                    
                    # Organização por Caixas Coloridas
                    st.success(f"### 🏁 Tradução\n{resposta.split('FONÉTICA:')[0].replace('TRADUÇÃO:', '')}")
                    
                    st.info(f"### 🧩 Pronúncia e Estrutura\n{resposta.split('EXEMPLOS:')[0].split('FONÉTICA:')[1]}")
                    
                    st.warning(f"### 💡 5 Exemplos Extras\n{resposta.split('EXEMPLOS:')[-1]}")
                    
                except Exception as e:
                    st.error("Erro ao processar. Tente novamente.")
        else:
            st.warning("Digite uma frase primeiro!")

# --- ABA 2: DESAFIOS ---
with tab2:
    st.header("🚀 Prática")
    st.markdown("**Como se diz 'Eu estudo todos os dias' em inglês?**")
    res_user = st.text_input("Sua resposta:", key="study_day")
    if st.button("Verificar"):
        if "i study every day" in res_user.lower().strip():
            st.balloons()
            st.success("Correto! Fonética: 'Ai stâdi évri dei'")
        else:
            st.info("Dica: Use 'I study every day'.")

st.markdown("---")
st.caption("Keep studying! 🚀")
