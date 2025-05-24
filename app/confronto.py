import pandas as pd
from rapidfuzz import process, fuzz

def confronta_clienti(df1, df2, soglia_similarita=90):
    risultati = []

    def normalizza(nome):
        return nome.lower().replace(".", "").replace(",", "").replace(" srl", "").replace(" s.r.l.", "").strip()

    clienti_2 = df2["CLIENTE"].tolist()
    clienti_2_normalizzati = [normalizza(nome) for nome in clienti_2]

    for _, riga in df1.iterrows():
        nome_1 = riga["CLIENTE"]
        qf_1 = riga["QF"]
        nome_1_norm = normalizza(nome_1)

        match, punteggio, indice = process.extractOne(
            nome_1_norm, clienti_2_normalizzati, scorer=fuzz.ratio
        )

        if punteggio >= soglia_similarita:
            cliente_2 = df2.iloc[indice]["CLIENTE"]
            qf_2 = df2.iloc[indice]["QF"]
            stato = "CORRISPONDENTE"
        else:
            cliente_2 = "-"
            qf_2 = "-"
            stato = "NON TROVATO"

        risultati.append({
            "CLIENTE_T1": nome_1,
            "QF_T1": qf_1,
            "CLIENTE_T2_CORRISPONDENTE": cliente_2,
            "QF_T2": qf_2,
            "SIMILARITÀ": f"{punteggio:.0f}%",
            "STATO": stato
        })

    return pd.DataFrame(risultati)
