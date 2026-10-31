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

### 1. Tela inicial (*Splash Screen*)

Ao iniciar, o sistema exibe o nome da aplicação, a disciplina, o professor, o semestre, os integrantes do grupo e a quantidade de registros de cada tabela, obtida com a consulta `select count(1) as total_{tabela} from {tabela}`.

### 2. Menu principal

```text
1 - Relatórios
2 - Inserir registros
3 - Remover registros
4 - Atualizar registros
5 - Sair
```

Nas opções 2, 3 e 4 o sistema exibe o menu de entidades (**Alunos, Instrutores, Treinos e Frequências**) para o usuário escolher em qual tabela deseja trabalhar. O menu principal volta a ser exibido ao final de cada operação.

### 3. Inserir registros

1. Escolha a entidade.
2. Informe cada atributo solicitado. Antes de gravar, o sistema verifica se o registro já existe (e-mail repetido de aluno ou instrutor, aluno e instrutor inexistentes no treino ou na frequência).
3. O registro é inserido e exibido na tela.
4. O sistema pergunta se deseja inserir mais algum registro: **Sim** continua na mesma entidade; **Não** volta ao menu principal.

### 4. Remover registros

1. Escolha a entidade.
2. O sistema lista os registros (ID e campos descritivos).
3. Informe o ID do registro e confirme a exclusão. Se responder **Não**, volta ao menu principal.
4. Se o registro for chave estrangeira em outra tabela (aluno com treinos ou frequências, instrutor com treinos), o sistema informa quantos registros relacionados existem e pergunta se deseja excluí-los também. Se a resposta for **Não**, o registro não é excluído.
5. O sistema pergunta se deseja excluir mais algum registro.

### 5. Atualizar registros

1. Escolha a entidade.
2. O sistema lista os registros (ID e campos descritivos).
3. Informe o ID do registro. O sistema mostra os dados atuais e pede todos os atributos, exceto a chave primária (ENTER mantém o valor atual).
4. O registro é atualizado e exibido com os novos dados.
5. O sistema pergunta se deseja atualizar mais algum registro.

### 6. Relatórios

```text
1 - Quantidade de treinos por aluno (agrupamento)
2 - Treinos com alunos e instrutores (junção)
3 - Treinos de um aluno
4 - Frequências de um aluno
0 - Voltar ao menu principal
```

- **Quantidade de treinos por aluno:** usa `COUNT` e `GROUP BY` (sumarização).
- **Treinos com alunos e instrutores:** usa `INNER JOIN` entre TREINO, ALUNO e INSTRUTOR (junção).

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
│   ├── model/
│   │   ├── aluno.py
│   │   ├── instrutor.py
│   │   ├── treino.py
│   │   └── frequencia.py
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
│   │   ├── config.py
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

Por padrão, o sistema se conecta ao Oracle em `localhost`, porta `1521`, primeiro pelo SID `XE` e, se não conseguir, pelo serviço `XEPDB1`. Esse é o cenário da VM da disciplina, em que o Oracle roda na mesma máquina que o programa.

Se o Oracle estiver em outra máquina (por exemplo, rodar o programa no seu computador acessando o Oracle da VM), informe o IP dela na variável de ambiente `ORACLE_HOST`, sem alterar o código:

```bash
export ORACLE_HOST=192.168.0.10   # IP da maquina onde o Oracle esta
python3 principal.py
```

Se aparecer o erro `ORA-12541: TNS:no listener`, o programa não encontrou o Oracle no endereço configurado: verifique se o banco está ligado e se o `ORACLE_HOST` está correto.

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

[Assistir à demonstração no YouTube](https://youtu.be/IGU7rv3a0Eo)

## Autores

Projeto desenvolvido em grupo como atividade acadêmica da disciplina de Banco de Dados.

Integrantes:
- Caio Vitor Ferrari
- Érika Pimenta
- Esther Bagatelli
- Gabriela de Oliveira Nascimento
- Lara Marchesi Goltara
- Laysa da Costa Colli

## Repositório

GitHub: https://github.com/gabinasciment/sistema-academia-bd