import streamlit as st
from groq import Groq
import re

# 1. Configuração de UX (Design Colorido e Minimalista)
st.set_page_config(page_title="English Phrase Trainer", page_icon="📖", layout="centered")
st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 2px solid #007bff; resize: none; }
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

tab1, tab2 = st.tabs(["🔍 Tradutor Real-time", "📝 Tutor de Inglês"])

# --- ABA 1: TRADUTOR ---
with tab1:
    texto = st.text_area("SUA FRASE", placeholder="Ex: I go to the beach...", height=50)
   
    if st.button("Analisar para Estudo"):
        if texto:
            with st.spinner('Decompondo a frase...'):
                try:
                    # Prompt ajustado para o novo formato de exemplos com estrutura específica
                    prompt = f"""Analise a frase: '{texto}'
                    Responda em PORTUGUÊS com este formato exato:
                   
                    TRADUÇÃO / EQUIVALENTE: " (tradução natural, corrigindo erros se houver) "
                   
                    ANÁLISE INTELIGENTE: (Parágrafo explicando a frase, incluindo possíveis erros como capitalização, estrutura gramatical, uso correto, e pronúncia aproximada da frase completa com sons do português. Siga regras de fonética precisa:
                    - 'I' = 'Ai'
                    - 'go' = 'gôu'
                    - 'to' = 'tu'
                    - 'the' = 'dâ'
                    - 'beach' = 'bitch'
                    - 'park' = 'pârc'
                    - 'store' = 'stôr'
                    - 'gym' = 'djim'
                    - 'library' = 'laibreri'
                    - 'movies' = 'mûvis'
                    - 'Monday' = 'mân-dêi'
                    Exemplo de fonética: Para 'I go to the beach' = 'Ai gôu tu dâ bitch'. Integre a fonética no parágrafo de forma natural).
                   
                    5 EXEMPLOS DE USO: (Crie 5 novas frases OBRIGATORIAMENTE EM INGLÊS que usem o MESMO padrão exato da frase '{texto}', corrigido se necessário. Para cada exemplo, formate exatamente assim com quebras de linha:
                    1.
                    English: [Frase em inglês].
                    Tradução: [tradução natural em português].
                    Pronúncia: [pronúncia aproximada da frase completa, ex: 'Ai gôu tu dâ bitch'].)"""
                   
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor de inglês nativo. Analise frases, corrija erros, explique estrutura e pronúncia. Mantenha o padrão nos exemplos. Use fonética fluida para brasileiros, com 'the' SEMPRE como 'dâ'. Evite decompor palavras e erros de acento."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.1
                    )
                   
                    res = completion.choices[0].message.content
                    st.markdown("---")
                   
                    # Parsing ajustado para o novo formato
                    traducao_match = re.search(r'TRADUÇÃO / EQUIVALENTE:(.*?)(?=ANÁLISE INTELIGENTE:|$)', res, re.DOTALL)
                    analise_match = re.search(r'ANÁLISE INTELIGENTE:(.*?)(?=5 EXEMPLOS DE USO:|$)', res, re.DOTALL)
                    exemplos_match = re.search(r'5 EXEMPLOS DE USO:(.*)', res, re.DOTALL)
                   
                    traducao = traducao_match.group(1).strip() if traducao_match else "Não encontrado"
                    analise = analise_match.group(1).strip() if analise_match else "Não encontrado"
                    exemplos = exemplos_match.group(1).strip() if exemplos_match else "Não encontrado"
                   
                    # Exibição em blocos inspirados no screenshot
                    st.info(f"### TRADUÇÃO / EQUIVALENTE\n{traducao}")
                    st.info(f"### ANÁLISE INTELIGENTE\n{analise}")
                    st.warning(f"### 5 EXEMPLOS DE USO\n{exemplos}")
                   
                except Exception as e:
                    st.error(f"Erro na API: {str(e)}. Verifique o modelo ou a chave.")
        else:
            st.warning("Digite uma frase primeiro.")

# --- ABA 2: DESAFIOS (agora como Tutor de Inglês) ---
with tab2:
    st.header("🚀 Desafios")
    
    # Adicionei mais desafios para tornar a aba mais interativa
    desafios = [
        {"pt": "Eu vou à praia", "en": "I go to the beach", "fon": "Ai gôu tu dâ bitch"},
        {"pt": "Ela come uma maçã", "en": "She eats an apple", "fon": "Chi its ân épou"},
        {"pt": "Nós corremos no parque", "en": "We run in the park", "fon": "Ui rân in dâ parc"},
        {"pt": "Ele lê um livro", "en": "He reads a book", "fon": "Ri rids â buk"},
        {"pt": "Eles jogam futebol", "en": "They play soccer", "fon": "Dei plei sôquer"}
    ]
    
    # Selecionar um desafio aleatório ou sequencial (usando session state para manter estado)
    if 'desafio_index' not in st.session_state:
        st.session_state.desafio_index = 0
    
    desafio_atual = desafios[st.session_state.desafio_index]
    
    st.markdown(f"**Traduza: '{desafio_atual['pt']}'**")
    res_user = st.text_input("Sua resposta:", key=f"test_{st.session_state.desafio_index}")
    
    if st.button("Validar"):
        if desafio_atual["en"].lower() in res_user.lower().strip():
            st.success(f"Correto! Pronúncia: '{desafio_atual['fon']}'")
            st.balloons()
            # Avançar para o próximo desafio
            st.session_state.desafio_index = (st.session_state.desafio_index + 1) % len(desafios)
            st.rerun()
        else:
            st.info(f"Dica: Use '{desafio_atual['en']}'.")
    
    # Botão para pular para o próximo
    if st.button("Próximo Desafio"):
        st.session_state.desafio_index = (st.session_state.desafio_index + 1) % len(desafios)
        st.rerun()
