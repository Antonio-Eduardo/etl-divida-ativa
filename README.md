# ETL - Dívida Ativa Não Previdenciária (PGFN)

Pipeline ETL para processamento dos dados públicos de dívida ativa não previdenciária da Procuradoria-Geral da Fazenda Nacional (PGFN).

## Fonte dos dados

Os dados são disponibilizados publicamente em:
https://dadosabertos.pgfn.gov.br/

O arquivo utilizado é o `Dados_abertos_Nao_Previdenciario.zip`, que contém 6 arquivos CSV separados por `;` com encoding `latin1`, totalizando aproximadamente 42 milhões de linhas e 8GB de dados.

## Estrutura do projeto

```
etl-pgfn/
├── .env                  # credenciais do banco (não vai ao git)
├── .gitignore
├── requirements.txt
├── main.py               # orquestra o pipeline E → T → L
├── data/
│   └── raw/              # local para armazenar os CSVs originais
└── src/
    ├── extract.py        # leitura dos arquivos CSV
    ├── transform.py      # limpeza e transformação dos dados
    └── load.py           # carregamento no PostgreSQL
```

## Como executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as credenciais do banco:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha
```

### 3. Baixar os dados

Acesse https://dadosabertos.pgfn.gov.br/ e baixe o arquivo `Dados_abertos_Nao_Previdenciario.zip`. Extraia os CSVs e atualize o caminho no `main.py`.

### 4. Executar o pipeline

```bash
python main.py
```

## Stack

| Biblioteca | Função |
|---|---|
| `pandas` | Leitura e transformação dos CSVs |
| `sqlalchemy` | Conexão com o PostgreSQL |
| `psycopg2-binary` | Driver do PostgreSQL para Python |
| `python-dotenv` | Leitura das credenciais do `.env` |

## Decisões técnicas

### Separação em extract / transform / load
Cada etapa do pipeline tem seu próprio arquivo com responsabilidade única. Isso facilita a manutenção — se o banco mudar, só o `load.py` precisa ser alterado.

### Credenciais no `.env`
A senha do banco nunca entra no código-fonte nem vai ao repositório. O `.env` está no `.gitignore`.

### Encoding `latin1`
Arquivos do governo brasileiro geralmente usam `latin1` (ISO-8859-1), o encoding padrão do Windows, em vez de `UTF-8`.

### Processamento arquivo por arquivo
A tentativa inicial era carregar os 6 arquivos de uma vez com `pd.concat()`. Isso causou `MemoryError` pois os dados descomprimidos excedem a RAM disponível. A solução foi processar um arquivo por vez no loop do `main.py`, usando `if_exists="replace"` no primeiro e `if_exists="append"` nos demais.

## Transformações aplicadas

| Coluna | Tipo original | Tipo final | Motivo |
|---|---|---|---|
| `DATA_INSCRICAO` | str | datetime | Permite filtros e cálculos por data |
| `INDICADOR_AJUIZADO` | str (SIM/NAO) | bool | Ocupa menos espaço, consultas mais limpas |
| `NUMERO_INSCRICAO` | float64 | str | É um código identificador, não um valor numérico |
| Colunas de texto | object | object | Aplicado `.strip()` para remover espaços nas bordas |

## O que falta

- [ ] Adicionar logs para acompanhar o progresso do pipeline (ex: `logging`)
- [ ] Tratar erros por arquivo — se um falhar, continuar nos demais
- [ ] Automatizar o download e extração do ZIP da fonte
- [ ] Criar índices no PostgreSQL para otimizar consultas
- [ ] Agendar execução periódica (ex: cron job trimestral, seguindo o calendário da PGFN)
