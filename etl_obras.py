# ==============================================================================
# BLOCO 1: IMPORTAR BIBLIOTECAS
# As bibliotecas são conjuntos de ferramentas pré-feitas que expandem o Python.
# ==============================================================================
import pandas as pd  # 'pandas' é a biblioteca principal para manipular dados em tabelas (DataFrames)
import sqlite3    # 'sqlite3' permite criar e gerir bases de dados SQL diretamente em ficheiro
import os         # 'os' ajuda a verificar se os ficheiros existem na pasta

print("=== INÍCIO DO PROCESSAMENTO ===")

# ==============================================================================
# BLOCO 2: CARREGAR OS DADOS BRUTOS
# Aqui lemos o ficheiro que descarregaste do portal e carregamo-lo em memória.
# ==============================================================================
# Ajusta o nome abaixo se o teu ficheiro for .xlsx ou .csv!
NOME_FICHEIRO = "Contratos2026.json" 

print(f"1. A carregar o ficheiro '{NOME_FICHEIRO}'...")

if NOME_FICHEIRO.endswith('.json'):
    df_bruto = pd.read_json(NOME_FICHEIRO)
elif NOME_FICHEIRO.endswith('.xlsx'):
    df_bruto = pd.read_excel(NOME_FICHEIRO)
else:
    df_bruto = pd.read_csv(NOME_FICHEIRO, sep=";", encoding="utf-8")

# Imprimir o tamanho inicial do conjunto de dados
print(f"   -> Sucesso! Carregados {len(df_bruto)} registos brutos.")

# ==============================================================================
# BLOCO 3: FILTRAR APENAS EMPREITADAS DE OBRAS PÚBLICAS
# Como o dataset contém todos os contratos, filtramos apenas os de Obras/CPV 45.
# ==============================================================================
print("2. A filtrar empreitadas de obras públicas...")

# Normalizar os nomes das colunas para minúsculas para evitar erros de escrita
df_bruto.columns = [col.lower().strip() for col in df_bruto.columns]

# Identificar a coluna do tipo de contrato e do CPV
coluna_tipo = 'tipocontrato' if 'tipocontrato' in df_bruto.columns else 'tipo_contrato'
coluna_cpv = 'cpv' if 'cpv' in df_bruto.columns else 'codigo_cpv'

# Criar a máscara de filtragem (condição lógica)
filtro_obras = (
    df_bruto[coluna_tipo].astype(str).str.contains('obra|empreitada', case=False, na=False) |
    df_bruto[coluna_cpv].astype(str).str.startswith('45', na=False)
)

# Aplicar o filtro e criar uma nova tabela (DataFrame) só com as obras
df_obras = df_bruto[filtro_obras].copy()
print(f"   -> Encontrados {len(df_obras)} registos de obras públicas.")

# ==============================================================================
# BLOCO 4: TRATAMENTO E LIMPEZA DE DADOS (FEATURE ENGINEERING)
# Aqui corrigimos os tipos de dados (texto -> número / texto -> data).
# ==============================================================================
print("3. A limpar e transformar os dados...")

# 4.1 Converter Preço Contratual para número decimal (float)
if 'precocontratual' in df_obras.columns:
    df_obras['precocontratual'] = pd.to_numeric(
        df_obras['precocontratual'].astype(str).str.replace(',', '.'), 
        errors='coerce'
    )

# 4.2 Converter Data de Celebração e extrair Ano e Mês
if 'datacelebracaocontrato' in df_obras.columns:
    df_obras['datacelebracaocontrato'] = pd.to_datetime(df_obras['datacelebracaocontrato'], errors='coerce')
    df_obras['ano_celebracao'] = df_obras['datacelebracaocontrato'].dt.year
    df_obras['mes_celebracao'] = df_obras['datacelebracaocontrato'].dt.month
    df_obras['mes_ano'] = df_obras['datacelebracaocontrato'].dt.to_period('M').astype(str)

# ==============================================================================
# BLOCO 4.3: TRATAMENTO DE VALORES COMPLEXOS (LISTAS) E NULOS
# ==============================================================================
# Remover registos sem preço
df_limpo = df_obras.dropna(subset=['precocontratual']).copy()

# Converter qualquer coluna que contenha listas ou dicionários em texto simples (string)
for col in df_limpo.columns:
    df_limpo[col] = df_limpo[col].apply(lambda x: str(x) if isinstance(x, (list, dict)) else x)


# ==============================================================================
# BLOCO 5: EXPORTAR PARA A BASE DE DADOS SQL
# ==============================================================================
print("4. A guardar os dados na base de dados SQLite 'obras_publicas.db'...")

# Conectar à base de dados SQLite
conexao = sqlite3.connect("obras_publicas.db")

# Gravar o DataFrame limpo na tabela 'fact_empreitadas'
df_limpo.to_sql("fact_empreitadas", conexao, if_exists="replace", index=False)

# Fechar a conexão
conexao.close()

print("=== PROCESSO CONCLUÍDO COM SUCESSO ===")
print("Ficheiro 'obras_publicas.db' gerado e pronto para consultas SQL!")