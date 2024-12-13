import streamlit as st
from streamlit_option_menu import option_menu

selected = option_menu(None, ["Configurações", "Orçamento", "Lançamentos", 'Dashboard', 'Relatórios'], 
    icons=['sliders', 'cash', "list-ul", 'graph-up', 'file-earmark-bar-graph'], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"max-width": "680px!important"}
    })


if selected == "Configurações":
    st.title("Configurações")
    st.write("Aqui você pode ajustar suas preferências.")
    
elif selected == "Orçamento":
    st.title("Orçamento")
    st.write("Aqui você pode gerenciar seu orçamento.")
    
elif selected == "Lançamentos":
    st.title("Lançamentos")
    st.write("Aqui você pode registrar seus lançamentos financeiros.")
    
elif selected == "Dashboard":
    st.title("Dashboard")
    st.write("Aqui você pode ver as visualizações dos seus dados financeiros.")
    
elif selected == "Relatórios":
    st.title("Relatórios")
    st.write("Aqui você pode acessar os relatórios financeiros.")