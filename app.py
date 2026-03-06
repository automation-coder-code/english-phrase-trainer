import streamlit as st
from groq import Groq

# 1. Configuração de UX (Visual Organizado por Cores)
st.set_page_config(page_title="English Phrase Trainer", page_icon="📖", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px; border: 1px solid #007bff; }
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
st.caption("Foco em pronúncia correta e estrutura da frase")

tab1, tab2 = st.tabs(["🔍 Tradutor & Análise", "📝 Desafios"])

# --- ABA 1: TRADUTOR ---
with tab1:
    texto = st.text_area("Digite a frase para estudar:", placeholder="Ex: I go to school...", label_visibility="collapsed")
    
    if st.button("Analisar para Estudo"):
        if texto:
            with st.spinner('Analisando...'):
                try:
                    # Prompt ultra detalhado para não haver erro de idioma ou fonética
                    prompt = f"""Analise a frase: '{texto}'
                    Responda em PORTUGUÊS seguindo exatamente esta ordem:
                    
                    1. TRADUÇÃO: (tradução natural para português)
                    
                    2. PRONÚNCIA: (Escreva como um brasileiro leria para soar inglês correto. 
                    Exemplo: 'School' escreva 'Skul'. 'I' escreva 'Ai'. 'Go' escreva 'Gôu'. 
                    NUNCA termine palavras com 'a' ou 'i' se o som original for seco).
                    
                    3. ANATOMIA: (Liste cada palavra da frase original em inglês e sua função: ex: verbo, sujeito, etc).
                    
                    4. 5 EXEMPLOS EM INGLÊS: (Crie 5 frases novas OBRIGATORIAMENTE EM INGLÊS. Para cada uma, traga a tradução e a pronúncia transcrita)."""
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor de inglês nativo que fala português. Seu foco é ensinar brasileiros a não falarem com sotaque de 'i' ou 'a' no final das palavras. Os 5 exemplos devem ser frases em inglês."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.1
                    )
                    
                    resposta = completion.choices[0].message.content
                    
                    st.markdown("---")
                    
                    # Divisão visual por seções para evitar bagunça
                    if "2. PRONÚNCIA:" in resposta and "3. ANATOMIA:" in resposta and "4. 5 EXEMPLOS EM INGLÊS:" in resposta:
                        secao1 = resposta.split("2. PRONÚNCIA:")[0]
                        secao2 = resposta.split("3. ANATOMIA:")[0].split("2. PRONÚNCIA:")[1]
                        secao3 = resposta.split("4. 5 EXEMPLOS EM INGLÊS:")[0].split("3. ANATOMIA:")[1]
                        secao4 = resposta.split("4. 5 EXEMPLOS EM INGLÊS:")[1]
                        
                        st.success(f"### 🏁 Tradução\n{secao1.replace('1. TRADUÇÃO:', '').strip()}")
                        
                        st.info(f"### 🧩 Pronúncia Transcrita\n{secao2.strip()}")
                        
                        st.info(f"### 📖 Anatomia da Frase\n{secao3.strip()}")
                        
                        st.warning(f"### 💡 5 Exemplos em Inglês\n{secao4.strip()}")
                    else:
                        # Fallback caso a IA não siga a numeração exata
                        st.markdown(resposta)
                    
                except Exception as e:
                    st.error("Erro ao processar. Tente novamente.")
        else:
            st.warning("Digite uma frase primeiro!")

# --- ABA 2: DESAFIOS ---
with tab2:
    st.header("🚀 Prática")
    st.markdown("**Como se diz 'Eu estudo todos os dias' em inglês?**")
    res_user = st.text_input("Sua resposta:", key="study_day")
    if st.button("Verificar"):
        if "i study every day" in res_user.lower().strip():
            st.balloons()
            st.success("Correto! Pronúncia: 'Ai stâdi évri dei'")
        else:
            st.info("Dica: Use 'I study every day'.")

st.markdown("---")
st.caption("Foco total no seu aprendizado. 🚀")
