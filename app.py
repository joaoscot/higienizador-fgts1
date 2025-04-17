import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Higienizador de Saldos FGTS", layout="wide")
st.title("📥 Higienização de Saldos FGTS via API")

# Simulação da consulta real à API
def consultar_api(cpf):
    nomes = ["João", "Maria", "Carlos", "Ana", "Fernanda", "Pedro"]
    nome = random.choice(nomes) + " " + str(random.randint(100, 999))
    saldo = round(random.uniform(0, 3000), 2)
    pode_antecipar = saldo >= 500
    return {
        "cpf": cpf,
        "nome": nome,
        "saldo": saldo,
        "pode_antecipar": pode_antecipar
    }

uploaded_file = st.file_uploader("📎 Envie a planilha com a coluna 'CPF'", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if "CPF" not in df.columns:
            st.error("❌ A planilha deve conter uma coluna chamada 'CPF'")
        else:
            st.success("✅ Planilha carregada com sucesso.")
            resultado = []

            with st.spinner("Consultando saldos..."):
                for cpf in df["CPF"]:
                    res = consultar_api(str(cpf))
                    resultado.append(res)
                    time.sleep(0.2)  # simula tempo de resposta da API

            df_resultado = pd.DataFrame(resultado)

            df_resultado["status"] = df_resultado["pode_antecipar"].apply(lambda x: "Sim" if x else "Não")

            st.subheader("📊 Resultado da Higienização")
            st.dataframe(df_resultado, use_container_width=True)

            # Dashboard
            st.markdown("---")
            st.subheader("📈 Dashboard")
            total = len(df_resultado)
            com_saldo = df_resultado[df_resultado["pode_antecipar"] == True]
            media_saldo = com_saldo["saldo"].mean()

            col1, col2, col3 = st.columns(3)
            col1.metric("CPFs consultados", total)
            col2.metric("Com saldo disponível", len(com_saldo))
            col3.metric("Média de saldo (R$)", f"{media_saldo:,.2f}")

            # Download dos dados
            csv = df_resultado.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Baixar resultado em CSV", data=csv, file_name="resultado_fgts.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Erro ao processar a planilha: {e}")
