SELECT t.id_treino, t.nome AS treino, t.objetivo, a.nome AS aluno, i.nome AS instrutor, t.data_criacao
FROM treino t
INNER JOIN aluno a
    ON a.id_aluno = t.id_aluno
INNER JOIN instrutor i
    ON i.id_instrutor = t.id_instrutor
ORDER BY t.data_criacao DESC