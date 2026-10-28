# Prompts desenvolvidos ao longo do projeto

## Prompt 1

"Faça uma revisão dos atributos e dos relacionamentos da minha tabela. Estou desenvolvendo um trabalho em grupo da máteria de banco de dados, o trabalho consiste em modelar, construir e programar um sistema de gerenciamento de academia de ginástica. Uma das minhas partes consiste em modelar as tabalas e diagramas do sistema.

Antes de modelar realizou um levantamento de atributos e tabelas que acho necessário, assim como os relacionamento entre elas:
ENTIDADES E ATRIBUTOS 

Aluno 
id_aluno int, pk, auto_increment not null
nome varchar2 not null
e-mail varchar2 not null
telefone varchar2 not null
gênero varchar2 not null

Instrutor
id_instrutor int, pk,auto_increment not null
nome varchar2 not null
cref VARCHAR UNIQUE NOT NULL
e-mail varchar2 not null
telefone number not null


Treino
id_treino int pk auto_increment
id_aluno int fk
id_instrutor int fk
nome varchar2 not null
objetivo varchar2 
data criação datetime not null

Frequencia 
id_frequencia int pk not null auto incremente
id_aluno int fk
data datetime not null
hora entrada datetime not null

Relacionamentos 
Um aluno possui vários treinos 
Um aluno possui várias presenças
Um instrutor monta/orientar  vários treinos 


A partir desse conteúdo, aponte o que está correto e com uma boa linha de raciocínio e o que posso melhorar para ter uma boa modelagem e construir tabelas"

Fonte : ChatGPT

Com a resposta do prompt foi possível perceber alguns erros no tipo do time escolhido para alguns atributos como telefone e algumas convenções na escrita de atributos. Após a análise, foi feita a correção do levantamento e seguiu para a parte do diagrama.

## Prompt 2 — Criação do banco de dados (Esther)

"A partir do diagrama relacional do grupo (ALUNO, INSTRUTOR, TREINO e FREQUENCIA) e das regras do edital, me ajude a entender e montar o script de criação das tabelas no Oracle (PK, FK, NOT NULL, UNIQUE e sequences), os dados de exemplo para testes e o script Python que executa esses arquivos, seguindo a estrutura do projeto de exemplo do professor."

Fonte : Claude Code (Anthropic)

Usei a ferramenta como apoio para estudar os conceitos (chaves, restrições e sequences) e para gerar uma primeira versão dos scripts a partir do diagrama do grupo. Revisei e entendi cada comando, mantive o padrão de nomes do projeto de exemplo, deixei as FKs sem ON DELETE CASCADE para atender ao item 6.c.5.i e testei no Oracle a criação das tabelas, os dados de exemplo e as restrições (FK, UNIQUE e NOT NULL).
