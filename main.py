import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

selected = option_menu(None, ["Configurações", "Orçamento", "Lançamentos", 'Dashboard', 'Relatórios'], 
    icons=['sliders', 'cash', "list-ul", 'graph-up', 'file-earmark-bar-graph'], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"max-width": "680px!important"}
    })


if selected == "Configurações":
    st.title("Configurações")
    
    st.subheader("Metas financeiras")
    meta_poupanca = st.number_input("Meta de poupança mensal", min_value=0, step=100)
    st.write(f"Sua meta de poupança mensal é: R${meta_poupanca}")
    
elif selected == "Orçamento":
    st.title("Orçamento")
    
    st.subheader("Defina seu orçamento para cada categoria")
    categorias = ["Alimentação", "Transporte", "Lazer", "Saúde", "Educação"]
    
    orcamento = {}
    for categoria in categorias:
        orcamento[categoria] = st.number_input(f"Orçamento para {categoria}", min_value=0, step=100)
    
    st.write("Seu orçamento definido:")
    for categoria, valor in orcamento.items():
        st.write(f"{categoria}: R${valor}")
    
    st.subheader("Visualização de orçamento")
    total_orcamento = sum(orcamento.values())
    st.write(f"Total do orçamento: R${total_orcamento}")
    
elif selected == "Lançamentos":
    st.title("Lançamentos")
    
    tipo_lancamento = st.selectbox("Tipo de lançamento", ["Despesa", "Receita"])    
    valor = st.number_input("Valor", min_value=0.01, step=0.01)
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Saúde", "Educação"])
    descricao = st.text_area("Descrição do lançamento", "")
    
    if st.button("Registrar lançamento"):
        st.write(f"Você registrou um {tipo_lancamento.lower()} de R${valor} na categoria {categoria}.")
        
    
elif selected == "Dashboard":
    st.title("Dashboard")
    st.write("Aqui você pode ver as visualizações dos seus dados financeiros.")
    
elif selected == "Relatórios":
    st.title("Relatórios")
    st.write("Aqui você pode acessar os relatórios financeiros.")
