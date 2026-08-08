"""
Funcoes pra juntar as 3 abas da planilha oficial (PEDE2022, PEDE2023,
PEDE2024) numa unica tabela, ja que os nomes das colunas mudam de ano pra
ano. Uso isso no notebook 01 (EDA) e no notebook 02 (modelo).
"""

from __future__ import annotations

import os
import re
import numpy as np
import pandas as pd

# caminho montado a partir da pasta deste arquivo (src/), e nao da pasta de onde
# o notebook foi aberto - assim funciona igual no Jupyter, no VS Code e no terminal
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(RAIZ, "data", "raw", "BASE_DADOS_PEDE_2024_DATATHON.xlsx")

# Mapas de coluna -> nome padronizado, um por ano (aba)
COLMAP_2022 = {
    "RA": "ra",
    "Fase": "fase",
    "Turma": "turma",
    "Nome": "nome",
    "Ano nasc": "ano_nascimento",
    "Idade 22": "idade",
    "Gênero": "genero",
    "Ano ingresso": "ano_ingresso",
    "Instituição de ensino": "instituicao_ensino",
    "Pedra 20": "pedra_2020",
    "Pedra 21": "pedra_2021",
    "Pedra 22": "pedra",
    "INDE 22": "inde",
    "Cg": "cg",
    "Cf": "cf",
    "Ct": "ct",
    "Nº Av": "n_avaliacoes",
    "IAA": "iaa",
    "IEG": "ieg",
    "IPS": "ips",
    "Rec Psicologia": "rec_psicologia",
    "IDA": "ida",
    "Matem": "nota_mat",
    "Portug": "nota_por",
    "Inglês": "nota_ing",
    "Indicado": "indicado_bolsa",
    "Atingiu PV": "atingiu_pv",
    "IPV": "ipv",
    "IAN": "ian",
    "Fase ideal": "fase_ideal",
    "Defas": "defasagem",
    "Destaque IEG": "destaque_ieg",
    "Destaque IDA": "destaque_ida",
    "Destaque IPV": "destaque_ipv",
}

COLMAP_2023 = {
    "RA": "ra",
    "Fase": "fase",
    "INDE 2023": "inde",
    "Pedra 2023": "pedra",
    "Turma": "turma",
    "Nome Anonimizado": "nome",
    "Data de Nasc": "data_nascimento",
    "Idade": "idade",
    "Gênero": "genero",
    "Ano ingresso": "ano_ingresso",
    "Instituição de ensino": "instituicao_ensino",
    "Pedra 20": "pedra_2020",
    "Pedra 21": "pedra_2021",
    "Pedra 22": "pedra_2022",
    "Cg": "cg",
    "Cf": "cf",
    "Ct": "ct",
    "Nº Av": "n_avaliacoes",
    "IAA": "iaa",
    "IEG": "ieg",
    "IPS": "ips",
    "IPP": "ipp",
    "Rec Psicologia": "rec_psicologia",
    "IDA": "ida",
    "Mat": "nota_mat",
    "Por": "nota_por",
    "Ing": "nota_ing",
    "Indicado": "indicado_bolsa",
    "Atingiu PV": "atingiu_pv",
    "IPV": "ipv",
    "IAN": "ian",
    "Fase Ideal": "fase_ideal",
    "Defasagem": "defasagem",
    "Destaque IEG": "destaque_ieg",
    "Destaque IDA": "destaque_ida",
    "Destaque IPV": "destaque_ipv",
}

COLMAP_2024 = {
    "RA": "ra",
    "Fase": "fase",
    "INDE 2024": "inde",
    "Pedra 2024": "pedra",
    "Turma": "turma",
    "Nome Anonimizado": "nome",
    "Data de Nasc": "data_nascimento",
    "Idade": "idade",
    "Gênero": "genero",
    "Ano ingresso": "ano_ingresso",
    "Instituição de ensino": "instituicao_ensino",
    "Pedra 20": "pedra_2020",
    "Pedra 21": "pedra_2021",
    "Pedra 22": "pedra_2022",
    "Cg": "cg",
    "Cf": "cf",
    "Ct": "ct",
    "Nº Av": "n_avaliacoes",
    "IAA": "iaa",
    "IEG": "ieg",
    "IPS": "ips",
    "IPP": "ipp",
    "Rec Psicologia": "rec_psicologia",
    "IDA": "ida",
    "Mat": "nota_mat",
    "Por": "nota_por",
    "Ing": "nota_ing",
    "Indicado": "indicado_bolsa",
    "Atingiu PV": "atingiu_pv",
    "IPV": "ipv",
    "IAN": "ian",
    "Fase Ideal": "fase_ideal",
    "Defasagem": "defasagem",
    "Destaque IEG": "destaque_ieg",
    "Destaque IDA": "destaque_ida",
    "Destaque IPV": "destaque_ipv",
    "Escola": "escola",
}

