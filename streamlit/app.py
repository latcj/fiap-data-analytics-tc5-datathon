"""
App Streamlit do Datathon Passos Mágicos.

Usa o modelo treinado no notebook 02 pra estimar a probabilidade de um aluno
entrar em risco de defasagem no ano seguinte, a partir dos indicadores do ano atual.
"""
import os
import pickle

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Passos Mágicos — Risco de Defasagem", page_icon="✨", layout="wide")

FEATURES_NUM = [
    "ian", "ida", "ieg", "iaa", "ips", "ipp", "ipv", "inde",
    "fase_ord", "idade", "ano_ingresso", "pedra_ord", "n_avaliacoes",
]
FEATURES_CAT = ["genero", "instituicao_ensino"]

CAMINHO_MODELO = os.path.join(os.path.dirname(__file__), "risk_model.pkl")


@st.cache_resource
def carregar_modelo():
    with open(CAMINHO_MODELO, "rb") as f:
        return pickle.load(f)


def prever(dados, modelo_salvo):
    """Monta as mesmas colunas usadas no treino e devolve a probabilidade de risco."""
    X = pd.get_dummies(dados[FEATURES_NUM + FEATURES_CAT], columns=FEATURES_CAT)
    X = X.reindex(columns=modelo_salvo["colunas"], fill_value=0)
    return modelo_salvo["modelo"].predict_proba(X)[:, 1]


def classificar(p):
    if p >= 0.66:
        return "Alto risco", "#ED3237"
    if p >= 0.4:
        return "Risco moderado", "#F58334"
    return "Baixo risco", "#37CD8F"


st.title("✨ Passos Mágicos — Risco de Defasagem")
st.caption(
    "Estima a probabilidade de um aluno entrar em risco de defasagem (IAN < 5 ou defasagem "
    "negativa) no ano seguinte, com base nos indicadores do ano atual."
)

try:
    modelo_salvo = carregar_modelo()
except FileNotFoundError:
    st.error("Modelo não encontrado. Rode o notebook `notebooks/02_model_training.ipynb` primeiro.")
    st.stop()

aba_aluno, aba_lote, aba_sobre = st.tabs(
    ["Avaliar um aluno", "Avaliar em lote (CSV)", "Sobre o modelo"]
)

with aba_aluno:
    st.subheader("Indicadores do aluno (ano atual)")
    col1, col2, col3 = st.columns(3)

    with col1:
        ian = st.slider("IAN — Adequação ao Nível", 0.0, 10.0, 6.5, 0.1)
        ida = st.slider("IDA — Desempenho Acadêmico", 0.0, 10.0, 6.0, 0.1)
        ieg = st.slider("IEG — Engajamento", 0.0, 10.0, 6.0, 0.1)
        iaa = st.slider("IAA — Autoavaliação", 0.0, 10.0, 7.0, 0.1)

    with col2:
        ips = st.slider("IPS — Psicossocial", 0.0, 10.0, 6.0, 0.1)
        ipp = st.slider("IPP — Psicopedagógico", 0.0, 10.0, 6.0, 0.1)
        ipv = st.slider("IPV — Ponto de Virada", 0.0, 10.0, 6.5, 0.1)
        inde = st.slider("INDE — Nota geral", 0.0, 10.0, 6.5, 0.1)

    with col3:
        fase_ord = st.selectbox(
            "Fase", options=list(range(0, 9)), index=3,
            format_func=lambda x: "ALFA" if x == 0 else str(x),
        )
        idade = st.number_input("Idade", min_value=5, max_value=25, value=12)
        ano_ingresso = st.number_input("Ano de ingresso", min_value=2010, max_value=2024, value=2020)
        pedra_ord = st.selectbox(
            "Pedra atual", options=[1, 2, 3, 4], index=2,
            format_func=lambda x: {1: "Quartzo", 2: "Ágata", 3: "Ametista", 4: "Topázio"}[x],
        )
        n_avaliacoes = st.number_input("Nº de avaliações no ano", min_value=0, max_value=10, value=4)
        genero = st.selectbox("Gênero", ["Feminino", "Masculino"])
        instituicao_ensino = st.selectbox(
            "Instituição de ensino", ["Escola Pública", "Pública", "Privada", "Rede Decisão"]
        )

    entrada = pd.DataFrame([{
        "ian": ian, "ida": ida, "ieg": ieg, "iaa": iaa, "ips": ips, "ipp": ipp,
        "ipv": ipv, "inde": inde, "fase_ord": fase_ord, "idade": idade,
        "ano_ingresso": ano_ingresso, "pedra_ord": pedra_ord, "n_avaliacoes": n_avaliacoes,
        "genero": genero, "instituicao_ensino": instituicao_ensino,
    }])

    if st.button("Calcular risco", type="primary"):
        proba = float(prever(entrada, modelo_salvo)[0])
        rotulo, cor = classificar(proba)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Probabilidade de risco no próximo ano", f"{proba * 100:.1f}%")
            st.markdown(f"<h3 style='color:{cor}'>{rotulo}</h3>", unsafe_allow_html=True)
        with c2:
            st.progress(min(max(proba, 0.0), 1.0))
            if proba >= 0.66:
                st.warning("Vale priorizar esse aluno para acompanhamento psicopedagógico.")
            elif proba >= 0.4:
                st.info("Aluno em zona de atenção — vale acompanhar a evolução do IAN e do IPV.")
            else:
                st.success("Aluno com baixo risco de defasagem no próximo ciclo.")

with aba_lote:
    st.subheader("Avaliação em lote a partir de um CSV")
    st.markdown("O arquivo precisa ter as colunas: `" + "`, `".join(FEATURES_NUM + FEATURES_CAT) + "`")

    arquivo = st.file_uploader("Selecione um arquivo CSV", type=["csv"])
    if arquivo is not None:
        dados = pd.read_csv(arquivo)
        faltando = [c for c in FEATURES_NUM + FEATURES_CAT if c not in dados.columns]

        if faltando:
            st.error(f"Colunas ausentes no arquivo: {faltando}")
        else:
            dados["probabilidade_risco"] = prever(dados, modelo_salvo)
            dados["classificacao"] = dados["probabilidade_risco"].apply(lambda p: classificar(p)[0])

            st.dataframe(
                dados.sort_values("probabilidade_risco", ascending=False),
                use_container_width=True,
            )
            st.download_button(
                "Baixar resultados (CSV)",
                dados.to_csv(index=False).encode("utf-8"),
                file_name="resultado_risco_defasagem.csv",
                mime="text/csv",
            )
            st.bar_chart(dados["classificacao"].value_counts())

with aba_sobre:
    st.markdown("""
### Sobre o modelo

- **Base de dados:** pesquisas PEDE da Associação Passos Mágicos (2022, 2023 e 2024).
- **Alvo:** o aluno é marcado como "em risco" se, no ano seguinte ao dos indicadores usados como
  entrada, ele tiver defasagem negativa ou IAN abaixo de 5.
- **Modelo:** Random Forest (scikit-learn), treinado no notebook `02_model_training.ipynb`.
- **Resultado no conjunto de teste (273 alunos):** acurácia de 80%, recall de 83% e precisão
  de 78% para a classe "em risco". A regressão logística testada em comparação ficou em 77%
  de acurácia.

Essa é uma ferramenta de apoio — o julgamento da equipe pedagógica e psicossocial deve sempre
prevalecer sobre a previsão do modelo.
""")
