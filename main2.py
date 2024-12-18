import streamlit as st
import pandas as pd
import json
import os
import uuid
from streamlit_option_menu import option_menu
import plotly.express as px

CATEGORIAS_JSON = "categorias.json"
LANCAMENTOS_JSON = "lancamentos.json"
ORCAMENTO_JSON = "orcamento.json"


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



def carregar_orcamento():
    if os.path.exists(ORCAMENTO_JSON):
        try:
            with open(ORCAMENTO_JSON, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {"gastos": {}, "investimentos": {}}
    return {"gastos": {}, "investimentos": {}}


def salvar_orcamento(dados):
    with open(ORCAMENTO_JSON, "w", encoding="utf-8") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)


def atualizar_orcamento(tipo, categoria, valor):
    orcamento = carregar_orcamento()
    if tipo in orcamento:
        orcamento[tipo][categoria] = valor
        salvar_orcamento(orcamento)
        return True
    return False


def excluir_categoria_orcamento(tipo, categoria):
    orcamento = carregar_orcamento()
    if tipo in orcamento and categoria in orcamento[tipo]:
        del orcamento[tipo][categoria]
        salvar_orcamento(orcamento)
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
    None, ["Categorias", "Orçamento", "Lançamentos", 'Dashboard'], 
    icons=['bi-tags', 'cash', "list-ul", 'graph-up'], 
    default_index=0, orientation="horizontal"
)

if selected == "Categorias":
    categorias = carregar_categorias()

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
    st.subheader("Defina seu Orçamento")

    orcamento = carregar_orcamento()

    st.subheader("Orçamento para Gastos")
    categorias_gastos = categorias["categorias"]["gastos"]

    if not categorias_gastos:
        st.warning("Nenhuma categoria de gastos cadastrada. Adicione em Categorias.")
    else:
        for categoria in categorias_gastos:
            valor = orcamento["gastos"].get(categoria, 0)
            novo_valor = st.number_input(
                f"Defina o orçamento para '{categoria}'",
                  value=float(valor),
                  min_value=0.0,
                  step=10.0)
            if st.button(f"Salvar orçamento para {categoria}", key=f"salvar_gasto_{categoria}"):
                atualizar_orcamento("gastos", categoria, novo_valor)
                st.success(f"Orçamento para '{categoria}' atualizado para R${novo_valor:.2f}.")

    st.subheader("Orçamento para Investimentos")
    categorias_investimentos = categorias["categorias"]["investimentos"]

    if not categorias_investimentos:
        st.warning("Nenhuma categoria de investimentos cadastrada. Adicione em Categorias.")
    else:
        for categoria in categorias_investimentos:
            valor = orcamento["investimentos"].get(categoria, 0)
            novo_valor = st.number_input(
                f"Defina o orçamento para '{categoria}'",
                  value=float(valor),
                    min_value=0.0,
                      step=10.0)
            if st.button(f"Salvar orçamento para {categoria}", key=f"salvar_investimentos_{categoria}"):
                atualizar_orcamento("investimentos", categoria, novo_valor)
                st.success(f"Orçamento para '{categoria}' atualizado para R${novo_valor:.2f}.")

    total_gastos = sum(orcamento["gastos"].values())
    total_investimentos = sum(orcamento["investimentos"].values())
    st.write(f"**Total de Gastos Planejados:** R${total_gastos:.2f}")
    st.write(f"**Total de Investimentos Planejados:** R${total_investimentos:.2f}")

    if st.button("Resetar Orçamento"):
        salvar_orcamento({"gastos": {}, "investimentos": {}})
        st.success("Orçamento resetado com sucesso!")
        st.rerun()

