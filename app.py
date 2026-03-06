import streamlit as st
from groq import Groq

# 1. Configuração de UX - Foco em Estudo e Aprendizado
st.set_page_config(page_title="English Study Lab", page_icon="📖", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTextArea textarea { 
        border: 2px solid #6c5ce7; 
        border-radius: 15px; 
    }
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        background-color: #6c5ce7; 
        color: white; 
        font-weight: bold;
        height: 3.5em;
        box-shadow: 0px 4px 10px rgba(108, 92, 231, 0.2);
    }
    .result-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        border-left: 8px solid #6c5ce7;
        margin-top: 20px;
    }
    .word-tag {
        background-color: #f1f0ff;
        color: #6c5ce7;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave de API não configurada.")
    st.stop()

# Cabeçalho de Estudo
st.markdown("<h1 style='text-align: center; color: #6c5ce7;'>📖 English Study Lab</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Seu ambiente pessoal para prática e análise da língua inglesa.</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 Laboratório de Tradução", "📝 Prática de Gramática"])

# --- ABA 1: TRADUTOR E ANÁLISE ---
with tab1:
    st.markdown("### ✍️ O que você quer aprender hoje?")
    texto = st.text_area("", placeholder="Digite uma frase que você ouviu ou quer traduzir...", label_visibility="collapsed", height=120)
    
    if st.button("Analisar para Estudo"):
        if texto:
            with st.spinner('A IA está decompondo a frase...'):
                try:
                    # Prompt focado em ensino da língua
                    prompt_estudo = (
                        f"Analise a frase: '{texto}'. "
                        "Responda em PORTUGUÊS com estas seções: "
                        "1. **Tradução Direta**: Tradução clara e natural. "
                        "2. **Anatomia da Frase**: Liste cada palavra, o significado e explique a função gramatical (ex: artigo, substantivo, verbo no passado, preposição, etc). "
                        "3. **Dicas de Estudo**: Explique uma regra gramatical presente nessa frase ou uma curiosidade cultural. "
                        "4. **Variações**: 3 formas diferentes de dizer a mesma coisa."
                    )
                    
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é um professor particular de inglês paciente e didático. Use negrito e tabelas se necessário para facilitar o aprendizado."},
                            {"role": "user", "content": prompt_estudo}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.4
                    )
                    
                    res = completion.choices[0].message.content
                    
                    st.markdown("---")
                    
                    # Blocos Coloridos para melhor UX de Estudo
                    st.success("### 🏁 Tradução")
                    st.write(res.split("2.")[0].replace("1. **Tradução Direta**:", "").strip())
                    
                    st.info("### 🧩 Como a frase é construída (Palavra por Palavra)")
                    st.markdown(res.split("2.")[-1].split("3.")[0])
                    
                    st.warning("### 💡 Dicas e Variações")
                    st.markdown(res.split("3.")[-1])
                    
                except Exception as e:
                    st.error(f"Erro na conexão: {e}")
        else:
            st.warning("Escreva algo para começarmos o estudo!")

# --- ABA 2: DESAFIOS DE GRAMÁTICA ---
with tab2:
    st.subheader("🚀 Desafios Rápidos")
    st.write("Teste seu conhecimento básico e intermediário:")
    
    # Exemplo de desafio de Gramática (Verb to Be / Present Continuous)
    with st.container():
        st.markdown("""
        <div style='background-color: #fff; padding: 15px; border-radius: 10px; border: 1px solid #ddd;'>
            <strong>Nível Iniciante:</strong><br>
            Como se diz: "Eu estou estudando inglês agora"?
        </div>
        """, unsafe_allow_html=True)
        
        resposta = st.text_input("Sua resposta:", key="study_1")
        if st.button("Verificar"):
            res_limpa = resposta.lower().strip()
            if "i am studying english" in res_limpa or "i'm studying english" in res_limpa:
                st.balloons()
                st.success("Perfeito! Você usou corretamente o Present Continuous (am + studying).")
            else:
                st.info("Dica: Lembre-se do verbo 'to be' (am) e o final 'ing' no verbo principal.")

st.markdown("---")
st.caption("Foco: Evolução constante no idioma Inglês. Keep studying! 🚀")
