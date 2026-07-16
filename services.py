import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

# --- CONEXÃO COM O POSTGRESQL (RENDER) ---

@st.cache_resource
def get_engine():
    """Cria e faz cache do engine de conexão com o PostgreSQL do Render."""
    try:
        pg = st.secrets["postgres"]
        db_url = f"postgresql://{pg['username']}:{pg['password']}@{pg['host']}:{pg['port']}/{pg['database']}"
        return create_engine(db_url)
    except Exception as e:
        st.error(f"Erro ao carregar credenciais do banco: {e}")
        return None

def executar_query(query, params=None, retornar_dados=True):
    """Auxiliar para executar comandos SQL de forma segura."""
    engine = get_engine()
    if not engine:
        return [] if retornar_dados else False
    
    try:
        with engine.begin() as conn:
            resultado = conn.execute(text(query), params or {})
            if retornar_dados:
                # Converte os resultados em uma lista de dicionários
                return [dict(row._mapping) for row in resultado]
            return True
    except Exception as e:
        st.error(f"Erro na execução da query: {e}")
        return [] if retornar_dados else False

# --- BUSCAS DE DADOS ---

@st.cache_data(ttl=10)
def get_equipamentos():
    """Busca a frota e anexa os modelos das peças."""
    try:
        # Busca equipamentos
        query_eq = "SELECT id, codigo_do_equipamento, nome, antena, monitor, nav FROM equipamentos ORDER BY codigo_do_equipamento"
        equipamentos = executar_query(query_eq)

        # Busca antenas e monitores para fazer o de-para
        antenas_list = executar_query("SELECT * FROM antenas")
        monitores_list = executar_query("SELECT * FROM monitores")

        antenas = {a["antena_serie"]: a for a in antenas_list if "antena_serie" in a}
        monitores = {m["monitor_serie"]: m for m in monitores_list if "monitor_serie" in m}

        dados_completos = []
        for eq in equipamentos:
            eq["Antenas"] = antenas.get(eq["antena"], {})
            eq["Monitores"] = monitores.get(eq["monitor"], {})
            dados_completos.append(eq)

        return dados_completos
    except Exception as e:
        st.error(f"Erro ao buscar frota: {e}")
        return []


@st.cache_data(ttl=10)
def get_itens_com_status(tabela, coluna_serie):
    """
    RASTREAMENTO TIPO VENCIMENTO:
    Identifica se a peça está em uso e por qual trator.
    """
    try:
        # Garante nome de tabela em minúsculo para o Postgres
        tabela_min = tabela.lower()
        pecas = executar_query(f"SELECT * FROM {tabela_min}")
        frota = executar_query("SELECT codigo_do_equipamento, antena, monitor, nav FROM equipamentos")

        mapa_vinculos = {}
        for trator in frota:
            cod = trator["codigo_do_equipamento"]
            if trator.get("antena"):
                mapa_vinculos[str(trator["antena"])] = cod
            if trator.get("monitor"):
                mapa_vinculos[str(trator["monitor"])] = cod
            if trator.get("nav"):
                mapa_vinculos[str(trator["nav"])] = cod

        for p in pecas:
            serie_atual = str(p.get(coluna_serie))
            p["vinculo"] = mapa_vinculos.get(serie_atual)
            p["disponivel"] = p["vinculo"] is None

        return pecas
    except Exception as e:
        st.error(f"Erro ao processar status e vínculos: {e}")
        return []


@st.cache_data(ttl=10)
def get_licencas_simples():
    """Busca as licenças para a página de vencimentos."""
    query = "SELECT * FROM licencas_validades ORDER BY data_vencimento"
    return executar_query(query)


@st.cache_data(ttl=10)
def get_tabela_simples(tabela):
    """Busca dados brutos de qualquer tabela auxiliar."""
    tabela_min = tabela.lower()
    query = f"SELECT * FROM {tabela_min}"
    return executar_query(query)


# --- OPERAÇÕES DE BANCO (CRUD) ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """Filtra itens para o SELECT de edição."""
    try:
        todos = get_itens_com_status(tabela, coluna_serie)
        return [
            i for i in todos
            if i["disponivel"] or str(i[coluna_serie]) == str(valor_atual)
        ]
    except Exception:
        return []


def add_registro(tabela, dados):
    """Insere novos registros no banco dinamicamente."""
    try:
        tabela_min = tabela.lower()
        colunas = ", ".join(dados.keys())
        valores_placeholder = ", ".join([f":{k}" for k in dados.keys()])
        
        query = f"INSERT INTO {tabela_min} ({colunas}) VALUES ({valores_placeholder})"
        
        sucesso = executar_query(query, dados, retornar_dados=False)
        if sucesso:
            st.cache_data.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao inserir: {e}")
        return False


def update_equipamento(equip_id, dados):
    """Atualiza equipamento."""
    try:
        colunas_validas = ["nome", "antena", "monitor", "nav"]
        payload = {k: v for k, v in dados.items() if k in colunas_validas}
        payload["id"] = equip_id

        set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys() if k != "id"])
        query = f"UPDATE equipamentos SET {set_clause} WHERE id = :id"

        sucesso = executar_query(query, payload, retornar_dados=False)
        if sucesso:
            st.cache_data.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False


def update_registro_generico(tabela, item_id, dados):
    """
    Atualiza Antenas, Monitores, Navs ou Licenças.
    """
    try:
        tabela_min = tabela.lower()
        payload = dict(dados)
        payload["id"] = item_id

        set_clause = ", ".join([f"{k} = :{k}" for k in dados.keys()])
        query = f"UPDATE {tabela_min} SET {set_clause} WHERE id = :id"

        sucesso = executar_query(query, payload, retornar_dados=False)
        if sucesso:
            st.cache_data.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao atualizar {tabela_min}: {e}")
        return False


def verificar_login(usuario, senha):
    """Validação de acesso simples contra a tabela 'usuarios'."""
    try:
        query = "SELECT * FROM usuarios WHERE usuarios = :usuario AND senha = :senha"
        res = executar_query(query, {"usuario": usuario, "senha": senha})
        return len(res) > 0
    except Exception:
        return False