elif selected == "Lançamentos":
    categorias = carregar_categorias()
    lancamentos = carregar_lancamentos()

    st.subheader("Registrar Lançamento")
    tipo_lancamento = st.selectbox("Tipo de lançamento", ["Gastos", "Receitas", "Investimentos"])
    valor = st.number_input("Valor", min_value=0.0, step=1.0)
    categoria = st.selectbox(
        "Categoria", 
        categorias["categorias"].get(tipo_lancamento.lower(), ["Nenhuma categoria cadastrada"])
    )
    descricao = st.text_area("Descrição do lançamento", "")
    data = st.date_input("Data do lançamento")
    data_formatada = data.strftime('%Y-%m-%d')

    if tipo_lancamento == "Investimentos":
        taxa_rendimento = st.number_input("Taxa de Rendimento (%)", min_value=0.0, step=0.1)
        meses = st.number_input("Meses para o investimento", min_value=1, step=1)
    else:
        taxa_rendimento = None
        meses = None

    if st.button("Registrar lançamento"):
        if categoria == "Nenhuma categoria cadastrada":
            st.error("Adicione categorias primeiro na aba Configurações.")
        else:
            lancamentos = carregar_lancamentos()

            novo_id = str(uuid.uuid4())

            novo_lancamento = {
                "id": novo_id,
                "tipo": tipo_lancamento,
                "valor": valor,
                "categoria": categoria,
                "descricao": descricao,
                "data": data_formatada,
                "taxa_rendimento": taxa_rendimento,
                "meses": meses
            }

            lancamentos["lancamentos"].append(novo_lancamento)
            salvar_lancamentos(lancamentos)
            st.success(f"Você registrou um {tipo_lancamento.lower()} de R${valor} na categoria {categoria}.")
    
    lancamentos = carregar_lancamentos()
    st.title("Histórico de Lançamentos")
    
    if not lancamentos["lancamentos"]:
        st.warning("Nenhum lançamento registrado até o momento.")
    else:
        st.subheader("Lançamentos Salvos")

        df = pd.DataFrame(lancamentos["lancamentos"])
        
        df.set_index('id', inplace=True)

        st.dataframe(df.style.format({
            "valor": "R$ {:.2f}",
            "data": lambda x: pd.to_datetime(x).strftime('%d/%m/%Y'),
            "taxa_rendimento": lambda x: f"{x:.2f}%" if pd.notna(x) else "-",
            "meses": lambda x: x if pd.notna(x) else "-"
        }), use_container_width=True)

    st.subheader("Excluir Lançamentos")
    lancamentos = carregar_lancamentos()

    if not lancamentos["lancamentos"]:
        st.warning("Nenhum lançamento registrado até o momento.")
    else:
        lancamentos_por_categoria = {}
        for lancamento in lancamentos["lancamentos"]:
            categoria = lancamento["categoria"]
            if categoria not in lancamentos_por_categoria:
                lancamentos_por_categoria[categoria] = []
            lancamentos_por_categoria[categoria].append(lancamento)

        for categoria, lista_lancamentos in lancamentos_por_categoria.items():
            st.markdown(f"### Categoria: {categoria}")
            
            ids_lancamentos = [lancamento["id"] for lancamento in lista_lancamentos]
            
            lancamento_excluir_id = st.selectbox(
                f"Selecione o ID de um lançamento de {categoria} para excluir",
                ids_lancamentos,
                key=f"excluir_{categoria}"
            )

            if lancamento_excluir_id:
                if st.button(f'Excluir lançamento com ID {lancamento_excluir_id}', key=f"excluir_btn_{lancamento_excluir_id}"):
                    lancamentos["lancamentos"] = [l for l in lancamentos["lancamentos"] if l["id"] != lancamento_excluir_id]
                    salvar_lancamentos(lancamentos)
                    st.success(f"Lançamento com ID {lancamento_excluir_id} excluído com sucesso!")
                    st.rerun()