KEEP_COLS = [
    "ra", "ano_pesquisa", "fase", "turma", "genero", "idade", "ano_ingresso",
    "instituicao_ensino", "pedra", "inde", "iaa", "ieg", "ips", "ipp", "ida",
    "ipv", "ian", "nota_mat", "nota_por", "nota_ing", "indicado_bolsa",
    "atingiu_pv", "fase_ideal", "defasagem", "rec_psicologia", "cg", "cf",
    "ct", "n_avaliacoes", "destaque_ieg", "destaque_ida", "destaque_ipv",
]

FASE_ORDER = {
    "ALFA": 0,
    "0": 0,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
}

PEDRA_ORDER = {"Quartzo": 1, "Ágata": 2, "Ametista": 3, "Topázio": 4}


def _clean_sheet(df: pd.DataFrame, colmap: dict, ano: int) -> pd.DataFrame:
    df = df.rename(columns=colmap)
    # remove colunas duplicadas geradas por cabecalhos repetidos na planilha
    df = df.loc[:, ~df.columns.duplicated()]
    df["ano_pesquisa"] = ano
    for c in KEEP_COLS:
        if c not in df.columns:
            df[c] = np.nan
    df = df[KEEP_COLS]
    df = df[df["ra"].notna()].copy()
    return df


def _normalize_fase(fase) -> str:
    if pd.isna(fase):
        return np.nan
    s = str(fase).strip().upper()
    if s.startswith("ALFA"):
        return "ALFA"
    m = re.search(r"\d+", s)
    return m.group(0) if m else s


def _to_bool(series: pd.Series) -> pd.Series:
    mapping = {"sim": True, "não": False, "nao": False, "true": True, "false": False}
    return series.astype(str).str.strip().str.lower().map(mapping)


def load_consolidated(raw_path: str = RAW_PATH) -> pd.DataFrame:
    """Le as 3 abas do arquivo oficial e retorna dataframe consolidado e limpo."""
    if not os.path.exists(raw_path):
        raise FileNotFoundError(
            f"Nao encontrei a planilha em:\n  {os.path.abspath(raw_path)}\n"
            f"Esperado: {RAW_PATH}"
        )
    sheets = pd.read_excel(raw_path, sheet_name=["PEDE2022", "PEDE2023", "PEDE2024"])

    df22 = _clean_sheet(sheets["PEDE2022"], COLMAP_2022, 2022)
    df23 = _clean_sheet(sheets["PEDE2023"], COLMAP_2023, 2023)
    df24 = _clean_sheet(sheets["PEDE2024"], COLMAP_2024, 2024)

    df = pd.concat([df22, df23, df24], ignore_index=True)

    # tipos numericos
    num_cols = ["idade", "ano_ingresso", "inde", "iaa", "ieg", "ips", "ipp",
                "ida", "ipv", "ian", "nota_mat", "nota_por", "nota_ing",
                "cg", "cf", "ct", "n_avaliacoes", "defasagem"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # normalizacoes categoricas
    df["fase_norm"] = df["fase"].apply(_normalize_fase)
    df["fase_ord"] = df["fase_norm"].map(FASE_ORDER)
    df["pedra"] = (
        df["pedra"].astype(str).str.strip()
        .replace({"nan": np.nan, "Agata": "Ágata", "INCLUIR": np.nan, "": np.nan})
    )
    df["pedra_ord"] = df["pedra"].map(PEDRA_ORDER)

    df["genero"] = (
        df["genero"].astype(str).str.strip().str.lower()
        .replace({
            "menina": "Feminino", "feminino": "Feminino", "f": "Feminino",
            "menino": "Masculino", "masculino": "Masculino", "m": "Masculino",
            "nan": np.nan,
        })
    )

    df["atingiu_pv"] = _to_bool(df["atingiu_pv"])
    df["indicado_bolsa"] = _to_bool(df["indicado_bolsa"])

    # duplicatas exatas
    df = df.drop_duplicates(subset=["ra", "ano_pesquisa"])

    # remove alunos sem nenhum indicador preenchido (linhas totalmente vazias)
    indicadores = ["inde", "iaa", "ieg", "ips", "ipp", "ida", "ipv", "ian"]
    df = df[df[indicadores].notna().any(axis=1)].reset_index(drop=True)

    return df


def build_risk_label(df: pd.DataFrame) -> pd.Series:
    """Marca 1 (em risco) quando o aluno tem defasagem negativa ou IAN < 5.
    Usei essa regra no notebook 02 pra treinar o modelo preditivo."""
    risco = (df["defasagem"] < 0) | (df["ian"] < 5)
    return risco.astype(int)
