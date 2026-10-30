# Prompts desenvolvidos ao longo do projeto

## Prompt 1 — Modelagem do banco de dados

"Faça uma revisão dos atributos e dos relacionamentos da minha tabela. Estou desenvolvendo um trabalho em grupo da matéria de banco de dados, o trabalho consiste em modelar, construir e programar um sistema de gerenciamento de academia de ginástica. Uma das minhas partes consiste em modelar as tabelas e diagramas do sistema.

Antes de modelar, realizei um levantamento de atributos e tabelas que acho necessários, assim como os relacionamentos entre elas:

**Entidades e atributos**

**Aluno**
- id_aluno int, PK, auto_increment, NOT NULL
- nome varchar2 NOT NULL
- e-mail varchar2 NOT NULL
- telefone varchar2 NOT NULL
- gênero varchar2 NOT NULL

**Instrutor**
- id_instrutor int, PK, auto_increment, NOT NULL
- nome varchar2 NOT NULL
- cref VARCHAR UNIQUE NOT NULL
- e-mail varchar2 NOT NULL
- telefone number NOT NULL

**Treino**
- id_treino int, PK, auto_increment
- id_aluno int FK
- id_instrutor int FK
- nome varchar2 NOT NULL
- objetivo varchar2
- data_criação datetime NOT NULL

**Frequência**
- id_frequencia int, PK, NOT NULL, auto_increment
- id_aluno int FK
- data datetime NOT NULL
- hora_entrada datetime NOT NULL

**Relacionamentos**
- Um aluno possui vários treinos.
- Um aluno possui várias presenças.
- Um instrutor monta/orienta vários treinos.

A partir desse conteúdo, aponte o que está correto e com uma boa linha de raciocínio e o que posso melhorar para ter uma boa modelagem e construir tabelas."

**Fonte:** ChatGPT.

Com a resposta do prompt foi possível perceber alguns erros no tipo escolhido para alguns atributos, como telefone, e algumas convenções na escrita de atributos. Após a análise, foi feita a correção do levantamento e seguiu-se para a parte do diagrama.

## Prompt 2 — Criação do banco de dados (Esther)

"A partir do diagrama relacional do grupo (ALUNO, INSTRUTOR, TREINO e FREQUENCIA) e das regras do edital, me ajude a entender e montar o script de criação das tabelas no Oracle (PK, FK, NOT NULL, UNIQUE e sequences), os dados de exemplo para testes e o script Python que executa esses arquivos, seguindo a estrutura do projeto de exemplo do professor."

**Fonte:** Claude Code (Anthropic).

Usei a ferramenta como apoio para estudar os conceitos (chaves, restrições e sequences) e para gerar uma primeira versão dos scripts a partir do diagrama do grupo. Revisei e entendi cada comando, mantive o padrão de nomes do projeto de exemplo, deixei as FKs sem ON DELETE CASCADE para atender ao item 6.c.5.i e testei no Oracle a criação das tabelas, os dados de exemplo e as restrições (FK, UNIQUE e NOT NULL).

## Prompt 3 — README: instalação e banco de dados (Esther)

"Me ajude a entender exatamente o que o README precisa ter segundo o edital (como executar o projeto no Linux), para que não haja erros e o trabalho atenda ao que o professor pede, e me ajude a montar o README.md com a descrição das tabelas, a instalação, a configuração da conexão, a criação das tabelas e os problemas mais comuns."

**Fonte:** Claude Code (Anthropic).

A resposta explicou o que o edital exige no README e propôs uma estrutura e um texto para cada seção. Usei como base, revisei as instruções, conferi os comandos e os resultados esperados com os testes que fiz no Oracle e deixei a seção de execução do sistema para a Laysa completar com os menus.

## Desenvolvimento das classes Aluno e Treino

**Prompt utilizado:**

"Ajude-me a desenvolver as classes Python Aluno e Treino para um sistema de academia com banco de dados Oracle, seguindo o diagrama relacional e o edital da disciplina. Inclua construtores, getters, setters, método to_string e relacionamentos entre objetos."

**Fonte:** ChatGPT (OpenAI).

**Utilização da resposta:**

A resposta foi utilizada como apoio para implementar as classes Aluno e Treino, de acordo com os atributos das tabelas do banco Oracle.

As classes foram testadas na máquina virtual Linux utilizando Python 3, verificando a criação de objetos, a exibição dos atributos e o relacionamento entre Aluno, Treino e um instrutor temporário.

## Prompt 4 — Implementação e execução do sistema em Python (Laysa)

"Estou desenvolvendo, junto com meu grupo, um sistema de gerenciamento de academia para a disciplina de Banco de Dados, utilizando Python e Oracle. O projeto possui funcionalidades de gerenciamento de alunos, instrutores, treinos e frequências, além de relatórios. Preciso de ajuda para entender a estrutura do código, implementar e organizar o menu principal e os menus de cada funcionalidade, integrar as operações com o banco de dados Oracle e verificar a execução do sistema. Também preciso de orientação para testar as opções de cadastro, consulta, atualização, exclusão e relatórios, garantindo que a navegação entre os menus funcione corretamente."

**Fonte:** ChatGPT (OpenAI).

Com o apoio da ferramenta, foi possível compreender melhor a organização do código e a integração entre os menus, os controladores e o banco de dados Oracle. A partir das orientações, participei da implementação e dos ajustes do menu principal, da tela inicial (*Splash Screen*) e da navegação entre os menus de alunos, instrutores, treinos, frequências e relatórios. Também realizei testes de execução do sistema, verificando as operações disponíveis e a comunicação com o banco de dados, além de corrigir problemas encontrados durante os testes.