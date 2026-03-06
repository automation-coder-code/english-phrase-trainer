import streamlit as st
from groq import Groq

# 1. Configuração de UX (Design Colorido e Minimalista)
st.set_page_config(page_title="English Phrase Trainer", page_icon="📖", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 2px solid #007bff; }
    .stButton>button { border-radius: 20px; background-color: #007bff; color: white; height: 3.5em; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave de API não configurada nos Secrets do Streamlit.")
    st.stop()

st.title("📖 English Phrase Trainer")
st.caption("Foco em padrões de frases e pronúncia aproximada real")

tab1, tab2 = st.tabs(["🔍 Tradutor & Análise", "📝 Prática"])

# --- ABA 1: TRADUTOR ---
with tab1:
    texto = st.text_area("Digite a frase para estudar:", placeholder="Ex: I go to the beach...", label_visibility="collapsed")
    
    if st.button("Analisar para Estudo"):
        if texto:
            with st.spinner('Decompondo a frase...'):
                try:
                    # Prompt reforçado para manter o padrão e fonética real
                    prompt = f"""Analise a frase: '{texto}'
                    Responda em PORTUGUÊS com este formato exato:
                    
                    TRADUÇÃO: (tradução natural)
                    
                    FONÉTICA: (Como se pronuncia com sons do português. Ex: 'Go' = 'Gôu', 'Beach' = 'Bitch'. NUNCA termine com vogal extra se a palavra for seca).
                    
                    ANATOMIA: (Explique o que cada palavra faz na frase).
                    
                    5 EXEMPLOS EM INGLÊS: (Crie 5 novas frases OBRIGATORIAMENTE EM INGLÊS que usem o MESMO padrão da frase '{texto}'. Se a frase usa 'I go', todos os exemplos devem começar com 'I go'. Inclua Tradução e Fonética para cada um)."""
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor de inglês nativo. Seu objetivo é ensinar padrões de frases. Se o aluno escrever um padrão, mantenha esse padrão nos exemplos. Use fonética transcrita para brasileiros (ex: 'I' = 'Ai')."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.1
                    )
                    
                    res = completion.choices[0].message.content
                    st.markdown("---")
                    
                    # Divisão visual por blocos de cores
                    if "FONÉTICA:" in res and "ANATOMIA:" in res and "5 EXEMPLOS EM INGLÊS:" in res:
                        st.success(f"### 🏁 Tradução\n{res.split('FONÉTICA:')[0].replace('TRADUÇÃO:', '').strip()}")
                        st.info(f"### 🧩 Pronúncia e Estrutura\n{res.split('5 EXEMPLOS EM INGLÊS:')[0].split('FONÉTICA:')[1]}")
                        st.warning(f"### 💡 5 Exemplos com o mesmo padrão\n{res.split('5 EXEMPLOS EM INGLÊS:')[1]}")
                    else:
                        st.markdown(res)
                    
                except Exception as e:
                    st.error("Erro na API. Verifique o modelo ou a chave.")
        else:
            st.warning("Digite uma frase primeiro.")

# --- ABA 2: DESAFIOS ---
with tab2:
    st.header("🚀 Desafio")
    st.markdown("**Traduza: 'Eu vou à praia'**")
    res_user = st.text_input("Sua resposta:", key="beach_test")
    if st.button("Validar"):
        if "i go to the beach" in res_user.lower().strip():
            st.success("Correto! Pronúncia: 'Ai gôu tu dâ bitch'")
            st.balloons()
        else:
            st.info("Dica: Use 'I go to the beach'.")
