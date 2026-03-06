import streamlit as st
from groq import Groq

# 1. Configuração de UX Estudo Premium
st.set_page_config(page_title="English Phrase Trainer", page_icon="📖", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 1px solid #007bff; }
    .stButton>button { border-radius: 20px; background-color: #007bff; color: white; height: 3.5em; width: 100%; font-weight: bold; }
    .main-result { padding: 20px; border-radius: 15px; background-color: #eef6ff; border-left: 6px solid #007bff; margin-top: 20px; }
    .section-title { color: #007bff; font-weight: bold; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave de API não configurada nos Secrets do Streamlit.")
    st.stop()

st.title("📖 English Phrase Trainer")
st.caption("Seu laboratório pessoal para dominar a língua inglesa")

tab1, tab2 = st.tabs(["🔍 Tradutor Detalhado", "📝 Desafios de Estudo"])

# --- ABA 1: TRADUTOR ---
with tab1:
    st.markdown("### 📝 Digite a frase para análise")
    texto = st.text_area("", placeholder="Ex: I want to learn English faster...", label_visibility="collapsed", height=100)
    
    if st.button("Analisar Frase Completa"):
        if texto:
            with st.spinner('Decompondo a estrutura da frase...'):
                try:
                    # Prompt focado em fonética, gramática e 5 exemplos
                    prompt_instrucao = (
                        f"Analise a frase: '{texto}'. "
                        "Responda em PORTUGUÊS seguindo exatamente esta estrutura: "
                        "1. **Tradução Principal**: Tradução natural da frase. "
                        "2. **Pronúncia Prática (Fonética)**: Mostre como se lê cada palavra usando o som do português (Ex: You = Iu). "
                        "3. **Anatomia da Frase**: Liste cada palavra, seu significado e o que ela faz na frase (sujeito, verbo, adjetivo, etc). "
                        "4. **5 Exemplos de Uso**: Crie 5 frases diferentes usando a palavra principal, com tradução e fonética para cada uma."
                    )
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor de inglês didático. Use negrito para destacar termos e mantenha um visual organizado."},
                            {"role": "user", "content": prompt_instrucao}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.3
                    )
                    
                    # Exibição do Resultado Estilizado
                    res_total = completion.choices[0].message.content
                    
                    st.markdown("---")
                    st.markdown("### 🎯 Resultado da Análise")
                    
                    # Caixa de Tradução Principal
                    st.info(f"**Tradução:** {res_total.split('2.')[0].replace('1. **Tradução Principal**:', '').strip()}")
                    
                    # Anatomia e Fonética
                    st.markdown(f"<div class='main-result'>{res_total.split('2.')[-1]}</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Erro na análise: {e}")
        else:
            st.warning("Por favor, insira um texto para começar o estudo.")

# --- ABA 2: DESAFIOS ---
with tab2:
    st.header("🚀 Prática de Gramática")
    st.write("Traduza a frase abaixo para testar seu conhecimento:")
    
    st.markdown("""
    <div style="background-color:#fff9c4; padding:20px; border-radius:10px; border-left: 6px solid #fbc02d;">
        <strong>Desafio:</strong> Como se diz 'Eu gosto de ler livros' em inglês?
    </div>
    """, unsafe_allow_html=True)
    
    res_usuario = st.text_input("Sua resposta:", key="desafio_estudo")
    if st.button("Verificar"):
        if "i like to read books" in res_usuario.lower() or "i like reading books" in res_usuario.lower():
            st.success("Correct! 🎉 Pronúncia: 'Ai laik tu rid buks'")
            st.balloons()
        else:
            st.info("Dica: Use o verbo 'to read' e o substantivo 'books'.")

st.markdown("---")
st.caption("Foco no aprendizado contínuo | Evolua seu Inglês diariamente")
