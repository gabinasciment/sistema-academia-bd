# Sistema de Academia

Sistema de gerenciamento de academia desenvolvido em Python com banco de dados Oracle. O projeto permite realizar operações de cadastro, consulta, atualização e exclusão de alunos, instrutores, treinos e frequências, além de gerar relatórios relacionados aos treinos.

## Objetivo do projeto

Desenvolver uma aplicação integrada a um banco de dados relacional Oracle para facilitar o gerenciamento das principais informações de uma academia, utilizando Python para a interação com o banco de dados.

## Tecnologias utilizadas

- **Python 3.10**
- **Oracle Database**
- **Oracle Instant Client**
- **cx_Oracle 8.3.0**
- **Pandas**
- **Git e GitHub**

## Funcionalidades

### 1. Menu principal

A aplicação apresenta uma tela inicial (*Splash Screen*) e um menu principal com as seguintes opções:

1. Gerenciar alunos.
2. Gerenciar instrutores.
3. Gerenciar treinos.
4. Gerenciar frequências.
5. Consultar relatórios.
0. Sair do sistema.

### 2. Gerenciamento de alunos

Permite realizar as seguintes operações:

- Listar os alunos cadastrados.
- Cadastrar novos alunos.
- Consultar um aluno pelo identificador.
- Atualizar os dados de um aluno.
- Excluir um aluno.
- Voltar ao menu principal.

Os dados dos alunos incluem nome, e-mail, telefone, data de nascimento e gênero.

### 3. Gerenciamento de instrutores

Permite:

- Listar os instrutores cadastrados.
- Cadastrar novos instrutores.
- Consultar um instrutor pelo identificador.
- Atualizar os dados de um instrutor.
- Excluir um instrutor.
- Voltar ao menu principal.

Os dados dos instrutores incluem nome, e-mail e telefone.

A exclusão de registros pode ser impedida quando existem relacionamentos com outros registros do banco de dados, conforme as restrições de integridade referencial.

### 4. Gerenciamento de treinos

Permite:

- Listar os treinos cadastrados.
- Cadastrar novos treinos.
- Consultar um treino pelo identificador.
- Atualizar os dados de um treino.
- Excluir um treino.
- Listar os treinos de um aluno.
- Voltar ao menu principal.

Cada treino está associado a um aluno e a um instrutor. Os dados incluem nome do treino, objetivo e data de criação.

### 5. Gerenciamento de frequências

Permite:

- Listar os registros de frequência.
- Registrar uma nova frequência.
- Consultar uma frequência pelo identificador.
- Atualizar um registro de frequência.
- Excluir um registro de frequência.
- Listar as frequências de um aluno.
- Voltar ao menu principal.

Cada registro de frequência está associado a um aluno e contém a data e a hora de entrada na academia.

### 6. Relatórios

O sistema disponibiliza dois relatórios:

**Relatório de treinos por aluno**

Apresenta os alunos e a quantidade de treinos associados a cada um.

**Relatório de treinos com instrutores**

Apresenta informações sobre os treinos, os alunos relacionados e os instrutores responsáveis.

## Estrutura do projeto

A organização principal dos arquivos é:

```text
sistema-academia-bd/
├── sql/
├── src/
│   ├── conexion/
│   │   ├── passphrase/
│   │   │   └── authentication.oracle
│   │   └── oracle_queries.py
│   ├── controller/
│   │   ├── controller_aluno.py
│   │   ├── controller_instrutor.py
│   │   ├── controller_treino.py
│   │   └── controller_frequencia.py
│   ├── reports/
│   │   └── relatorios.py
│   ├── sql/
│   │   ├── relatorio_treinos_por_aluno.sql
│   │   └── relatorio_treinos_com_instrutores.sql
│   ├── utils/
│   │   ├── menu.py
│   │   ├── menu_alunos.py
│   │   ├── menu_instrutores.py
│   │   ├── menu_treinos.py
│   │   ├── menu_frequencias.py
│   │   └── splash_screen.py
│   ├── create_tables_and_records.py
│   ├── principal.py
│   └── requirements.txt
├── PROMPTS.md
└── README.md
```

**Observação:** a estrutura apresenta os principais arquivos utilizados pela aplicação. Outros arquivos SQL e auxiliares podem existir no repositório.

## Banco de dados

O projeto utiliza o Oracle Database para armazenar os dados da academia.

As principais entidades são:

- **ALUNO:** armazena os dados dos alunos.
- **INSTRUTOR:** armazena os dados dos instrutores.
- **TREINO:** armazena os treinos e seus relacionamentos com alunos e instrutores.
- **FREQUENCIA:** registra as entradas dos alunos na academia.

As tabelas utilizam chaves primárias e relacionamentos por chaves estrangeiras para manter a integridade dos dados. O projeto também utiliza sequências para gerar identificadores.

## Configuração da conexão

A conexão com o banco de dados é configurada em:

`src/conexion/oracle_queries.py`

O arquivo de autenticação está localizado em:

`src/conexion/passphrase/authentication.oracle`

O arquivo de autenticação deve conter as credenciais no formato esperado pela aplicação, sem que senhas reais sejam publicadas no GitHub.

A configuração da conexão deve corresponder ao ambiente Oracle utilizado pelo grupo, incluindo:

- Endereço IP ou nome do servidor.
- Porta de conexão.
- Serviço ou identificador do banco de dados.
- Usuário e senha válidos.

O endereço do servidor pode variar conforme a rede e o ambiente disponibilizado pelo professor. Caso a aplicação não consiga se conectar, confira as configurações e verifique se o banco Oracle está em execução e acessível.

