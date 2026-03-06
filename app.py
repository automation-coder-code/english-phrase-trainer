import streamlit as st
from groq import Groq

# 1. Configurações Iniciais de UX
st.set_page_config(page_title="Phrase Trainer", page_icon="🇬🇧", layout="centered")

# Estilização CSS para botões e áreas de texto
st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 1px solid #007bff; }
    .stButton>button { border-radius: 20px; background-color: #007bff; color: white; transition: 0.3s; }
    .stButton>button:hover { background-color: #0056b3; border: 1px solid #0056b3; }
    .word-box { 
        padding: 10px; 
        border-radius: 8px; 
        background-color: #f0f2f6; 
        margin-bottom: 5px;
        border-left: 5px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Configure a chave GROQ_API_KEY nos Secrets.")
    st.stop()

# Cabeçalho
st.title("English Phrase Trainer")
st.caption("Focado em Processos Industriais e ISO | Binatural")

tab1, tab2 = st.tabs(["🔍 Tradutor Detalhado", "👨‍🏫 Desafios Técnicos"])

# --- ABA 1: TRADUTOR ---
with tab1:
    st.markdown("### 📝 Digite sua frase")
    texto = st.text_area("", placeholder="Ex: We need to improve the production process...", label_visibility="collapsed", height=100)
    
    if st.button("Analisar Frase Completa"):
        if texto:
            with st.spinner('A IA está mapeando o processo da frase...'):
                try:
                    # Prompt ajustado para trazer a análise palavra por palavra
                    prompt_instrucao = (
                        f"Analise a frase: '{texto}'. "
                        "Responda em PORTUGUÊS com este formato: "
                        "1. Tradução completa em um bloco de destaque. "
                        "2. Uma seção chamada 'Análise por Palavra' onde você lista cada palavra da frase original, "
                        "seu significado e sua função (verbo, substantivo, etc) naquela frase. "
                        "3. 5 exemplos curtos em inglês técnico com tradução."
                    )
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um mentor de inglês técnico. Use Markdown para formatar a resposta com cores e negritos."},
                            {"role": "user", "content": prompt_instrucao}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.3
                    )
                    
                    # Exibição Visualmente Atraente
                    st.markdown("### 🎯 Resultado da Análise")
                    st.info(f"**Tradução Principal:**\n\n{completion.choices[0].message.content.split('1.')[-1].split('2.')[0].strip()}")
                    
                    # O restante da análise (Palavras e Exemplos)
                    st.markdown(completion.choices[0].message.content.split('2.')[-1])
                    
                except Exception as e:
                    st.error(f"Erro na análise: {e}")
        else:
            st.warning("Por favor, insira um texto para análise.")

# --- ABA 2: DESAFIOS ---
with tab2:
    st.header("💡 Prática Profissional")
    st.write("Complete a frase corretamente para avançar:")
    
    # Exemplo de desafio focado em auditoria (ISO)
    st.markdown("""
    <div style="background-color:#e1f5fe; padding:20px; border-radius:10px; border-left: 6px solid #03a9f4;">
        <strong>Desafio ISO:</strong> Como se diz 'O auditor encontrou uma não-conformidade'?
    </div>
    """, unsafe_allow_html=True)
    
    res_iso = st.text_input("Sua resposta:", key="iso_1")
    if st.button("Validar"):
        if "non-conformity" in res_iso.lower() and "auditor" in res_iso.lower():
            st.success("Correct! 🎉 'The auditor found a non-conformity'.")
            st.balloons()
        else:
            st.info("Dica: Use 'auditor' e 'non-conformity'.")

st.markdown("---")
st.caption("Desenvolvido para Lucas Rodrigues | Suporte a Auditorias ISO 9001, 14001, 45001")
