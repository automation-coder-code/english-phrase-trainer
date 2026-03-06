import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="English Phrase Trainer", page_icon="🇬🇧")

# Inicialização segura da API via Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave GROQ_API_KEY não configurada nos Secrets do Streamlit.")
    st.stop()

st.title("🇬🇧 English Phrase Trainer")

# Abas de navegação
tab1, tab2 = st.tabs(["🔍 Tradutor & 5 Exemplos", "👨‍🏫 Treino Técnico (ISO & Biodiesel)"])

# --- ABA 1: TRADUTOR ---
with tab1:
    st.header("Tradutor Inteligente")
    st.write("Digite sua frase e clique no botão para processar.")
    
    texto = st.text_area("Digite sua frase em PT ou EN:", key="txt_trad", height=150)
    
    # Botão para evitar consumo desnecessário e facilitar o envio
    if st.button("Traduzir e Analisar"):
        if texto:
            with st.spinner('O Llama 3.1 está analisando...'):
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system", 
                                "content": "Você é um professor de inglês especializado em termos técnicos industriais. Traduza a frase, explique a gramática em português e dê 5 exemplos curtos em inglês com tradução."
                            },
                            {
                                "role": "user", 
                                "content": texto
                            }
                        ],
                        model="llama-3.1-8b-instant",
                    )
                    st.markdown("---")
                    st.markdown(completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"Erro na análise: {e}")
        else:
            st.warning("Por favor, digite algo antes de traduzir.")

# --- ABA 2: TREINO TÉCNICO ---
with tab2:
    st.header("Treinamento Profissional")
    st.info("Desafios baseados na sua rotina de análise de processos e normas ISO.")

    # Dicionário de desafios técnicos
    desafios = {
        "Qualidade (ISO 9001)": {
            "pergunta": "Como se diz: 'Nós precisamos realizar uma auditoria interna no processo de produção'?",
            "correto": "we need to conduct an internal audit in the production process",
            "dica": "Use 'conduct an internal audit'."
        },
        "Meio Ambiente (ISO 14001)": {
            "pergunta": "Como se diz: 'O biodiesel é um combustível renovável e sustentável'?",
            "correto": "biodiesel is a renewable and sustainable fuel",
            "dica": "Biodiesel se escreve igual, 'Sustainable' é sustentável."
        },
        "Segurança (ISO 45001)": {
            "pergunta": "Como se diz: 'Todos os funcionários devem usar equipamentos de proteção individual'?",
            "correto": "all employees must use personal protective equipment",
            "dica": "Equipamento de Proteção Individual = PPE (Personal Protective Equipment)."
        }
    }

    for tema, info in desafios.items():
        with st.expander(f"📌 Desafio: {tema}"):
            st.write(info["pergunta"])
            user_res = st.text_input("Sua resposta:", key=f"input_{tema}")
            
            if st.button("Validar", key=f"btn_{tema}"):
                if info["correto"] in user_res.lower().strip():
                    st.balloons()
                    st.success("Perfect! Você dominou esse termo técnico! 🎉")
                else:
                    st.warning(f"Quase lá! Dica: {info['dica']}")

    st.markdown("---")
    st.caption("Dica: Use a Aba 1 para explorar as variações dessas frases técnicas!")