**Importante:** não publique senhas reais ou outras credenciais de acesso no repositório.

## Requisitos

Antes de executar o projeto, instale ou configure:

- Python 3.10 de 64 bits.
- Oracle Database acessível pela máquina que executará a aplicação.
- Oracle Instant Client compatível com o ambiente.
- Dependências Python listadas em `src/requirements.txt`.

A versão Python 3.10 é utilizada neste projeto por compatibilidade com a versão do `cx_Oracle` especificada nos requisitos.

Para a execução no ambiente acadêmico, utilize a máquina virtual Linux conforme as orientações do professor. Verifique se o Python, o Oracle Instant Client e as dependências estão instalados e se o banco de dados Oracle está acessível.

## Instalação e execução

### 1. Clonar o repositório

No terminal, execute:

git clone https://github.com/gabinasciment/sistema-academia-bd.git
cd sistema-academia-bd

### 2. Instalar as dependências

Na pasta raiz do projeto, execute:

**Windows:**

```powershell
py -3.10 -m pip install -r src/requirements.txt
```

**Linux:**

```bash
python3 -m pip install -r src/requirements.txt
```

Se o comando `py -3.10` não estiver disponível no Windows, verifique se o Python 3.10 está instalado e registrado no inicializador do Python.

### 3. Configurar o Oracle Instant Client

O Oracle Instant Client deve estar instalado e configurado no ambiente em que a aplicação será executada.

**Windows:**

Adicione a pasta do Oracle Instant Client ao `PATH`.

Exemplo de configuração no terminal PowerShell:

```powershell
$env:PATH = "C:\caminho\para\instantclient;$env:PATH"
```

O caminho deve ser substituído pelo local em que o Instant Client está instalado no computador.

O comando configura o `PATH` somente para o terminal atual. Ao abrir outro terminal, será necessário configurar novamente ou ajustar as variáveis de ambiente do Windows de forma permanente.

**Linux:**

Configure a variável `LD_LIBRARY_PATH` com o caminho da pasta do Oracle Instant Client, conforme o local em que ele foi instalado.

Exemplo:

```bash
export LD_LIBRARY_PATH=/caminho/para/instantclient:$LD_LIBRARY_PATH
```

Substitua o caminho pelo diretório correto da instalação.

Para verificar se o `cx_Oracle` consegue carregar o cliente Oracle, execute:

**Windows:**

```powershell
py -3.10 -c "import cx_Oracle; print(cx_Oracle.clientversion())"
```

**Linux:**

```bash
python3 -c "import cx_Oracle; print(cx_Oracle.clientversion())"
```

Se a configuração estiver correta, o comando exibirá a versão do cliente Oracle.

### 4. Configurar a conexão com o banco

Confira as configurações de conexão em `src/conexion/oracle_queries.py` e as credenciais no arquivo de autenticação.

Antes de executar a aplicação, confirme que:

- O banco Oracle está em execução.
- O computador consegue alcançar o servidor do banco.
- O endereço IP ou nome do servidor está correto.
- A porta e o serviço estão corretos.
- As credenciais configuradas são válidas.

### 5. Executar o sistema

A partir da pasta raiz do projeto, entre na pasta `src`:

```bash
cd src
```

Execute a aplicação:

**Windows:**

```powershell
py -3.10 principal.py
```

**Linux:**

```bash
python3 principal.py
```

A aplicação exibirá a tela inicial e, em seguida, o menu principal. Utilize os números apresentados para navegar pelas funcionalidades.

## Criação das tabelas e dos registros iniciais

O projeto contém o script:

`src/create_tables_and_records.py`

Esse arquivo é responsável pela criação das estruturas do banco e pela inserção de registros iniciais, conforme as instruções implementadas no script.

Para executá-lo, entre na pasta `src` e utilize:

**Windows:**

```powershell
py -3.10 create_tables_and_records.py
```

**Linux:**

```bash
python3 create_tables_and_records.py
```

**Atenção:** execute esse script somente quando necessário e depois de conferir seu conteúdo. Ele pode remover e recriar objetos do banco de dados, apagando registros existentes. Não o execute novamente em um banco com dados que deseja preservar sem antes verificar os comandos utilizados.

## Tratamento de erros e observações

- A aplicação depende de uma conexão ativa com o Oracle Database.
- Problemas com o Oracle Instant Client podem causar erros de carregamento da biblioteca cliente, como `DPI-1047`.
- Falhas de conexão podem ocorrer quando o endereço IP, a porta, o serviço ou as credenciais estão incorretos.
- A exclusão de registros relacionados a outros dados pode ser bloqueada pelas restrições de chaves estrangeiras.
- Mensagens indicando que tabelas ou sequências não existem podem aparecer na primeira execução do script de criação quando ele tenta remover objetos ainda não criados. Confira o resultado final da execução antes de concluir que houve falha.

## Uso de inteligência artificial

As ferramentas de inteligência artificial utilizadas como apoio ao desenvolvimento do projeto estão documentadas no arquivo `PROMPTS.md`, que apresenta os prompts utilizados, os resultados obtidos e as atividades realizadas pelo grupo a partir das respostas.

## Demonstração do sistema

Vídeo de apresentação e demonstração das funcionalidades:

[Assistir à demonstração no YouTube](INSERIR_LINK_DO_VIDEO)

## Autores

Projeto desenvolvido em grupo como atividade acadêmica da disciplina de Banco de Dados.

Integrantes:
- Esther Bagatelli
- Érika Pimenta
- Gabriela Nascimento
- Laysa Costa
- Lara Marchesi
- Caio Ferrari

## Repositório

GitHub: https://github.com/gabinasciment/sistema-academia-bd