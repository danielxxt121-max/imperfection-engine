import os
import streamlit as st
from openai import OpenAI

# Configuração visual do site para celular
st.set_page_config(page_title="The Imperfection Engine", page_icon="⚙️", layout="centered")

# Coleta a chave secreta da OpenAI cadastrada no servidor
api_key = st.secrets.get("OPENAI_API_KEY") if "OPENAI_API_KEY" in st.secrets else os.environ.get("OPENAI_API_KEY")

def engine_humanizador(texto_robotico):
    client = OpenAI(api_key=api_key)
    # Suas regras de ouro exclusivas do negócio
    prompt_sistema = (
        "Você é o 'The Imperfection Engine'. Sua única função é receber textos de IA perfeitinhos "
        "e reescrevê-los aplicando falhas humanas reais. Siga estas 3 regras:\n"
        "1. Alterne o tamanho das frases (use parágrafos normais seguidos de frases curtíssimas).\n"
        "2. Apague clichês de robô (como 'ecossistema', 'revolucionário', 'mitigar', 'holístico').\n"
        "3. Comece algumas frases com expressões humanas de hesitação (ex: 'Veja bem', 'Sejamos francos').\n"
        "O texto final deve convencer o leitor, mas parecer que foi escrito por uma pessoa real."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": texto_robotico}
        ],
        temperature=0.85
    )
    return response.choices.message.content

# Montagem da tela no celular
st.title("⚙️ The Imperfection Engine")
st.write("### O fim dos textos com cara de robô.")

texto_usuario = st.text_area("Cole aqui a copy ou texto gerado por IA:", height=180, placeholder="No dinâmico mercado atual, nosso ecossistema...")

if st.button("Humanizar Texto 🚀", type="primary"):
    if not texto_usuario.strip():
        st.warning("Por favor, cole um texto primeiro!")
    elif not api_key:
        st.error("Erro: Você esqueceu de colocar a sua OPENAI_API_KEY nas configurações do Streamlit.")
    else:
        with st.spinner("Injetando imperfeições humanas..."):
            try:
                texto_final = engine_humanizador(texto_usuario)
                st.success("Texto Humanizado!")
                st.subheader("✨ Resultado:")
                st.write(texto_final)
                st.code(texto_final, language="text") # Facilita para o cliente copiar
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
