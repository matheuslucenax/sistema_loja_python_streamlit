from tinydb import TinyDB, where
import streamlit as st

db = TinyDB("loja.json")

estoque = db.table("estoque")
vendas  = db.table("vendas")

st.set_page_config(page_title="Sistema Loja", page_icon="🏪")
st.title("🏪 Sistema de Loja")

aba_estoque, aba_cadastro, aba_vender, aba_vendas = st.tabs(
    ["Estoque", "Cadastrar", "Vender", "Vendas"]
)

with aba_estoque:
    st.header("Estoque atual")

    produtos = estoque.all()
    if len(produtos) == 0:
        st.info("Estoque vazio. Cadastre um produto na aba ao lado!")
    else:
        st.table(produtos)
        st.metric("Total de produtos", len(produtos))

with aba_cadastro:
    st.header("Cadastrar produto")

    nome = st.text_input("Nome", key="cad_nome")
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.5, key="cad_preco")
    qtd = st.number_input("Quantidade", min_value=0, step=1,key="cad_qtd")

    if st.button("Cadastrar", type="primary"):
        estoque.insert({"nome": nome, "preco": float(preco), "qtd": int(qtd)})
        st.success("Produto cadastrado com sucesso!")

with aba_vender:
    st.header("Registrar venda")
    produtos = estoque.all()

    if len(produtos) == 0:
        st.info("Sem produtos para vender")
    else:
        nomes = [produto ["nome"] for produto in produtos if produto ["qtd"] > 0]
        if len(nomes) == 0:
            st.warning("Tudo zerado")
        else:
            escolhido = st.selectbox("Produto", nomes, key="v_prod")
            qtd_v = st.number_input("Quantidade", min_value=1, step=1, key="v_qtd")
            cliente = st.text_input("Cliente", key="v_cli")

            produto = estoque.get(where("nome") == escolhido)

            total = produto["preco"] * qtd_v

            if st.button("Confirmar venda",type="primary"):
                vendas.insert({
                    "produto": escolhido, "qtd": int(qtd_v), "total": total, "cliente": cliente
                })
                estoque.update({"qtd": produto["qtd"] - int(qtd_v)}, where("nome") == escolhido)

                st.success("Venda Registrada")
                st.balloons()

with aba_vendas:
    st.header("Histórico de vendas")
    lista = vendas.all()

    if len(lista) == 0:
        st.info("Sem vendas até o momento.")
    else:
        st.table(lista)
        
