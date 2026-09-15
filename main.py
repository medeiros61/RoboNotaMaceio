from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import configparser


config = configparser.ConfigParser()
config.read('parametros.txt', encoding='utf-8')
parametros = dict(config['DEFAULT'])

Usuario = config.get('DEFAULT', 'Usuario')
Senha = config.get('DEFAULT', 'Senha')
nomeArquivo = config.get('DEFAULT', 'nomeArquivo')
Valor_Aliquota = config.get('DEFAULT', 'Valor_Aliquota')
cnpj = config.get('DEFAULT', 'cnpj')
tempoEspera = config.getint('DEFAULT', 'tempoEspera')
ambiente = config.get('DEFAULT', 'ambiente')

# Configuração do driver (certifique-se de ter o ChromeDriver instalado)
driver = webdriver.Chrome()


def buscar_elemento(by, valor, descricao):
  """Busca um elemento obrigatorio na pagina. Se nao encontrar, informa claramente
  qual campo/etapa falhou (provavelmente o site foi atualizado e o seletor mudou)."""
  try:
    return driver.find_element(by, valor)
  except NoSuchElementException:
    raise RuntimeError(
      f"Elemento nao encontrado: '{descricao}' (localizador: {by}='{valor}'). "
      "Provavel causa: o site do portal foi atualizado, a pagina nao terminou de carregar "
      "ou o layout mudou. Revise esse seletor no main.py."
    )


def buscar_elemento_opcional(by, valor, descricao):
  """Busca um elemento que pode nao existir (ex: popups eventuais). Se nao encontrar,
  apenas avisa e retorna None, sem interromper a execucao."""
  try:
    return driver.find_element(by, valor)
  except NoSuchElementException:
    print(
      f"AVISO: elemento opcional nao encontrado: '{descricao}' (localizador: {by}='{valor}'). "
      "Provavelmente o site foi atualizado e esse elemento nao existe mais ou mudou de posicao. "
      "Continuando a execucao normalmente."
    )
    return None


try:
  # Acessa o site
  driver.get("https://maceio.giss.com.br/portal/#/login-portal")
  time.sleep(3)  # Aguarda o carregamento da página

  popup = buscar_elemento_opcional(By.XPATH, "/html/body/div[1]/div[4]/div/div/div[1]/button/span", "popup inicial de boas-vindas")
  if popup is not None:
    popup.click()

  time.sleep(1)  # Aguarda o carregamento da página

  # Localiza e preenche o campo de usuário
  usuario_input = buscar_elemento(By.ID, "usuario", "campo de usuario (login)")
  usuario_input.send_keys(Usuario)

  # Localiza e preenche o campo de senha
  senha_input = buscar_elemento(By.ID, "senha", "campo de senha (login)")
  senha_input.send_keys(Senha)

  time.sleep(5)  # Aguarda o login ser processado

  # Clica no botão de login
  login_button = buscar_elemento(By.XPATH, "/html/body/div[1]/div[1]/form/div/div/div[3]/div/button", "botao de login")
  login_button.click()
  time.sleep(1)  # Aguarda o login ser processado

  elemento = None
  if cnpj == "37.971.252/0001-78":
    elemento = "/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[1]/td[5]/button"
  if cnpj == "54.552.751/0001-40":
    elemento = "/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[2]/td[5]/button"
  if cnpj == "56.422.742/0001-60":
    elemento = "/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[3]/td[5]/button"

  if elemento is None:
    raise RuntimeError(
      f"CNPJ '{cnpj}' configurado em parametros.txt nao e reconhecido. "
      "Verifique o valor do parametro 'cnpj' ou cadastre o XPath correspondente no main.py."
    )

  selecionaEmpresa = buscar_elemento(By.XPATH, elemento, "botao de selecao da empresa (CNPJ)")
  selecionaEmpresa.click()
  time.sleep(3)  # Aguarda o login ser processado


