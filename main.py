from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

try:
  # Acessa o site
  driver.get("https://maceio.giss.com.br/portal/#/login-portal")
  time.sleep(3)  # Aguarda o carregamento da página

  popup = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/div[1]/button/span")
  popup.click()

  time.sleep(1)  # Aguarda o carregamento da página

  # Localiza e preenche o campo de usuário
  usuario_input = driver.find_element(By.ID, "usuario")
  usuario_input.send_keys(Usuario)

  # Localiza e preenche o campo de senha
  senha_input = driver.find_element(By.ID, "senha")
  senha_input.send_keys(Senha)

  time.sleep(5)  # Aguarda o login ser processado

  # Clica no botão de login
                                                    
  login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form/div/div/div[3]/div/button")

  login_button.click()
  time.sleep(1)  # Aguarda o login ser processado
  if cnpj == "37.971.252/0001-78":
    elemento ="/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[1]/td[5]/button"     
    elemento ="/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[1]/td[5]/button"
  if cnpj == "54.552.751/0001-40":
    elemento ="/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[2]/td[5]/button"     
  if cnpj == "56.422.742/0001-60":
    elemento ="/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[3]/td[5]/button"     


  selecionaEmpresa = driver.find_element(By.XPATH, elemento)
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
      
    #iniciar emissao
    elemento = "/html/body/div[1]/main/div[2]/div[1]/sidebar-directive/nav/ul/li[1]/a"
    servicoPrestado = driver.find_element(By.XPATH, elemento)
    servicoPrestado.click()
    time.sleep(1)  
    
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/sub-menu/nav/ul/li[1]/a"
    emitirNF = driver.find_element(By.XPATH, elemento)
    emitirNF.click()
    time.sleep(1)  

    #data prestação
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[1]/div/div[1]/div[1]/input"
    dataPrestacao = driver.find_element(By.XPATH, elemento)
    dataPrestacao.clear()
    dataPrestacao.send_keys(data.strftime("%d/%m/%Y"))
    time.sleep(0.5)  
    
    #atividade
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[1]/div/div[1]/div[2]/select"
    atividade = driver.find_element(By.XPATH, elemento)
    atividade.click()
    atividade.send_keys("17.06 / 7319002 - promoção de vendas")
    time.sleep(0.5)  
    
    #dadosTomador
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[1]/input"
    dadosTomador = driver.find_element(By.XPATH, elemento)
    dadosTomador.send_keys(cpf) 
    time.sleep(2) 
    
    #Pesquisar Tomador
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[2]/button"
    pesquisarTomador = driver.find_element(By.XPATH, elemento)
    pesquisarTomador.click() 
    time.sleep(2)
    
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[1]/div/div/div/div[1]/ul[2]/li/p[1]"
    listaTomador = driver.find_element(By.XPATH, elemento)
    listaTomador.click() 
    time.sleep(2)
        
    #valor
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[3]/div/div/div[1]/input"
    valorInput = driver.find_element(By.XPATH, elemento)
    valorInput.send_keys(str(valor).replace('.','').replace(',','.'))    
    time.sleep(1)
    
    #discriminacao
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[4]/div/div[1]/div[2]/textarea"
    discriminacao = driver.find_element(By.XPATH, elemento)
    discriminacao.send_keys("Serviços prestados")
    time.sleep(0.5)  

    #piscofins
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[5]/div/piscofins-form/ng-form/div/div/select"
    piscofins = driver.find_element(By.XPATH, elemento)
    piscofins.click()
    piscofins.send_keys("00 - Nenhum")
    time.sleep(0.5)

    #btnProximo
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/div/div/button"
    btnProximo = driver.find_element(By.XPATH, elemento)
    btnProximo.click()
    time.sleep(0.5)  
    
    #outra tela
    time.sleep(2)
    #estado
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/fieldset[1]/div/div/div[1]/select"
    estado = driver.find_element(By.XPATH, elemento)
    estado.click()
    estado.send_keys("AL")
    
    #município
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/fieldset[1]/div/div/div[2]/select"
    municipio = driver.find_element(By.XPATH, elemento)
    municipio.click()
    municipio.send_keys("Maceió")
    time.sleep(0.5)  
    
    #alíquota
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/fieldset[2]/div/div/div/input"
    aliquota = driver.find_element(By.XPATH, elemento)
    aliquota.clear()
    aliquota.send_keys(Valor_Aliquota)    
    aliquota.send_keys(Keys.TAB)
    time.sleep(0.5)  

    #proximo
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/div/div/button[2]"
    btnProximo2 = driver.find_element(By.XPATH, elemento)
    btnProximo2.click() 
    time.sleep(2) 
    
    #ultima tela
    elemento = "/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/div/div/button[2]"
    btnConcluir = driver.find_element(By.XPATH, elemento)
    if ambiente == "producao":

      btnConcluir.click() 
      print(f"Concluir... {i} segundos...", end='\r')
      i = i +1
      time.sleep(5)
      
#    btnConcluir.click()
    df.at[index, "STATUS NF"] = "processado"

    for i in range(tempoEspera, 0, -1):
      print(f"Próxima NF em {i} segundos...", end='\r')
      time.sleep(1)
    print(" " * 30, end='\r')  # Limpa a linha
    print("proxima NF")
    
  #fim
  df.to_excel("PLANILHA EMISSAO NOVA 2025_processada.xlsx", index=False)


  time.sleep(5)  # Aguarda o login ser processado

finally:
  driver.quit()