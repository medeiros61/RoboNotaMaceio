import configparser

# Para gerar o arquivo parametros.txt:
#with open('parametros2.txt', 'w', encoding='utf-8') as f:
##  f.write('[DEFAULT]\n')
#  f.write('Usuario = seu_usuario\n')
#  f.write('Senha = sua_senha\n')
#  f.write('nomeArquivo = sua_planilha.xlsx\n')
##  f.write('Valor_Aliquota = 5\n')
#  f.write('cnpj = 37.971.252/0001-78\n')
#  f.write('tempoEspera = 5\n')
  
def ler_parametros(arquivo):
  config = configparser.ConfigParser()
  config.read(arquivo, encoding='utf-8')
  parametros = dict(config['DEFAULT'])
  return parametros

  # Exemplo de uso:
parametros = ler_parametros('parametros2.txt')
print(parametros)
