import streamlit as st
from grafo import ejecutar_grafo


st.set_page_config(
    page_title="BimBam Buy",
    page_icon="🛍️",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

html, body, [class*="css"]{
    background:#070811;
    color:white;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:#090B15;
    border-right:1px solid #25253a;
}

.logo{
    font-size:34px;
    font-weight:bold;
}

.logo span{
    color:#8A3FFC;
}

.card{
    background:#101321;
    border:1px solid #2d2f42;
    border-radius:18px;
    padding:20px;
    margin-top:20px;
}

.online{
    color:#3DFF73;
    font-weight:bold;
}

/* Título */

.title{
    font-size:44px;
    font-weight:700;
}

.subtitle{
    color:#BBBBBB;
    font-size:18px;
    margin-bottom:20px;
}

/* Chat */

.user-bubble{
    background:linear-gradient(90deg,#6B2DFF,#8A3FFC);
    padding:18px;
    border-radius:18px;
    color:white;
    width:fit-content;
    max-width:70%;
    margin-left:auto;
    margin-top:18px;
    margin-bottom:10px;
    font-size:17px;
}

.bot-bubble{
    background:#111420;
    border:1px solid #292C3F;
    padding:20px;
    border-radius:18px;
    color:white;
    width:fit-content;
    max-width:75%;
    margin-top:18px;
    margin-bottom:10px;
    font-size:17px;
}

.bot-name{
    color:#C18BFF;
    font-weight:bold;
    margin-bottom:8px;
}

.footer{
    color:#888;
    text-align:center;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Historial
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"👋 ¡Hola! Soy **Bimbi**, el agente inteligente de BimBam Buy.\n\nEstoy aquí para responder preguntas sobre productos, pedidos, envíos, reembolsos y políticas."
        }
    ]

# =========================
# Sidebar
# =========================

with st.sidebar:

    st.markdown("""
<div class='logo'>
🛍️ BimBam <span>Buy</span>
</div>

<p style="color:#BBB;">
E-commerce multiplataforma
</p>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='card'>

<h2 style="text-align:center;">🤖 Bimbi</h2>

<p style="text-align:center;">
Tu agente inteligente
</p>

<p class='online' style="text-align:center;">
● En línea
</p>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='card'>

<h3>BimBam Buy</h3>

<p>
E-commerce multiplataforma enfocado en una experiencia de compra rápida, segura y confiable.
</p>

</div>
""", unsafe_allow_html=True)

# =========================
# Encabezado
# =========================

st.markdown("""
<div class='title'>
¡Hola! Soy Bimbi 👋
</div>

<div class='subtitle'>
Estoy aquí para ayudarte con todo lo relacionado con BimBam Buy.
</div>
""", unsafe_allow_html=True)

# =========================
# Conversación
# =========================

for msg in st.session_state.messages:

    if msg["role"]=="user":

        st.markdown(
            f"<div class='user-bubble'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='bot-bubble'>
                <div class='bot-name'>🤖 Bimbi</div>
                {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# Entrada
# =========================

pregunta = st.chat_input("Escribe tu pregunta...")

if pregunta:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":pregunta
        }
    )

    st.rerun()

# =========================
# Respuesta IA
# =========================

if (
    len(st.session_state.messages)>0
    and st.session_state.messages[-1]["role"]=="user"
):

    pregunta = st.session_state.messages[-1]["content"]

    with st.spinner("Bimbi está pensando..."):

        try:

            respuesta = ejecutar_grafo(pregunta)

        except Exception as e:

            respuesta = f"❌ Error:\n\n{e}"
        st.markdown(respuesta)
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":respuesta
        }
    )

    st.rerun()

st.markdown(
"""
<div class='footer'>
Bimbi puede cometer errores. Verifica la información importante.
</div>
""",
unsafe_allow_html=True
)