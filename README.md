# Datathon FIAP - Fase 5 - Passos Mágicos

## Objetivo

Analisar os dados da pesquisa PEDE (2022-2024) da Associação Passos Mágicos para entender o
impacto do programa no desempenho dos alunos, e desenvolver um modelo de Machine Learning capaz
de prever quais alunos correm risco de defasagem escolar no ano seguinte, auxiliando a equipe
pedagógica na priorização do acompanhamento.


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
│
├── notebooks/
│   ├── 01_eda.ipynb                 # exploração dos dados
│   ├── 02_model_training.ipynb      # modelo preditivo
│   └── 03_analise_perguntas.ipynb   # respostas às 11 perguntas
│
├── src/
│   └── data_cleaning.py
│
├── streamlit/
│   ├── app.py
│   └── risk_model.pkl
│
├── presentation/
│   ├── Passos_Magicos_Datathon.pptx
│   └── assets_v3/                   # gráficos gerados pelo notebook 03
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
- Avaliação realizada utilizando conjunto de teste separado do treinamento, com `stratify`
  para manter a mesma proporção de alunos em risco nos dois conjuntos.

## Resultados da análise

1. **IAN** melhora de forma consistente nos 3 anos (6,42 → 7,68); defasagem severa cai de 3,3%
   para 0,3% dos alunos.
2. **IDA** oscila (6,09 → 6,66 → 6,35), sem tendência linear como o IAN; fases intermediárias
   (2 e 3) ficam com desempenho mais baixo nos três anos.
3. **IEG** tem relação moderada com IDA (r=0,54) e IPV (r=0,56).
4. **IAA** tem correlação baixa com o desempenho real (r=0,12) - os alunos tendem a se
   autoavaliar acima do que realmente performam.
5. **IPS** do ano anterior é um pouco mais baixo entre alunos que caem de desempenho, mas é um
   sinal parcial, não isolado.
6. **IPP** confirma a defasagem do IAN direcionalmente, mas com relação fraca - são indicadores
   complementares.
7. **IPV** é mais influenciado por IPP, IEG e IDA.
8. **INDE** é mais puxado por IDA, IEG e IPV.
9. **Efetividade do programa:** Quartzo cai de 15,3% para 10,6%; Topázio sobe de 15,1% para
   30,9% ao longo dos 3 anos.

## Autor

Luiz Carvalho
Pós-graduação em Data Analytics - FIAP
