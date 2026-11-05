# Dashboard de empreitadas e investimento (contratação pública)

Dashboard em **Power BI** alimentado por um pipeline em **Python** e uma base de dados **SQLite**, sobre contratos públicos de empreitadas celebrados entre dezembro de 2025 e outubro de 2026.

<img width="1292" height="734" alt="image" src="https://github.com/user-attachments/assets/b20e8f49-e398-4da1-a153-ddb317d8727a" />



## O que o dashboard mostra

- **Total investido:** montante global contratado em obras públicas (3,82 bn€).
- **Volume de obras:** número de empreitadas adjudicadas (cerca de 10 mil).
- **Valor e prazo médios:** custo médio por empreitada e prazo médio de execução.
- **Poupança total:** diferença entre o preço base e o preço contratual.
- **Tipos de procedimento:** distribuição do investimento por concurso público, ajuste direto, consulta prévia e outros.
- **Distribuição geográfica:** onde as obras são executadas, no continente e nas ilhas.
- **Evolução mensal:** ritmo do investimento ao longo do período.

## Arquitetura

1. **Extração e tratamento (`etl_obras.py`):** lê o ficheiro de contratos, filtra as empreitadas, converte tipos (preços e datas), remove registos sem preço contratual e grava a tabela `fact_empreitadas`.
2. **Modelação (`views.sql`):** views analíticas sobre a base SQLite:
   - `vw_top_empreiteiros`: ranking nacional de adjudicatários por valor adjudicado.
   - `vw_evolucao_mensal`: investimento mensal e variação percentual face ao mês anterior (MoM).
3. **Visualização (`Dashboard_Obras_Publicas_2026.pbix`):** relatório Power BI com tema escuro, cartões de KPI personalizados e mapa em tons de azul.

## Critério de filtragem

São consideradas empreitadas os contratos cujo tipo contém "obra" ou "empreitada", ou cujo código CPV começa por 45 (trabalhos de construção). Contratos sem preço contratual são excluídos.

## Dados

Fonte: [Contratos públicos – Portal BASE (IMPIC), contratos de 2012 a 2026](https://dados.gov.pt/pt/datasets/contratos-publicos-portal-base-impic-contratos-de-2012-a-2026), em dados.gov.pt.
Ficheiro usado: `Contratos2026.json` (cerca de 570 MB, por isso não está incluído neste repositório). Data de extração: 29/10/2026.

## Como correr

1. Descarregar o ficheiro de contratos de 2026 da fonte acima e colocá-lo na pasta do projeto como `Contratos2026.json`.
2. Instalar a dependência: `pip install pandas`
3. Correr o pipeline: `python etl_obras.py` (gera `obras_publicas.db`).
4. Executar `views.sql` sobre a base de dados para criar as views (por exemplo, no DB Browser for SQLite).
5. Abrir o `.pbix` no Power BI Desktop e atualizar a origem de dados, se for preciso.

## Limitações

- Um contrato celebrado não equivale a uma obra concluída.
- Os valores dependem de como a fonte regista o preço contratual e as modificações aos contratos.
- O dashboard mostra o panorama geral. O ranking de adjudicatários e a variação mensal estão disponíveis na base de dados, mas não no relatório.
- A variação mensal do primeiro e do último mês pode ser enganadora se esses meses estiverem incompletos.

## Autor

Mateus Pereira
