import streamlit as st
from groq import Groq

# 1. Configuração de UX e Identidade Visual (Cores Binatural/Industrial)
st.set_page_config(page_title="Phrase Trainer", page_icon="🇬🇧", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextArea textarea { 
        border: 2px solid #007bff; 
        border-radius: 15px; 
    }
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        background-color: #007bff; 
        color: white; 
        font-weight: bold;
        height: 3.5em;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .section-box {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border-left: 8px solid #007bff;
        background-color: white;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    .word-analysis {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 8px;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API via Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Configure a chave 'GROQ_API_KEY' nos Secrets do Streamlit.")
    st.stop()

# Cabeçalho Elegante
st.markdown("<h1 style='text-align: center; color: #007bff;'>🇬🇧 English Phrase Trainer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analista de Processos | ISO 9001, 14001, 45001 | Biodiesel Industry</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 Tradutor Profissional", "👨‍🏫 Treinamento ISO"])

# --- ABA 1: TRADUTOR DETALHADO ---
with tab1:
    st.markdown("### ✍️ Digite seu texto técnico")
    texto = st.text_area("", placeholder="Ex: The internal audit identified a non-conformity in the production line...", label_visibility="collapsed", height=120)
    
    if st.button("🚀 Analisar Estrutura"):
        if texto:
            with st.spinner('Mapeando processos gramaticais...'):
                try:
                    # Prompt mestre para análise palavra por palavra e cores
                    prompt_final = (
                        f"Analise a frase: '{texto}'. "
                        "Responda em PORTUGUÊS com estas seções obrigatórias: "
                        "1. **Tradução Principal**: Em uma frase clara. "
                        "2. **Análise Morfológica**: Crie uma lista ou tabela detalhando cada palavra, seu significado e o que ela faz na frase (ex: Sujeito, Verbo de ação, Adjetivo técnico, etc). "
                        "3. **Uso Profissional**: 5 exemplos curtos em inglês técnico de biodiesel/ISO com tradução."
                    )
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um mentor de inglês para executivos e engenheiros. Use cores e negritos no Markdown para destacar termos técnicos."},
                            {"role": "user", "content": prompt_final}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.2
                    )
                    
                    res = completion.choices[0].message.content
                    
                    # Layout de Resposta em Blocos Coloridos
                    st.markdown("---")
                    st.success("### 🎯 Tradução Final")
                    st.write(res.split("2.")[0].replace("1. **Tradução Principal**:", "").strip())
                    
                    st.info("### 🧩 Anatomia da Frase (O que cada palavra faz)")
                    st.markdown(res.split("2.")[-1].split("3.")[0])
                    
                    st.warning("### 💡 Exemplos para seu Dia a Dia")
                    st.markdown(res.split("3.")[-1])
                    
                except Exception as e:
                    st.error(f"Erro na conexão: {e}")
        else:
            st.warning("Por favor, insira uma frase para começar.")

# --- ABA 2: DESAFIOS TÉCNICOS ---
with tab2:
    st.markdown("### 📈 Teste seus Conhecimentos")
    
    with st.container():
        st.markdown("""
        <div class='section-box' style='border-left-color: #28a745;'>
            <strong>Desafio de Qualidade (ISO 9001):</strong><br>
            Como se diz: "Nós devemos monitorar os indicadores de desempenho"?
        </div>
        """, unsafe_allow_html=True)
        
        resposta = st.text_input("Sua resposta aqui:", key="challenge_1")
        if st.button("Verificar Resposta"):
            if "monitor" in resposta.lower() and "performance indicators" in resposta.lower():
                st.balloons()
                st.success("Excelente! 'We must monitor the performance indicators'.")
            else:
                st.info("Dica: Use 'monitor' e 'performance indicators'.")

st.markdown("---")
st.caption("Suporte ao Sistema de Gestão Integrado | Lucas Rodrigues")
