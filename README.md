# Sistema de Academia

Sistema de gerenciamento de uma academia de ginástica, desenvolvido na disciplina de **Banco de Dados** (Prof. Howard Roatti, 2026/2). O programa roda no terminal, em Python, e guarda os dados em um banco **Oracle**. Pelo menu é possível gerar relatórios e inserir, atualizar e remover alunos, instrutores, treinos e frequências.

<!-- completar com os nomes completos -->
**Integrantes:** Gabriela Nascimento, Esther, Érika, Lara, Caio e Laysa

**Vídeo de demonstração:** _(link do YouTube)_

---

## Banco de dados

O sistema possui quatro tabelas:

| Tabela | O que guarda | Relacionamento |
|---|---|---|
| `ALUNO` | Dados dos alunos (nome, e-mail, telefone, data de nascimento, gênero) | Tabela pai |
| `INSTRUTOR` | Dados dos instrutores (nome, e-mail, telefone) | Tabela pai |
| `TREINO` | Treinos montados para cada aluno | 1 aluno possui N treinos · 1 instrutor orienta N treinos |
| `FREQUENCIA` | Entradas dos alunos na academia (data e hora) | 1 aluno registra N frequências |

- As chaves primárias são geradas por **sequences** (ex.: `ALUNO_ID_ALUNO_SEQ`).
- Os e-mails de aluno e instrutor são **únicos** (`UNIQUE`).
- As chaves estrangeiras **não** usam `ON DELETE CASCADE`: antes de remover um aluno ou instrutor, o próprio sistema verifica se existem registros ligados a ele e pergunta ao usuário o que fazer.

O diagrama relacional está em [diagramas/diagramarelacional.png](diagramas/diagramarelacional.png).

---

## Requisitos

- Linux (máquina virtual da disciplina)
- Oracle Database (XE) em execução na própria máquina (`localhost`, porta `1521`)
- Oracle Instant Client (já instalado na VM da disciplina)
- Python 3 e pip

## Instalação

1. Baixe o projeto e entre na pasta `src`:

   ```shell
   git clone https://github.com/gabinasciment/sistema-academia-bd.git
   cd sistema-academia-bd/src
   ```

2. Instale as bibliotecas:

   ```shell
   pip3 install -r requirements.txt
   ```

## Configurando a conexão com o banco

O usuário e a senha do Oracle ficam no arquivo [src/conexion/passphrase/authentication.oracle](src/conexion/passphrase/authentication.oracle), no formato `usuario,senha`:

```
labdatabase,lab@Database2025
```

Se o usuário ou a senha do Oracle na sua máquina forem diferentes, altere esse arquivo.

O módulo de conexão ([src/conexion/oracle_queries.py](src/conexion/oracle_queries.py)) conecta em `localhost:1521`, tentando primeiro o SID `XE` e, se não conseguir, o service name `XEPDB1`.

## Criando as tabelas e os dados de exemplo

Ainda dentro da pasta `src`, execute:

```shell
python3 create_tables_and_records.py
```

O script executa os arquivos da pasta [sql](sql):

- [sql/create_tables_academia.sql](sql/create_tables_academia.sql): apaga as tabelas, se já existirem, e cria as tabelas, chaves primárias, chaves estrangeiras e sequences
- [sql/inserting_samples_records.sql](sql/inserting_samples_records.sql): insere os dados de exemplo

No final, ele mostra a quantidade de registros de cada tabela:

```
TOTAL DE REGISTROS POR TABELA
  ALUNO        10
  INSTRUTOR    4
  TREINO       20
  FREQUENCIA   30
```

O script pode ser executado quantas vezes for necessário: ele sempre recria o banco do zero com os mesmos dados.

Avisos esperados durante a execução:

- Na primeira vez, os comandos `DROP` mostram `ORA-00942` e `ORA-02289` (a tabela ou a sequência ainda não existe).
- O último comando (`ALTER USER ... QUOTA`) pode mostrar `ORA-01031` quando o usuário já tem espaço liberado no banco.

O que importa é o resultado final: os totais de registros de cada tabela.

## Executando o sistema

Depois de criar as tabelas, ainda dentro da pasta `src`:

```shell
python3 principal.py
```

<!-- Laysa: completar com a descrição da tela inicial e dos menus -->

---

## Organização do projeto

- [diagramas](diagramas): diagrama relacional do sistema (Mermaid e PNG)
- [sql](sql): scripts de criação das tabelas e de inserção dos dados de exemplo
- [src](src): código do sistema
  - [conexion](src/conexion): módulo de conexão com o Oracle e arquivo de autenticação
  - [controller](src/controller): classes responsáveis por inserir, atualizar e remover registros
  - [model](src/model): classes que representam as entidades do banco
  - [reports](src/reports): classe que gera os relatórios
  - [sql](src/sql): consultas SQL dos relatórios
  - [utils](src/utils): menus e tela inicial (splash screen)
  - [create_tables_and_records.py](src/create_tables_and_records.py): cria as tabelas e insere os dados de exemplo
  - `principal.py`: programa principal
- [PROMPTS.md](PROMPTS.md): registro dos prompts de IA utilizados no desenvolvimento

---

## Problemas comuns

| Mensagem | Causa | Solução |
|---|---|---|
| `ORA-12541: TNS:no listener` | O Oracle não está em execução | Inicie o Oracle e tente novamente |
| `ORA-01017: invalid username/password` | Usuário ou senha incorretos | Confira o arquivo `authentication.oracle` |
| `ORA-28001: the password has expired` | A senha do usuário expirou | Como administrador, execute `ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;` e `ALTER USER labdatabase IDENTIFIED BY "lab@Database2025";` |
| `ORA-01031: insufficient privileges` em um `CREATE TABLE` ou `CREATE SEQUENCE` | O usuário não tem permissão para criar objetos | Como administrador, execute `GRANT ALL PRIVILEGES TO LABDATABASE;` |
| `DPI-1047: Cannot locate a 64-bit Oracle Client library` | O Oracle Instant Client não foi encontrado | Verifique a instalação do Instant Client e as variáveis `ORACLE_HOME` e `LD_LIBRARY_PATH` |
| `FileNotFoundError` ao abrir um relatório | O sistema foi executado fora da pasta `src` | Entre na pasta `src` antes de executar |
