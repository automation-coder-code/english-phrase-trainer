import streamlit as st
from groq import Groq

# 1. Configuração de UX (Visual por Cores que você aprovou)
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
    st.error("⚠️ Erro: Chave de API não configurada nos Secrets.")
    st.stop()

st.title("📖 English Phrase Trainer")
st.caption("Foco em padrões de frases e pronúncia real")

tab1, tab2 = st.tabs(["🔍 Tradutor & Análise", "📝 Desafios"])

# --- ABA 1: TRADUTOR ---
with tab1:
    texto = st.text_area("Digite a frase para estudar:", placeholder="Ex: I go to school...", label_visibility="collapsed")
    
    if st.button("Analisar para Estudo"):
        if texto:
            with st.spinner('Analisando contexto e fonética...'):
                try:
                    # Prompt REFORMULADO para manter o padrão e fonética correta
                    prompt = f"""Analise a frase: '{texto}'
                    Responda estritamente em PORTUGUÊS seguindo esta estrutura:
                    
                    1. TRADUÇÃO: (tradução natural)
                    
                    2. PRONÚNCIA: (Transcrição fonética para brasileiros. Ex: 'Go' = 'Gôu', 'School' = 'Skul', 'Work' = 'Uôrk').
                    
                    3. ANATOMIA: (Explique a função gramatical de cada palavra da frase original).
                    
                    4. 5 EXEMPLOS EM INGLÊS: (Crie 5 novas frases OBRIGATORIAMENTE EM INGLÊS que usem o mesmo padrão ou verbo da frase original '{texto}'. 
                    Para cada exemplo, forneça a tradução e a pronúncia transcrita correta)."""
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor de inglês rigoroso. Se o usuário usar 'I go', todos os 5 exemplos devem começar com 'I go'. Use uma fonética que imite o SOM do inglês para brasileiros, evitando sons de 'a' ou 'i' extras no final."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.1 # Temperatura baixa para manter a IA focada e não inventar
                    )
                    
                    res = completion.choices[0].message.content
                    st.markdown("---")
                    
                    # Divisão visual limpa
                    if "2. PRONÚNCIA:" in res and "3. ANATOMIA:" in res and "4. 5 EXEMPLOS EM INGLÊS:" in res:
                        st.success(f"### 🏁 Tradução\n{res.split('2. PRONÚNCIA:')[0].replace('1. TRADUÇÃO:', '').strip()}")
                        st.info(f"### 🧩 Pronúncia Transcrita\n{res.split('3. ANATOMIA:')[1].split('2. PRONÚNCIA:')[0] if '3. ANATOMIA:' in res else res.split('2. PRONÚNCIA:')[1].split('3. ANATOMIA:')[0]}")
                        st.info(f"### 📖 Anatomia da Frase\n{res.split('4. 5 EXEMPLOS EM INGLÊS:')[0].split('3. ANATOMIA:')[1]}")
                        st.warning(f"### 💡 5 Exemplos com o mesmo padrão\n{res.split('4. 5 EXEMPLOS EM INGLÊS:')[1]}")
                    else:
                        st.markdown(res)
                    
                except Exception as e:
                    st.error("Erro ao processar. Verifique sua conexão.")
        else:
            st.warning("Digite uma frase primeiro!")

# --- ABA 2: DESAFIOS ---
with tab2:
    st.header("🚀 Prática")
    st.markdown("**Como se diz 'Eu vou ao supermercado' em inglês?**")
    res_user = st.text_input("Sua resposta:", key="study_day")
    if st.button("Verificar"):
        if "i go to the supermarket" in res_user.lower().strip():
            st.success("Correto! Pronúncia: 'Ai gôu tu dâ su-per-mar-ket'")
            st.balloons()
        else:
            st.info("Dica: Use 'I go to the supermarket'.")

st.markdown("---")
st.caption("Foco: Entender padrões e falar corretamente. 🚀")
