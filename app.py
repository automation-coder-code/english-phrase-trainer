import streamlit as st
from groq import Groq

# 1. Configuração de UX Estudo Premium
st.set_page_config(page_title="English Phrase Trainer", page_icon="📖", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 1px solid #007bff; }
    .stButton>button { border-radius: 20px; background-color: #007bff; color: white; height: 3.5em; width: 100%; font-weight: bold; }
    .main-result { padding: 20px; border-radius: 15px; background-color: #f0f7ff; border-left: 6px solid #007bff; margin-top: 20px; }
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
    texto = st.text_area("", placeholder="Ex: I go to school every day...", label_visibility="collapsed", height=100)
    
    if st.button("Analisar Frase Completa"):
        if texto:
            with st.spinner('Analisando pronúncia e gramática...'):
                try:
                    # Prompt REFORMULADO para fonética ultra precisa
                    prompt_instrucao = (
                        f"Analise a frase: '{texto}'. "
                        "Responda em PORTUGUÊS com estas seções: "
                        "1. **Tradução Principal**: Tradução natural. "
                        "2. **Fonética Prática (Som do Português)**: Escreva como um brasileiro leria essa frase para soar correto no inglês. "
                        "ATENÇÃO: 'School' soa como 'skul', 'I' soa como 'Ai', 'Go' soa como 'Gôu'. Não invente vogais no final das palavras. "
                        "3. **Anatomia da Frase**: O que cada palavra faz (sujeito, verbo, etc). "
                        "4. **5 Exemplos de Estudo**: 5 frases curtas usando o contexto, com Tradução e Fonética Prática correta."
                    )
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um especialista em fonética para brasileiros aprendendo inglês. Sua missão é evitar que o aluno pronuncie vogais inexistentes no final das palavras (como dizer 'dógui' em vez de 'dóg' ou 'skóla' em vez de 'skul')."},
                            {"role": "user", "content": prompt_instrucao}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.2
                    )
                    
                    res_total = completion.choices[0].message.content
                    
                    st.markdown("---")
                    st.markdown("### 🎯 Resultado da Análise")
                    
                    # Seção 1: Tradução
                    st.success(f"**Tradução Principal:**\n\n{res_total.split('2.')[0].replace('1. **Tradução Principal**:', '').strip()}")
                    
                    # Seção 2 e 3: Fonética e Anatomia
                    st.info("### 🧩 Pronúncia e Estrutura")
                    st.markdown(f"<div class='main-result'>{res_total.split('2.')[-1].split('4.')[0]}</div>", unsafe_allow_html=True)
                    
                    # Seção 4: 5 Exemplos
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
        <strong>Desafio:</strong> Como se diz 'Eu vou ao trabalho' em inglês?
    </div>
    """, unsafe_allow_html=True)
    
    res_usuario = st.text_input("Sua resposta:", key="desafio_estudo")
    if st.button("Validar Resposta"):
        if "i go to work" in res_usuario.lower().strip():
            st.success("Correct! 🎉 Fonética: 'Ai gôu tu uôrk'")
            st.balloons()
        else:
            st.info("Dica: Use 'I go to work'.")

st.markdown("---")
st.caption("Foco na pronúncia correta. Keep going! 🚀")
