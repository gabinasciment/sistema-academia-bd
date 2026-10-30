-- =====================================================================
-- SISTEMA DE ACADEMIA - criacao das tabelas e relacionamentos (Oracle)
-- Banco de Dados 2026/2 - Prof. Howard Roatti
--
-- Baseado no diagrama relacional (diagramas/diagramarelacional.mmd)
-- Tabelas pai:   ALUNO, INSTRUTOR
-- Tabelas filha: TREINO (aponta para ALUNO e INSTRUTOR)
--                FREQUENCIA (aponta para ALUNO)
--
-- ATENCAO: o programa Python separa os comandos deste arquivo pelo
-- ponto e virgula. Por isso NUNCA use ponto e virgula dentro de
-- comentarios, so no final de cada comando.
-- =====================================================================


-- ============ 1. LIMPEZA (para poder rodar o script de novo) =========
-- Ordem: primeiro as filhas, depois os pais.
-- Na 1a execucao estes comandos dao erro "tabela nao existe" (ORA-00942)
-- e isso e normal.

DROP TABLE TREINO;
DROP TABLE FREQUENCIA;
DROP TABLE ALUNO;
DROP TABLE INSTRUTOR;

DROP SEQUENCE ALUNO_ID_ALUNO_SEQ;
DROP SEQUENCE INSTRUTOR_ID_INSTRUTOR_SEQ;
DROP SEQUENCE TREINO_ID_TREINO_SEQ;
DROP SEQUENCE FREQUENCIA_ID_FREQUENCIA_SEQ;


-- ============ 2. TABELAS PAI =========================================

CREATE TABLE ALUNO (
    ID_ALUNO          NUMBER          NOT NULL,
    NOME_ALUNO        VARCHAR2(100)   NOT NULL,
    EMAIL_ALUNO       VARCHAR2(64)    NOT NULL,
    TELEFONE_ALUNO    VARCHAR2(20)    NOT NULL,   -- texto: pode ter zero e nao se faz conta
    DATA_NASCIMENTO   DATE            NOT NULL,
    GENERO            VARCHAR2(10)    NOT NULL,
    CONSTRAINT ALUNO_PK       PRIMARY KEY (ID_ALUNO),
    CONSTRAINT ALUNO_EMAIL_UK UNIQUE (EMAIL_ALUNO)   -- dois alunos nao podem ter o mesmo e-mail
);

CREATE TABLE INSTRUTOR (
    ID_INSTRUTOR        NUMBER          NOT NULL,
    NOME_INSTRUTOR      VARCHAR2(100)   NOT NULL,
    EMAIL_INSTRUTOR     VARCHAR2(64)    NOT NULL,
    TELEFONE_INSTRUTOR  VARCHAR2(20)    NOT NULL,
    CONSTRAINT INSTRUTOR_PK       PRIMARY KEY (ID_INSTRUTOR),
    CONSTRAINT INSTRUTOR_EMAIL_UK UNIQUE (EMAIL_INSTRUTOR)
);


-- ============ 3. TABELAS FILHA ======================================

CREATE TABLE TREINO (
    ID_TREINO       NUMBER          NOT NULL,
    ID_ALUNO        NUMBER          NOT NULL,   -- FK: todo treino e de um aluno
    ID_INSTRUTOR    NUMBER          NOT NULL,   -- FK: todo treino tem um instrutor
    NOME_TREINO     VARCHAR2(100)   NOT NULL,
    OBJETIVO        VARCHAR2(200)   NOT NULL,
    DATA_CRIACAO    DATE            DEFAULT SYSDATE NOT NULL,
    CONSTRAINT TREINO_PK PRIMARY KEY (ID_TREINO)
);

CREATE TABLE FREQUENCIA (
    ID_FREQUENCIA       NUMBER   NOT NULL,
    ID_ALUNO            NUMBER   NOT NULL,      -- FK: toda entrada e de um aluno
    DATA_HORA_ENTRADA   DATE     DEFAULT SYSDATE NOT NULL,   -- DATE do Oracle guarda data e hora
    CONSTRAINT FREQUENCIA_PK PRIMARY KEY (ID_FREQUENCIA)
);


-- ============ 4. SEQUENCES (geram os IDs automaticamente) ============

CREATE SEQUENCE ALUNO_ID_ALUNO_SEQ             START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE INSTRUTOR_ID_INSTRUTOR_SEQ     START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE TREINO_ID_TREINO_SEQ           START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE FREQUENCIA_ID_FREQUENCIA_SEQ   START WITH 1 INCREMENT BY 1;


-- ============ 5. RELACIONAMENTOS (chaves estrangeiras) ===============
-- Todas SEM "ON DELETE CASCADE", de proposito: quem decide se apaga os
-- registros filhos e o programa, perguntando ao usuario (edital 6.c.5.i).
-- Se alguem tentar apagar um pai que tem filhos, o Oracle bloqueia
-- com o erro ORA-02292.

ALTER TABLE TREINO ADD CONSTRAINT ALUNO_TREINO_FK
FOREIGN KEY (ID_ALUNO)
REFERENCES ALUNO (ID_ALUNO);

ALTER TABLE TREINO ADD CONSTRAINT INSTRUTOR_TREINO_FK
FOREIGN KEY (ID_INSTRUTOR)
REFERENCES INSTRUTOR (ID_INSTRUTOR);

ALTER TABLE FREQUENCIA ADD CONSTRAINT ALUNO_FREQUENCIA_FK
FOREIGN KEY (ID_ALUNO)
REFERENCES ALUNO (ID_ALUNO);


-- ============ 6. PERMISSAO DE ESPACO PARA O USUARIO DA VM ============
-- Igual ao projeto de exemplo. Se o usuario ja tiver permissao, o
-- comando pode dar erro e tudo bem.

ALTER USER LABDATABASE QUOTA UNLIMITED ON USERS;
