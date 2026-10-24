SELECT a.id_aluno, a.nome AS aluno, COUNT(t.id_treino) AS quantidade_treinos
FROM aluno a
LEFT JOIN treino t
    ON t.id_aluno = a.id_aluno
GROUP BY a.id_aluno, a.nome
ORDER BY a.nome