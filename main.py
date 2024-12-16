import streamlit as st
from streamlit_option_menu import option_menu
import json
import os

ARQUIVO_JSON = "dados.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"categorias": {"receitas": [], "gastos": [], "investimentos": []}}

def salvar_dados(dados):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)

def excluir_categoria(tipo, categoria):
    dados = carregar_dados()
    if categoria in dados["categorias"][tipo]:
        dados["categorias"][tipo].remove(categoria)
        salvar_dados(dados)
        return True
    return False
    
dados = carregar_dados()

st.markdown(
    """
    <style>
    .block-container {
        padding: 45px 0;
        max-width: 80% !important;
    }
    .card {
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        padding: 10px;
        margin: 10px 0;
        text-align: center;
        font-family: Arial, sans-serif;
        font-size: 16px;
    }
    h4 a, h3 a, h2 a {
            display: none !important;
    }
    </style>
    """, unsafe_allow_html=True
)

selected = option_menu(
    None, ["Configurações", "Orçamento", "Lançamentos", 'Dashboard', 'Relatórios'], 
    icons=['sliders', 'cash', "list-ul", 'graph-up', 'file-earmark-bar-graph'], 
    default_index=0, orientation="horizontal"
)

if selected == "Configurações":
    st.subheader("Categorias de Receitas")
    nova_receita = st.text_input("Adicionar nova categoria de Receita")
    if st.button("Adicionar Receita"):
        if nova_receita and nova_receita not in dados["categorias"]["receitas"]:
            dados["categorias"]["receitas"].append(nova_receita)
            salvar_dados(dados)
            st.success(f"Categoria '{nova_receita}' adicionada com sucesso!")
        elif nova_receita in dados["categorias"]["receitas"]:
            st.warning("Essa categoria já existe!")
        else:
            st.error("O campo não pode estar vazio!")

    st.subheader("Categorias de Gastos")
    novo_gasto = st.text_input("Adicionar nova categoria de Gasto")
    if st.button("Adicionar Gasto"):
        if novo_gasto and novo_gasto not in dados["categorias"]["gastos"]:
            dados["categorias"]["gastos"].append(novo_gasto)
            salvar_dados(dados)
            st.success(f"Categoria '{novo_gasto}' adicionada com sucesso!")
        elif novo_gasto in dados["categorias"]["gastos"]:
            st.warning("Essa categoria já existe!")
        else:
            st.error("O campo não pode estar vazio!")

    st.subheader("Categorias de Investimentos")
    novo_investimento = st.text_input("Adicionar nova categoria de Investimento")
    if st.button("Adicionar Investimento"):
        if novo_investimento and novo_investimento not in dados["categorias"]["investimentos"]:
            dados["categorias"]["investimentos"].append(novo_investimento)
            salvar_dados(dados)
            st.success(f"Categoria '{novo_investimento}' adicionada com sucesso!")
        elif novo_investimento in dados["categorias"]["investimentos"]:
            st.warning("Essa categoria já existe!")
        else:
            st.error("O campo não pode estar vazio!")

    st.write("### Categorias Salvas:")
    
    for tipo, categorias in dados["categorias"].items():
        if categorias:
            st.markdown(f"#### {tipo.capitalize()}")
            colunas = st.columns(3)
            for i, categoria in enumerate(categorias):
                with colunas[i % 3]:
                    st.markdown(f"<div class='card'>{categoria}</div>", unsafe_allow_html=True)

            categoria_excluir = st.selectbox(f"Selecione a categoria de {tipo} que deseja excluir", categorias, key=f"excluir_{tipo}")
            
            if categoria_excluir:
                if st.button(f"Confirmar exclusão de '{categoria_excluir}'", key=f"excluir_btn_{categoria_excluir}"):
                    if excluir_categoria(tipo, categoria_excluir):
                        st.success(f"Categoria '{categoria_excluir}' excluída com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"A categoria '{categoria_excluir}' não foi encontrada em {tipo}.")
        else:
            st.write(f"Nenhuma categoria de **{tipo}** cadastrada.")

elif selected == "Orçamento":
    st.subheader("Defina seu orçamento para cada categoria")
    categorias = dados["categorias"]["gastos"]
    if not categorias:
        st.warning("Nenhuma categoria de gasto cadastrada. Adicione em Configurações.")
    else:
        orcamento = {}
        for categoria in categorias:
            orcamento[categoria] = st.number_input(f"Orçamento para {categoria}", min_value=0, step=100)
        total_orcamento = sum(orcamento.values())
        st.write(f"Total do orçamento: R${total_orcamento}")

elif selected == "Lançamentos":
    st.subheader("Registrar Lançamento")
    tipo_lancamento = st.selectbox("Tipo de lançamento", ["Despesa", "Receita", "Investimento"])
    valor = st.number_input("Valor", min_value=0.01, step=0.01)
    categoria = st.selectbox("Categoria", dados["categorias"][tipo_lancamento.lower()] if dados["categorias"][tipo_lancamento.lower()] else ["Nenhuma categoria cadastrada"])
    descricao = st.text_area("Descrição do lançamento", "")

    if st.button("Registrar lançamento"):
        if categoria == "Nenhuma categoria cadastrada":
            st.error("Adicione categorias primeiro na aba Configurações.")
        else:
            st.success(f"Você registrou um {tipo_lancamento.lower()} de R${valor} na categoria {categoria}.")

elif selected == "Dashboard":
    st.subheader("Visualizações dos Dados Financeiros")
    st.write("Aqui você pode ver gráficos e estatísticas baseados nos seus dados financeiros.")

elif selected == "Relatórios":
    st.subheader("Relatórios Financeiros")
    st.write("Aqui você pode acessar os relatórios financeiros.")