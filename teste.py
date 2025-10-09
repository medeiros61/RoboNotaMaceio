import pandas as pd
df = pd.read_excel(
  "PLANILHA EMISSAO NOVA 2025.xlsx",
  usecols=["CPF", "NOME", "CEP", "Nº", "VALOR", "DATA", "STATUS NF", "FORMA"],
  skiprows=1
)
# Itera sobre as linhas da planilha
for index, row in df.iterrows():
  cpf = str(row["CPF"])
  if cpf.endswith('.0'):
    cpf = cpf[:-2]
  nome = row["NOME"]
  cep = row["CEP"]
  numero = row["Nº"]
  valor = row["VALOR"]
  data = row["DATA"]
  status_nf = row["STATUS NF"]
  forma = row["FORMA"]
  print(cpf)
  df.at[index, "STATUS NF"] = "processado"
  if pd.isna(cpf):
    print("fim")
    break
    
  
df.to_excel("PLANILHA EMISSAO NOVA 2025_processada.xlsx", index=False)
