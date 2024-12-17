import streamlit as st
from streamlit_option_menu import option_menu
import json
import os

CATEGORIAS_JSON = "categorias.json"
LANCAMENTOS_JSON = "lancamentos.json"

def carregar_categorias():
    if os.path.exists(CATEGORIAS_JSON):
        with open(CATEGORIAS_JSON, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"categorias": {"receitas": [], "gastos": [], "investimentos": []}}


def salvar_categorias(dados):
    with open(CATEGORIAS_JSON, "w", encoding="utf-8") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)


def excluir_categoria(tipo, categoria):
    categorias = carregar_categorias()
    if categoria in categorias["categorias"][tipo]:
        categorias["categorias"][tipo].remove(categoria)
        salvar_categorias(categorias)
        return True
    return False
    

def carregar_lancamentos():
    if os.path.exists(LANCAMENTOS_JSON):
        with open(LANCAMENTOS_JSON, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"lancamentos": []}


def salvar_lancamentos(dados):
    with open(LANCAMENTOS_JSON, "w", encoding="utf-8") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)


def excluir_lancamentos(tipo, lancamento):
    lancamentos = carregar_lancamentos()
    if lancamento in lancamentos["lancamentos"][tipo]:
        lancamentos["lancamentos"][tipo].remove(lancamento)
        salvar_lancamentos(lancamentos)
        return True
    return False


categorias = carregar_categorias()

st.markdown(
    """
    <style>
    .block-container {
        padding: 45px 0;
        max-width: 80% !important;
    }
    .card {
        color: white;
        background-color: rgb(24, 27, 33);
        border-radius: 10px;
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
    None, ["Categorias", "Orçamento", "Lançamentos", 'Dashboard', 'Relatórios'], 
    icons=['bi-tags', 'cash', "list-ul", 'graph-up', 'file-earmark-bar-graph'], 
    default_index=0, orientation="horizontal"
)

if selected == "Categorias":
    st.subheader("Categorias de Receitas")
    nova_receita = st.text_input("Adicionar nova categoria de Receita")
    if st.button("Adicionar Receita"):
        if nova_receita not in categorias["categorias"]["receitas"]:
            categorias["categorias"]["receitas"].append(nova_receita)
            salvar_categorias(categorias)
            st.success(f"Categoria '{nova_receita}' adicionada com sucesso!")
        elif nova_receita in categorias["categorias"]["receitas"]:
            st.warning("Essa categoria já existe!")
        else:
            st.error("O campo não pode estar vazio!")

    st.subheader("Categorias de Gastos")
    novo_gasto = st.text_input("Adicionar nova categoria de Gasto")
    if st.button("Adicionar Gasto"):
        if novo_gasto and novo_gasto not in categorias["categorias"]["gastos"]:
            categorias["categorias"]["gastos"].append(novo_gasto)
            salvar_categorias(categorias)
            st.success(f"Categoria '{novo_gasto}' adicionada com sucesso!")
        elif novo_gasto in categorias["categorias"]["gastos"]:
            st.warning("Essa categoria já existe!")
        else:
            st.error("O campo não pode estar vazio!")

    st.subheader("Categorias de Investimentos")
    novo_investimento = st.text_input("Adicionar nova categoria de Investimento")
    if st.button("Adicionar Investimento"):
        if novo_investimento and novo_investimento not in categorias["categorias"]["investimentos"]:
            categorias["categorias"]["investimentos"].append(novo_investimento)
            salvar_categorias(categorias)
            st.success(f"Categoria '{novo_investimento}' adicionada com sucesso!")
        elif novo_investimento in categorias["categorias"]["investimentos"]:
            st.warning("Essa categoria já existe!")
        else:
            st.error("O campo não pode estar vazio!")

    st.write("### Categorias Salvas:")
    
    for tipo, categorias in categorias["categorias"].items():
        if categorias:
            st.markdown(f"#### {tipo.capitalize()}")
            colunas = st.columns(3)
            for i, categoria in enumerate(categorias):
                with colunas[i % 3]:
                    st.markdown(f"<div class='card'>{categoria}</div>", unsafe_allow_html=True)

            categoria_excluir = st.selectbox(f"Selecione a categoria de {tipo} que deseja excluir", categorias, key=f"excluir_{tipo}")
            
            if categoria_excluir:
                if st.button(f'Excluir', key=f"excluir_btn_{categoria_excluir}"):
                    if excluir_categoria(tipo, categoria_excluir):
                        st.success(f"Categoria '{categoria_excluir}' excluída com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"A categoria '{categoria_excluir}' não foi encontrada em {tipo}.")
        else:
            st.write(f"Nenhuma categoria de **{tipo}** cadastrada.")

elif selected == "Orçamento":
    st.subheader("Defina seu orçamento para Gastos")
    categorias_gastos = categorias["categorias"]["gastos"]
    if not categorias_gastos:
        st.warning("Nenhuma categoria de gastos cadastrada. Adicione em Configurações.")
    else:
        orcamento = {}
        for categoria in categorias_gastos:
            orcamento[categoria] = st.number_input(f"Orçamento para {categoria}", min_value=0, step=100)
        total_orcamento = sum(orcamento.values())
        st.write(f"Total do orçamento: R${total_orcamento}")
    
    st.subheader("Defina seu orçamento para Investimentos")
    categorias_investimentos = categorias["categorias"]["investimentos"]
    if not categorias_investimentos:
        st.warning("Nenhuma categoria de investimentos cadastrada. Adicione em Configurações.")
    else:
        investimentos = {}
        for categoria in categorias_investimentos:
            investimentos[categoria] = st.number_input(f"Investimento para {categoria}", min_value=0, step=100)
        total_investimentos = sum(investimentos.values())
        st.write(f"Total investido: R${total_investimentos}")

elif selected == "Lançamentos":
    st.subheader("Registrar Lançamento")
    tipo_lancamento = st.selectbox("Tipo de lançamento", ["Gastos", "Receitas", "Investimentos"])
    valor = st.number_input("Valor", min_value=0.01, step=0.01)
    categoria = st.selectbox(
        "Categoria", 
        categorias["categorias"].get(tipo_lancamento.lower(), ["Nenhuma categoria cadastrada"])
    )
    descricao = st.text_area("Descrição do lançamento", "")
    data = str(st.date_input("Data do lançamento"))

    if st.button("Registrar lançamento"):
        if categoria == "Nenhuma categoria cadastrada":
            st.error("Adicione categorias primeiro na aba Configurações.")
        else:
            lancamentos = carregar_lancamentos()

            novo_lancamento = {
                "tipo": tipo_lancamento,
                "valor": valor,
                "categoria": categoria,
                "descricao": descricao,
                "data": data
            }

            lancamentos["lancamentos"].append(novo_lancamento)
            salvar_lancamentos(lancamentos)
            st.success(f"Você registrou um {tipo_lancamento.lower()} de R${valor} na categoria {categoria}.")

elif selected == "Dashboard":
    st.subheader("Visualizações dos Dados Financeiros")
    st.write("Aqui você pode ver gráficos e estatísticas baseados nos seus dados financeiros.")

elif selected == "Relatórios":
    st.subheader("Relatórios Financeiros")
    st.write("Aqui você pode acessar os relatórios financeiros.")