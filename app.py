import streamlit as st
from groq import Groq

# 1. Configuração de UX Estudo Premium (Visual Colorido e Limpo)
st.set_page_config(page_title="English Phrase Trainer", page_icon="📖", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 1px solid #007bff; }
    .stButton>button { border-radius: 20px; background-color: #007bff; color: white; height: 3.5em; width: 100%; font-weight: bold; }
    .main-result { padding: 20px; border-radius: 15px; background-color: #f0f7ff; border-left: 6px solid #007bff; margin-top: 20px; }
    .word-analysis { background-color: #ffffff; padding: 10px; border-radius: 10px; border: 1px solid #d1e3ff; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave de API não configurada nos Secrets do Streamlit.")
    st.stop()

st.title("📖 English Phrase Trainer")
st.caption("Seu laboratório pessoal para estudo da língua inglesa")

tab1, tab2 = st.tabs(["🔍 Tradutor & Análise", "📝 Prática e Desafios"])

# --- ABA 1: TRADUTOR DETALHADO ---
with tab1:
    st.markdown("### ✍️ Digite a frase para estudar")
    texto = st.text_area("", placeholder="Ex: I am learning how to speak English...", label_visibility="collapsed", height=100)
    
    if st.button("Analisar Frase Completa"):
        if texto:
            with st.spinner('Decompondo a estrutura para seu estudo...'):
                try:
                    # Prompt focado em fonética, gramática e 5 exemplos para estudo
                    prompt_instrucao = (
                        f"Analise a frase: '{texto}'. "
                        "Responda em PORTUGUÊS seguindo exatamente esta estrutura organizada: "
                        "1. **Tradução Principal**: Tradução natural para o português. "
                        "2. **Fonética Prática**: Como se pronuncia cada palavra usando sons do português (Ex: You = Iu, English = Ínglish). "
                        "3. **Anatomia da Frase**: Liste cada palavra original, seu significado e sua função gramatical (sujeito, verbo, adjetivo, etc). "
                        "4. **5 Exemplos de Estudo**: Forneça 5 frases curtas diferentes usando a palavra principal ou o contexto, com Tradução e Fonética para cada uma."
                    )
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor particular de inglês focado em brasileiros. Seja extremamente organizado e didático."},
                            {"role": "user", "content": prompt_instrucao}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.3
                    )
                    
                    res_total = completion.choices[0].message.content
                    
                    st.markdown("---")
                    st.markdown("### 🎯 Resultado da Análise")
                    
                    # Seção 1: Tradução (Caixa Verde Sucesso)
                    st.success(f"**Tradução Principal:**\n\n{res_total.split('2.')[0].replace('1. **Tradução Principal**:', '').strip()}")
                    
                    # Seção 2 e 3: Fonética e Anatomia (Caixa Azul)
                    st.info("### 🧩 Pronúncia e Estrutura")
                    st.markdown(f"<div class='main-result'>{res_total.split('2.')[-1].split('4.')[0]}</div>", unsafe_allow_html=True)
                    
                    # Seção 4: 5 Exemplos (Caixa Amarela)
                    st.warning("### 💡 Mais 5 Exemplos para Praticar")
                    st.markdown(res_total.split('4.')[-1])
                    
                except Exception as e:
                    st.error(f"Erro na análise: {e}")
        else:
            st.warning("Por favor, insira um texto para começar.")

# --- ABA 2: DESAFIOS ---
with tab2:
    st.header("🚀 Desafio do Dia")
    st.write("Traduza a frase abaixo:")
    
    st.markdown("""
    <div style="background-color:#fff3cd; padding:20px; border-radius:10px; border-left: 6px solid #ffc107;">
        <strong>Desafio Iniciante:</strong> Como se diz 'Eu gosto de estudar todos os dias' em inglês?
    </div>
    """, unsafe_allow_html=True)
    
    res_usuario = st.text_input("Sua resposta:", key="desafio_estudo")
    if st.button("Validar Resposta"):
        if "i like to study every day" in res_usuario.lower() or "i like studying every day" in res_usuario.lower():
            st.success("Correct! 🎉 Fonética: 'Ai laik tu stâdi évri dei'")
            st.balloons()
        else:
            st.info("Dica: Use o verbo 'to study' e a expressão 'every day'.")

st.markdown("---")
st.caption("Foco no seu progresso pessoal. Keep going! 🚀")
