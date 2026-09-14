import streamlit as st
from supabase import create_client, Client

# --- CONEXÃO COM O SUPABASE ---

@st.cache_resource
def get_supabase_client() -> Client:
    """Cria e faz cache do cliente oficial do Supabase."""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao inicializar cliente Supabase: {e}")
        return None

# --- BUSCAS DE DADOS ---

@st.cache_data(ttl=10)
def get_equipamentos():
    """Busca a frota e anexa os dados de antenas e monitores."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        # Busca equipamentos
        res_eq = supabase.table("Equipamentos").select("id, codigo_do_equipamento, nome, antena, monitor, nav").order("codigo_do_equipamento").execute()
        equipamentos = res_eq.data or []

        # Busca antenas e monitores
        res_antenas = supabase.table("Antenas").select("*").execute()
        res_monitores = supabase.table("Monitores").select("*").execute()

        antenas_list = res_antenas.data or []
        monitores_list = res_monitores.data or []

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
    """Rastreamento de status de vínculo do componente."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        pecas_res = supabase.table(tabela).select("*").execute()
        frota_res = supabase.table("Equipamentos").select("codigo_do_equipamento, antena, monitor, nav").execute()

        pecas = pecas_res.data or []
        frota = frota_res.data or []

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
        st.error(f"Erro ao processar status e vínculos em {tabela}: {e}")
        return []


@st.cache_data(ttl=10)
def get_licencas_simples():
    """Busca as licenças ordenadas pela data de vencimento."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        res = supabase.table("Licencas_Validades").select("*").order("data_vencimento").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar licenças: {e}")
        return []


@st.cache_data(ttl=10)
def get_tabela_simples(tabela):
    """Busca registros brutos de qualquer tabela."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        res = supabase.table(tabela).select("*").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Erro ao buscar tabela {tabela}: {e}")
        return []


# --- OPERAÇÕES DE BANCO (CRUD) ---

def get_itens_disponiveis(tabela, coluna_serie, valor_atual=None):
    """Filtra itens para o selectbox de edição."""
    try:
        todos = get_itens_com_status(tabela, coluna_serie)
        return [
            i for i in todos
            if i["disponivel"] or str(i[coluna_serie]) == str(valor_atual)
        ]
    except Exception:
        return []


def add_registro(tabela, dados):
    """Insere novos registros."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        res = supabase.table(tabela).insert(dados).execute()
        if res.data:
            st.cache_data.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao inserir em {tabela}: {e}")
        return False


def update_equipamento(equip_id, dados):
    """Atualiza equipamento."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        colunas_validas = ["nome", "antena", "monitor", "nav"]
        payload = {k: v for k, v in dados.items() if k in colunas_validas}

        res = supabase.table("Equipamentos").update(payload).eq("id", int(equip_id)).execute()
        if res.data:
            st.cache_data.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao atualizar equipamento: {e}")
        return False


def update_registro_generico(tabela, item_id, dados):
    """Atualiza Antenas, Monitores, Navs ou Licenças."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        payload = dict(dados)
        if "id" in payload:
            del payload["id"]  # Evita tentar atualizar a chave primária

        res = supabase.table(tabela).update(payload).eq("id", int(item_id)).execute()
        if res.data:
            st.cache_data.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Erro ao atualizar em {tabela}: {e}")
        return False


def delete_registro(tabela, item_id):
    """Remove um registro pelo ID."""
    if item_id is None:
        st.error("Erro: Não foi possível capturar o identificador (ID) para exclusão.")
        return False

    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        res = supabase.table(tabela).delete().eq("id", int(item_id)).execute()
        if res.data:
            st.cache_data.clear()
            return True
        return False
    except ValueError:
        st.error(f"Erro: O ID precisa ser numérico. Recebido: {item_id}")
        return False
    except Exception as e:
        st.error(f"Erro ao excluir registro de {tabela}: {e}")
        return False


def verificar_login(usuario, senha):
    """Validação de acesso simples contra a tabela 'usuarios'."""
    supabase = get_supabase_client()
    if not supabase:
        print("Erro: Cliente Supabase não inicializado.")
        return False

    try:
        # Garante que ambos os parâmetros sejam enviados como String para o Supabase (text)
        usr_str = str(usuario).strip()
        pwd_str = str(senha).strip()

        res = (
            supabase.table("usuarios")
            .select("*")
            .eq("usuarios", usr_str)
            .eq("senha", pwd_str)
            .execute()
        )
        
        return len(res.data) > 0

    except Exception as e:
        print(f"Erro ao verificar login no Supabase: {e}")
        return False
