# ENTSO-E e OMIE Data Comparison Project

Projeto para buscar, processar e comparar dados de preços de eletricidade da ENTSO-E (European Network of Transmission System Operators) e OMIE (Operador del Mercado Ibérico de Energía).

## Descrição

Este projeto permite:
- **Buscar dados** da ENTSO-E via API oficial
- **Processar dados** do OMIE (arquivos .TXT)
- **Converter timezones** (CEST → UTC)
- **Comparar preços** entre as duas fontes
- **Gerar relatórios** de comparação

##Funcionalidades

### Busca de Dados ENTSO-E
- Preços day-ahead para Portugal e Espanha
- Dados de geração por tipo de fonte
- Período configurável (semana de 10/08/2025 a 16/08/2025)

###Processamento OMIE
- Parse de arquivos .TXT do OMIE
- Conversão automática de timezone (CEST → UTC)
- Extração de preços para PT e ES

### Comparação de Dados
- Alinhamento temporal por UTC
- Cálculo de diferenças e correlações
- Relatórios detalhados em CSV

## Tecnologias

- **Python 3.x**
- **pandas** - Manipulação de dados
- **entsoe-py** - Cliente oficial ENTSO-E API
- **pytz** - Tratamento de timezones
- **python-dotenv** - Configuração de variáveis

## Estrutura do Projeto

```
entso-e/
├── utils/
│   ├── entsoe_csv.py          # Busca dados ENTSO-E
│   ├── process_omie_data.py   # Processa dados OMIE
│   └── compare_entsoe_omie.py # Compara os dados
├── entsoe_data/               # Dados da ENTSO-E (CSV)
├── omie_data/                 # Dados processados OMIE (CSV)
├── comparison_reports/        # Relatórios de comparação
├── dadosomie/                 # Arquivos .TXT do OMIE
├── config.env                 # Configurações (API key, datas)
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## Configuração

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key
Crie um arquivo `config.env`:
```env
ENTSOE_API_KEY=sua_chave_api_aqui
START_DATE=2025-08-10
END_DATE=2025-08-16
```

### 3. Obter API Key ENTSO-E
- Acesse: https://transparency.entsoe.eu/
- Registre-se e solicite uma API key
- Adicione a chave no `config.env`

## Como Usar

### 1. Buscar Dados ENTSO-E
```bash
python utils/entsoe_csv.py
```

### 2. Processar Dados OMIE
```bash
python utils/process_omie_data.py
```

### 3. Comparar Dados
```bash
python utils/compare_entsoe_omie.py
```

## Saídas

### Dados ENTSO-E
- `entsoe_data/ENTSOE_Precos_PT_Semana_2025-08-10_a_2025-08-16.csv`
- `entsoe_data/ENTSOE_Precos_ES_Semana_2025-08-10_a_2025-08-16.csv`
- `entsoe_data/ENTSOE_Geracao_PT_Semana_2025-08-10_a_2025-08-16.csv`
- `entsoe_data/ENTSOE_Geracao_ES_Semana_2025-08-10_a_2025-08-16.csv`

### Dados OMIE Processados
- `omie_data/OMIE_Precos_Processados_10_08_a_16_08_2025.csv`

### Relatórios de Comparação
- `comparison_reports/comparison_report_[timestamp].csv`

## 🔍 Análise dos Resultados

O projeto gera relatórios com:
- **Preços alinhados** por timestamp UTC
- **Diferenças** entre ENTSO-E e OMIE
- **Correlações** entre as fontes
- **Estatísticas** descritivas

## Notas Importantes

- **Timezone**: Todos os dados são convertidos para UTC
- **MIBEL**: Portugal e Espanha compartilham mercado integrado
- **Formato**: CSV para compatibilidade com LibreOffice
- **Período**: Configurável via `config.env`


## 📄 Licença

Este projeto é de uso educacional e de pesquisa.

---

*Projeto desenvolvido para análise de dados de mercado de eletricidade europeu.*
