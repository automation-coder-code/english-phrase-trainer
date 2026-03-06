import streamlit as st
from groq import Groq

# 1. Configuração da Página e Estilo CSS para UX Minimalista
st.set_page_config(page_title="Phrase Trainer", page_icon="🇬🇧", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        border: none;
    }
    .stTextArea textarea { border-radius: 10px; }
    div[data-testid="stExpander"] { border: none; box-shadow: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Configure a chave GROQ_API_KEY nos Secrets.")
    st.stop()

# Título Minimalista
st.title("English Phrase Trainer")
st.caption("Focado em Termos Técnicos e ISO | Biodiesel Industry")

tab1, tab2 = st.tabs(["🔍 Tradução", "👨‍🏫 Desafios"])

# --- ABA 1: TRADUTOR ---
with tab1:
    texto = st.text_area("", placeholder="Digite aqui sua frase para traduzir...", key="txt_trad", height=120)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        btn_traduzir = st.button("Analisar Frase")

    if btn_traduzir and texto:
        with st.spinner('Processando...'):
            try:
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Você é um mentor de inglês técnico. Forneça: 1. Tradução direta e clara. 2. Explicação gramatical breve (se necessário). 3. Exatamente 5 exemplos técnicos curtos com tradução. Use Markdown com negrito para termos chave."},
                        {"role": "user", "content": texto}
                    ],
                    model="llama-3.1-8b-instant",
                )
                
                # Exibição organizada do resultado
                resultado = completion.choices[0].message.content
                st.markdown("---")
                st.markdown(resultado)
                
            except Exception as e:
                st.error(f"Erro: {e}")

# --- ABA 2: DESAFIOS TÉCNICOS ---
with tab2:
    st.subheader("💡 Prática de Auditoria e Processos")
    
    desafios = [
        {
            "tema": "ISO 9001 (Qualidade)",
            "pergunta": "Como dizer: 'O controle de qualidade é essencial para o biodiesel'?",
            "correto": "quality control is essential for biodiesel",
            "dica": "Quality control = Controle de qualidade."
        },
        {
            "tema": "ISO 14001 (Ambiental)",
            "pergunta": "Como dizer: 'Reduzimos o impacto ambiental na produção'?",
            "correto": "we reduced the environmental impact in production",
            "dica": "Environmental impact = Impacto ambiental."
        }
    ]

    for i, d in enumerate(desafios):
        with st.container():
            st.markdown(f"**{d['tema']}**")
            st.write(d['pergunta'])
            user_input = st.text_input("Resposta:", key=f"input_{i}", label_visibility="collapsed")
            
            if st.button("Validar", key=f"btn_{i}"):
                if d['correto'] in user_input.lower().strip():
                    st.success("Correct! 🚀")
                    st.balloons()
                else:
                    st.info(f"Dica: {d['dica']}")
            st.markdown("---")

st.caption("Desenvolvido para Lucas Rodrigues | Binatural Process Analysis")
