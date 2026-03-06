import streamlit as st
from groq import Groq
import re

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
                   
                    # Parsing mais robusto usando regex para extrair seções exatas
                    traducao_match = re.search(r'TRADUÇÃO:(.*?)(?=FONÉTICA:|$)', res, re.DOTALL)
                    fonetica_match = re.search(r'FONÉTICA:(.*?)(?=ANATOMIA:|$)', res, re.DOTALL)
                    anatomia_match = re.search(r'ANATOMIA:(.*?)(?=5 EXEMPLOS EM INGLÊS:|$)', res, re.DOTALL)
                    exemplos_match = re.search(r'5 EXEMPLOS EM INGLÊS:(.*)', res, re.DOTALL)
                   
                    traducao = traducao_match.group(1).strip() if traducao_match else "Não encontrado"
                    fonetica = fonetica_match.group(1).strip() if fonetica_match else "Não encontrado"
                    anatomia = anatomia_match.group(1).strip() if anatomia_match else "Não encontrado"
                    exemplos = exemplos_match.group(1).strip() if exemplos_match else "Não encontrado"
                   
                    # Divisão visual por blocos de cores, agora separados
                    st.success(f"### 🏁 Tradução\n{traducao}")
                    st.info(f"### 🔊 Pronúncia\n{fonetica}")
                    st.info(f"### 🧩 Estrutura\n{anatomia}")
                    st.warning(f"### 💡 5 Exemplos com o mesmo padrão\n{exemplos}")
                   
                except Exception as e:
                    st.error(f"Erro na API: {str(e)}. Verifique o modelo ou a chave.")
        else:
            st.warning("Digite uma frase primeiro.")

# --- ABA 2: DESAFIOS ---
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