#37.971.252/0001-78
#/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[1]/td[5]/button/svg
#54.552.751/0001-40
#/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[2]/td[5]/button/svg
#56.422.742/0001-60
#/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[3]/td[5]/button/svg

    # Abre a planilha e lê as colunas necessárias
    # Itera sobre as linhas da planilha
  df = pd.read_excel(
    nomeArquivo,
    usecols=["CPF", "NOME", "CEP", "Nº", "VALOR", "DATA", "STATUS NF", "FORMA"],
    skiprows=1)
    # Itera sobre as linhas da planilha
  i = 1
  for index, row in df.iterrows():
    cpf = str(row["CPF"])
    if cpf.endswith('.0'):
      cpf = cpf[:-2]

    nome = row["NOME"]
    cep = str(row["CEP"])
    if cep.endswith('.0'):
      cep = cep[:-2]

    numero = row["Nº"]
    valor = row["VALOR"]
    data = row["DATA"]
    status_nf = row["STATUS NF"]
    forma = row["FORMA"]
    print(cpf)
    if pd.isna(cpf) or cpf == "NaT":
      print("fim")
      break
    if len(cpf) < 5:
      print("fim")
      break

    try:
      # normaliza a coluna DATA: na planilha pode vir como texto ou como data/hora
      data = pd.to_datetime(data, dayfirst=True, errors='coerce')
      if pd.isna(data):
        raise RuntimeError(
          f"Valor invalido/vazio na coluna 'DATA' (valor original: '{row['DATA']}'). "
          "Verifique se a celula esta preenchida com uma data valida, ex: 03/08/2026."
        )

      #iniciar emissao
      elemento = "/html/body/div[1]/main/div[2]/div[1]/sidebar-directive/nav/ul/li[1]/a"
      servicoPrestado = buscar_elemento(By.XPATH, elemento, "menu 'Servico Prestado'")
      servicoPrestado.click()
      time.sleep(1)

      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/sub-menu/nav/ul/li[1]/a"
      emitirNF = buscar_elemento(By.XPATH, elemento, "submenu 'Emitir NF'")
      emitirNF.click()
      time.sleep(1)

      #data prestação
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[1]/div/div[1]/div[1]/input"
      dataPrestacao = buscar_elemento(By.XPATH, elemento, "campo 'Data de prestacao'")
      dataPrestacao.clear()
      dataPrestacao.send_keys(data.strftime("%d/%m/%Y"))
      time.sleep(0.5)

      #atividade
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[1]/div/div[1]/div[2]/select"
      atividade = buscar_elemento(By.XPATH, elemento, "campo 'Atividade'")
      atividade.click()
      atividade.send_keys("17.06 / 7319002 - promoção de vendas")
      time.sleep(0.5)

      #dadosTomador
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[1]/input"
      dadosTomador = buscar_elemento(By.XPATH, elemento, "campo 'CPF do tomador'")
      dadosTomador.send_keys(cpf)
      time.sleep(2)

      #Pesquisar Tomador
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[2]/button"
      pesquisarTomador = buscar_elemento(By.XPATH, elemento, "botao 'Pesquisar tomador'")
      pesquisarTomador.click()
      time.sleep(2)

      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[1]/div/div/div/div[1]/ul[2]/li/p[1]"
      listaTomador = buscar_elemento(By.XPATH, elemento, "resultado da busca do tomador")
      listaTomador.click()
      time.sleep(2)

      #valor
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[3]/div/div/div[1]/input"
      valorInput = buscar_elemento(By.XPATH, elemento, "campo 'Valor'")
      valorInput.send_keys(str(valor).replace('.','').replace(',','.'))
      time.sleep(1)

      #discriminacao
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[4]/div/div[1]/div[2]/textarea"
      discriminacao = buscar_elemento(By.XPATH, elemento, "campo 'Discriminacao'")
      discriminacao.send_keys("Serviços prestados")
      time.sleep(0.5)

      #piscofins
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[5]/div/piscofins-form/ng-form/div/div/select"
      piscofins = buscar_elemento(By.XPATH, elemento, "campo 'PIS/COFINS'")
      piscofins.click()
      piscofins.send_keys("00 - Nenhum")
      time.sleep(0.5)

      #btnProximo
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/div/div/button"
      btnProximo = buscar_elemento(By.XPATH, elemento, "botao 'Proximo' (etapa 1)")
      btnProximo.click()
      time.sleep(0.5)

      #outra tela
      time.sleep(2)
      #estado
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/fieldset[1]/div/div/div[1]/select"
      estado = buscar_elemento(By.XPATH, elemento, "campo 'Estado'")
      estado.click()
      estado.send_keys("AL")

      #município
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/fieldset[1]/div/div/div[2]/select"
      municipio = buscar_elemento(By.XPATH, elemento, "campo 'Municipio'")
      municipio.click()
      municipio.send_keys("Maceió")
      time.sleep(0.5)

      #alíquota
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/fieldset[2]/div/div/div/input"
      aliquota = buscar_elemento(By.XPATH, elemento, "campo 'Aliquota'")
      aliquota.clear()
      aliquota.send_keys(Valor_Aliquota)
      aliquota.send_keys(Keys.TAB)
      time.sleep(0.5)

      #proximo
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/div/div/button[2]"
      btnProximo2 = buscar_elemento(By.XPATH, elemento, "botao 'Proximo' (etapa 2)")
      btnProximo2.click()
      time.sleep(2)

      #ultima tela
      elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/div/div/button[2]"
      btnConcluir = buscar_elemento(By.XPATH, elemento, "botao 'Concluir'")
      if ambiente == "producao":

        btnConcluir.click()
        print(f"Concluir... {i} segundos...", end='\r')
        i = i +1
        time.sleep(2)
        
        elemento = "/html/body/div[4]/div[7]/button"
        btnNao = buscar_elemento(By.XPATH, elemento, "botao 'Nao' (etapa 2)")
        btnNao.click()
        time.sleep(2)


  #    btnConcluir.click()
      df.at[index, "STATUS NF"] = "processado"

    except RuntimeError as e:
      print(f"\nERRO ao processar a linha {index + 1} (CPF: {cpf}, NOME: {nome}): {e}")
      print("Interrompendo o processamento das proximas linhas. A planilha sera salva com o progresso ate aqui.")
      break

    for i in range(tempoEspera, 0, -1):
      print(f"Próxima NF em {i} segundos...", end='\r')
      time.sleep(1)
    print(" " * 30, end='\r')  # Limpa a linha
    print("proxima NF")

  #fim
  df.to_excel("PLANILHA EMISSAO NOVA 2025_processada.xlsx", index=False)


  time.sleep(5)  # Aguarda o login ser processado

except RuntimeError as e:
  print(f"\nERRO: {e}")
finally:
  driver.quit()
