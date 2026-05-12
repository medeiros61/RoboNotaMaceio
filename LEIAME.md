# Robo Nota Maceio

Automação de emissão de NFS-e no portal da prefeitura de Maceió (GISS).

**Localização do projeto:** `e:\Projetos\datavix\RoboNotaMaceio`

---

## O que faz

Lê uma planilha Excel com dados de tomadores e emite automaticamente as Notas Fiscais de Serviço no portal:
`https://maceio.giss.com.br/portal/#/login-portal`

Ao finalizar, gera uma nova planilha marcando cada linha como `processado`.

---

## Estrutura

```
RoboNotaMaceio/
├── main.py                          # Script principal
├── main.spec                        # Configuração do PyInstaller
├── parametros.txt                   # Credenciais e configurações (editar antes de rodar)
├── requirements.txt                 # Dependências Python
├── venv_robo_maceio/                # Ambiente virtual Python
├── PLANILHA EMISSAO NOVA 2025-2.xlsx  # Planilha de entrada (nome configurável)
└── PLANILHA EMISSAO NOVA 2025_processada.xlsx  # Gerada automaticamente após execução
```

---

## Planilha de entrada

A planilha deve conter as colunas (a partir da segunda linha — a primeira é ignorada com `skiprows=1`):

| Coluna    | Descrição                         |
|-----------|-----------------------------------|
| CPF       | CPF do tomador                    |
| NOME      | Nome do tomador                   |
| CEP       | CEP do tomador                    |
| Nº        | Número do endereço                |
| VALOR     | Valor da nota                     |
| DATA      | Data da prestação do serviço      |
| STATUS NF | Deixar em branco (preenchido pelo robô) |
| FORMA     | Forma de pagamento                |

O robô para de processar quando encontra uma linha com CPF vazio ou com menos de 5 caracteres.

---

## Parâmetros (`parametros.txt`)

```ini
[DEFAULT]
Usuario      = <CPF do usuário do portal>
Senha        = <Senha do portal>
nomeArquivo  = PLANILHA EMISSAO NOVA 2025-2.xlsx
Valor_Aliquota = 3,23
cnpj         = 56.422.742/0001-60
tempoEspera  = 10
ambiente     = producao
```

### CNPJs cadastrados e sua linha na tela de seleção de empresa

| CNPJ                  | Posição na tabela |
|-----------------------|-------------------|
| 37.971.252/0001-78    | Linha 1           |
| 54.552.751/0001-40    | Linha 2           |
| 56.422.742/0001-60    | Linha 3           |

> Para adicionar outro CNPJ, inserir novo `if cnpj == "..."` em `main.py` apontando para a linha correta da tabela.

### Parâmetro `ambiente`

| Valor      | Comportamento                                      |
|------------|----------------------------------------------------|
| `producao` | Clica em "Concluir" e emite a nota de verdade      |
| qualquer outro valor | Preenche o formulário mas **não** clica em Concluir (modo teste) |

---

## Como executar

### Pelo Python (desenvolvimento)

```powershell
# Ativar ambiente virtual
.\venv_robo_maceio\Scripts\Activate.ps1

# Rodar
python main.py
```

### Pelo executável gerado

```
dist\main.exe
```

O `parametros.txt` e a planilha Excel devem estar **na mesma pasta** do executável.

---

## Como gerar o executável (.exe)

```powershell
# Ativar ambiente virtual
.\venv_robo_maceio\Scripts\Activate.ps1

# Gerar executável (usa o main.spec já configurado)
pyinstaller main.spec
```

O executável gerado fica em: `dist\main.exe`

> Após gerar, copiar para a pasta de uso junto com `parametros.txt` e a planilha Excel.

---

## Instalar dependências (primeira vez ou após reset do venv)

```powershell
# Criar o ambiente virtual
python -m venv venv_robo_maceio

# Ativar
.\venv_robo_maceio\Scripts\Activate.ps1

# Instalar pacotes
pip install -r requirements.txt
```

---

## Requisitos do sistema

- Python 3.x
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome instalada
  - O Selenium 4.x gerencia o ChromeDriver automaticamente (não precisa instalar manualmente)

---

## Dados fixos no código (`main.py`)

Estes valores estão hardcoded e precisam ser alterados diretamente no script se mudarem:

| Campo           | Valor atual                                    |
|-----------------|------------------------------------------------|
| Atividade       | `17.06 / 7319002 - promoção de vendas`         |
| Discriminação   | `Serviços prestados`                           |
| Estado          | `AL`                                           |
| Município       | `Maceió`                                       |
| PIS/COFINS      | `00 - Nenhum`                                  |
