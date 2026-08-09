# Tech Challenge 5 - Datathon - Passos Mágicos

## Objetivo

Analisar os dados da pesquisa PEDE (2022-2024) da Associação Passos Mágicos para entender o
impacto do programa no desempenho dos alunos, e desenvolver um modelo de Machine Learning capaz
de prever quais alunos correm risco de defasagem escolar no ano seguinte, auxiliando a equipe
pedagógica na priorização do acompanhamento.

## Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Scikit-Learn
- Random Forest
- Matplotlib
- Streamlit

## Estrutura do projeto

```
├── data/
│   └── raw/
│       └── BASE_DADOS_PEDE_2024_DATATHON.xlsx
│   └── processed/
│       └── pede_consolidado.csv
│
├── src/
│   └── data_cleaning.py
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_model_training.ipynb     
│   └── 03_analise_perguntas.ipynb
│
├── streamlit/
│   ├── app.py
│   └── risk_model.pkl
│
├── presentation/
│   ├── Passos_Magicos_Datathon.pptx
│   └── Passos_Magicos_Datathon.pdf
│
├── requirements.txt
└── README.md
```

## Execução local

Instale as dependências:

```
pip install -r requirements.txt
```

Execute a aplicação:

```
streamlit run streamlit/app.py
```

## Organização dos notebooks

- **`01_eda.ipynb`** — exploração inicial: formato da base, tipos, valores faltantes,
  duplicatas, distribuições e correlações gerais.
- **`03_analise_perguntas.ipynb`** — responde uma a uma as 11 perguntas do desafio. Cada
  pergunta tem o código da análise, o gráfico gerado a partir dele e a resposta. Os gráficos
  salvos aqui são exatamente os que aparecem na apresentação.
- **`02_model_training.ipynb`** — feature engineering, separação treino/teste, modelagem e
  avaliação do modelo de risco de defasagem.

## Sobre o modelo

- **Problema:** prever, a partir dos indicadores de um ano, se o aluno vai entrar em risco de
  defasagem no ano seguinte.
- **Alvo:** aluno marcado como "em risco" quando, no ano seguinte, apresenta defasagem negativa
  ou IAN abaixo de 5.
- **Features:** sempre do ano atual, nunca do ano-alvo, para evitar vazamento de dados.
- **Modelos testados:** Regressão Logística (77% de acurácia) e Random Forest (80%).
- **Modelo escolhido:** Random Forest.
- **Resultado no conjunto de teste (273 alunos):** acurácia 80%, recall 83% e precisão 78%
  para a classe "em risco".
  
## Resultados da análise
| # | Pergunta | Resposta curta |
|---|---|---|
| 1 | **Perfil de defasagem (IAN)** | Melhora clara: defasagem severa quase zerada, IAN 6,42 → 7,68 |
| 2 | **Desempenho (IDA)** | Estagnado; vale nas fases 2 e 3 |
| 3 | **Engajamento (IEG)** | Relação moderada com IDA e IPV |
| 4 | **Autoavaliação (IAA)** | Pouco coerente com o desempenho real; otimista demais |
| 5 | **Psicossocial (IPS)** | Sinal fraco, serve só em conjunto |
| 6 | **Psicopedagógico (IPP)** | Confirma o IAN na direção, mas com relação fraca |
| 7 | **Ponto de virada (IPV)** | Puxado por IPP e IEG |
| 8 | **Multidimensionalidade** | INDE puxado por IDA/IEG/IPV; efeito cumulativo |
| 9 | **Previsão de risco** | Grupos já se separam um ano antes (ver notebook 02) |
| 10 | **Efetividade** | Sim: Quartzo cai, Topázio mais que dobra |
| 11 | **Insights** | Evasão seletiva e gargalo na fase 3 |

## Links  

### [Aplicação Streamlit](https://fiap-tc5-risco-defasagem.streamlit.app//)

### [Vídeo de apresentação](https://www.youtube.com/watch?v=4z3HHzEyyTU)

## Autor

Luiz Carvalho

Pós-graduação em Data Analytics – FIAP