elif selected == "Dashboard":
    dados_lancamentos = carregar_lancamentos()
    dados_categorias = carregar_categorias()

    lancamentos = pd.DataFrame(dados_lancamentos["lancamentos"])
    lancamentos["data"] = pd.to_datetime(lancamentos["data"])

    st.subheader("Dashboard de Lançamentos")

    st.sidebar.header("Filtros")

    tipo_filter = st.sidebar.multiselect(
        "Filtrar por Tipo:",
        options=lancamentos["tipo"].unique(),
        default=lancamentos["tipo"].unique()
    )

    if tipo_filter:
        categorias_filtradas = dados_categorias["categorias"]
        categorias_selecionadas = []
        
        for tipo in tipo_filter:
            categorias_selecionadas.extend(categorias_filtradas[tipo.lower()])
        
        categorias_selecionadas = list(set(categorias_selecionadas))

        categoria_filter = st.sidebar.multiselect(
            "Filtrar por Categoria:",
            options=categorias_selecionadas,
            default=categorias_selecionadas
        )
    else:
        categoria_filter = st.sidebar.multiselect(
            "Filtrar por Categoria:",
            options=lancamentos["categoria"].unique(),
            default=lancamentos["categoria"].unique()
        )

    date_range = st.sidebar.date_input(
        "Filtrar por Intervalo de Datas:",
        [lancamentos["data"].min(), lancamentos["data"].max()]
    )

    filtered_data = lancamentos[
        (lancamentos["tipo"].isin(tipo_filter)) &
        (lancamentos["categoria"].isin(categoria_filter)) &
        (lancamentos["data"] >= pd.Timestamp(date_range[0])) &
        (lancamentos["data"] <= pd.Timestamp(date_range[1]))
    ]

    st.subheader("Dados Filtrados")
    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index += 1

    tem_investimentos = filtered_data["tipo"].str.contains("Investimentos").any()

    if tem_investimentos:
        st.dataframe(filtered_data.style.format({
            "valor": "R$ {:.2f}",
            "data": lambda x: pd.to_datetime(x).strftime('%d/%m/%Y'),
            "taxa_rendimento": lambda x: f"{x:.2f}%" if pd.notna(x) else "-",
            "meses": lambda x: x if pd.notna(x) else "-"
        }), use_container_width=True)
    else:
        filtered_data = filtered_data.loc[:, ~filtered_data.columns.isin(['taxa_rendimento', 'meses'])]
        st.dataframe(filtered_data.style.format({
            "valor": "R$ {:.2f}",
            "data": lambda x: pd.to_datetime(x).strftime('%d/%m/%Y'),
        }), use_container_width=True)

    st.subheader("Resumo")
    col1, col2 = st.columns(2)
    with col1:
        total_valor = filtered_data["valor"].sum()
        st.metric(label="Total (R$)", value=f"{total_valor:,.2f}")
    with col2:
        valor_medio = round(filtered_data["valor"].mean(), 2)
        st.metric(label="Valor Médio (R$)", value=valor_medio)

    st.write("") 
    st.write("") 

    st.subheader("Distribuição Financeira")

    col1, col2, col3 = st.columns(3)

    with col1:
        if not filtered_data.empty:
            gastos_data = filtered_data[filtered_data["tipo"] == "Gastos"]
            pie_chart_gastos = px.pie(
                gastos_data,
                names="categoria",
                values="valor",
                title="Distribuição de Gastos por Categoria",
                labels={"categoria": "Categoria", "valor": "Valor (R$)"},
                hole=0.4
            )
            st.plotly_chart(pie_chart_gastos, use_container_width=True)

    with col2:
        if not filtered_data.empty:
            receitas_data = filtered_data[filtered_data["tipo"] == "Receitas"]
            pie_chart_receitas = px.pie(
                receitas_data,
                names="categoria",
                values="valor",
                title="Distribuição de Receitas por Categoria",
                labels={"categoria": "Categoria", "valor": "Valor (R$)"},
                hole=0.4
            )
            st.plotly_chart(pie_chart_receitas, use_container_width=True)

    with col3:
        if not filtered_data.empty:
            investimentos_data = filtered_data[filtered_data["tipo"] == "Investimentos"]
            pie_chart_investimentos = px.pie(
                investimentos_data,
                names="categoria",
                values="valor",
                title="Distribuição de Investimentos por Categoria",
                labels={"categoria": "Categoria", "valor": "Valor (R$)"},
                hole=0.4
            )
            st.plotly_chart(pie_chart_investimentos, use_container_width=True)


    st.subheader("Gastos, Receitas e Investimentos por Categoria por Mês")

    if not filtered_data.empty:
        filtered_data['mês'] = filtered_data['data'].dt.to_period('M').astype(str)

        gastos_data = filtered_data[filtered_data["tipo"] == "Gastos"]
        if not gastos_data.empty:
            gastos_por_categoria = gastos_data.groupby(['mês', 'categoria'])['valor'].sum().reset_index()
            bar_chart_gastos = px.bar(
                gastos_por_categoria,
                x='mês',
                y='valor',
                color='categoria',
                title='Gastos por Categoria por Mês',
                labels={"valor": "Valor (R$)", "mês": "Mês"},
                barmode='group'
            )
            st.plotly_chart(bar_chart_gastos, use_container_width=True)

        receitas_data = filtered_data[filtered_data["tipo"] == "Receitas"]
        if not receitas_data.empty:
            receitas_por_categoria = receitas_data.groupby(['mês', 'categoria'])['valor'].sum().reset_index()
            bar_chart_receitas = px.bar(
                receitas_por_categoria,
                x='mês',
                y='valor',
                color='categoria',
                title='Receitas por Categoria por Mês',
                labels={"valor": "Valor (R$)", "mês": "Mês"},
                barmode='group'
            )
            st.plotly_chart(bar_chart_receitas, use_container_width=True)

        investimentos_data = filtered_data[filtered_data["tipo"] == "Investimentos"]
        if not investimentos_data.empty:
            investimentos_por_categoria = investimentos_data.groupby(['mês', 'categoria'])['valor'].sum().reset_index()
            bar_chart_investimentos = px.bar(
                investimentos_por_categoria,
                x='mês',
                y='valor',
                color='categoria',
                title='Investimentos por Categoria por Mês',
                labels={"valor": "Valor (R$)", "mês": "Mês"},
                barmode='group'
            )
            st.plotly_chart(bar_chart_investimentos, use_container_width=True)
