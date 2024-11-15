import sqlite3
import streamlit as st
from datetime import date

# Configuração inicial do Streamlit
st.set_page_config(page_title="Cantinho da Bia", layout="wide")

# Funções para manipulação do banco de dados
def init_db():
    conn = sqlite3.connect("cantinho_da_bia.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            tipo_bolo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            data_entrega DATE NOT NULL,
            observacoes TEXT,
            status TEXT DEFAULT 'Em andamento'
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_pedido(nome_cliente, tipo_bolo, quantidade, preco, data_entrega, observacoes):
    conn = sqlite3.connect("cantinho_da_bia.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedidos (nome_cliente, tipo_bolo, quantidade, preco, data_entrega, observacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome_cliente, tipo_bolo, quantidade, preco, data_entrega, observacoes))
    conn.commit()
    conn.close()

def listar_pedidos():
    conn = sqlite3.connect("cantinho_da_bia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def atualizar_pedido(id_pedido, nome_cliente, tipo_bolo, quantidade, preco, data_entrega, observacoes, status):
    conn = sqlite3.connect("cantinho_da_bia.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedidos
        SET nome_cliente = ?, tipo_bolo = ?, quantidade = ?, preco = ?, data_entrega = ?, observacoes = ?, status = ?
        WHERE id = ?
    """, (nome_cliente, tipo_bolo, quantidade, preco, data_entrega, observacoes, status, id_pedido))
    conn.commit()
    conn.close()

def excluir_pedido(id_pedido):
    conn = sqlite3.connect("cantinho_da_bia.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = ?", (id_pedido,))
    conn.commit()
    conn.close()

# Inicializando o banco de dados
init_db()

# Layout do app
st.sidebar.image("CANTINHO_DA_BIA.png", use_column_width=True)  # Adiciona a logo acima do menu lateral
menu = ["Cadastrar Pedido", "Visualizar Pedidos", "Editar Pedido", "Relatório de Pedidos"]
escolha = st.sidebar.selectbox("Menu", menu)

st.title("Cantinho da Bia - Gerenciamento de Pedidos de Bolos")

if escolha == "Cadastrar Pedido":
    st.header("Cadastrar Novo Pedido")
    nome_cliente = st.text_input("Nome do Cliente")
    tipo_bolo = st.selectbox("Tipo de Bolo", ["Chocolate", "Baunilha", "Red Velvet", "Cenoura", "Outros"])
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    preco = st.number_input("Preço Total (R$)", min_value=0.0, step=0.01, format="%.2f")
    data_entrega = st.date_input("Data de Entrega", min_value=date.today())
    observacoes = st.text_area("Observações (opcional)")
    
    if st.button("Cadastrar"):
        cadastrar_pedido(nome_cliente, tipo_bolo, quantidade, preco, data_entrega, observacoes)
        st.success("Pedido cadastrado com sucesso!")

elif escolha == "Visualizar Pedidos":
    st.header("Visualizar Pedidos")
    pedidos = listar_pedidos()
    for pedido in pedidos:
        st.write(f"**Número do Pedido:** {pedido[0]}")
        st.write(f"**Nome do Cliente:** {pedido[1]}")
        st.write(f"**Tipo de Bolo:** {pedido[2]}")
        st.write(f"**Quantidade:** {pedido[3]}")
        st.write(f"**Preço Total:** R$ {pedido[4]:.2f}")
        st.write(f"**Data de Entrega:** {pedido[5]}")
        st.write(f"**Status:** {pedido[7]}")
        st.write(f"**Observações:** {pedido[6] if pedido[6] else 'Nenhuma'}")
        st.write("---")

elif escolha == "Editar Pedido":
    st.header("Editar Pedido")
    pedidos = listar_pedidos()
    pedido_selecionado = st.selectbox("Selecione o Pedido", [f"{p[0]} - {p[1]}" for p in pedidos])
    if pedido_selecionado:
        id_pedido = int(pedido_selecionado.split(" - ")[0])
        pedido = [p for p in pedidos if p[0] == id_pedido][0]

        nome_cliente = st.text_input("Nome do Cliente", pedido[1])
        tipo_bolo = st.selectbox("Tipo de Bolo", ["Chocolate", "Baunilha", "Red Velvet", "Cenoura", "Outros"], index=["Chocolate", "Baunilha", "Red Velvet", "Cenoura", "Outros"].index(pedido[2]))
        quantidade = st.number_input("Quantidade", min_value=1, step=1, value=pedido[3])
        preco = st.number_input("Preço Total (R$)", min_value=0.0, step=0.01, format="%.2f", value=pedido[4])
        data_entrega = st.date_input("Data de Entrega", value=date.fromisoformat(pedido[5]))
        observacoes = st.text_area("Observações (opcional)", pedido[6])
        status = st.selectbox("Status", ["Em andamento", "Entregue", "Cancelado"], index=["Em andamento", "Entregue", "Cancelado"].index(pedido[7]))
        
        if st.button("Atualizar"):
            atualizar_pedido(id_pedido, nome_cliente, tipo_bolo, quantidade, preco, data_entrega, observacoes, status)
            st.success("Pedido atualizado com sucesso!")

elif escolha == "Relatório de Pedidos":
    st.header("Relatório de Pedidos")
    pedidos = listar_pedidos()
    st.table(pedidos)
