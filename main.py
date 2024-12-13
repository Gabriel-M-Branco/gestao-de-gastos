import streamlit as st

def pagina_1():
    st.write('teste1')

def pagina_2():
    st.write('teste5')


page_names_to_funcs = {
    "Movimentações": pagina_1,
    "Dashboard": pagina_2
}

demo_name = st.sidebar.selectbox("", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()