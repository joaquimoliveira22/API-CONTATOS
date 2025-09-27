📖 Documentação da API de Contatos e Ligações

Esta API gerencia contatos telefônicos e o histórico de ligações associado a cada contato.
Foi desenvolvida em Flask + SQLAlchemy e está hospedada no Render.

🌐 URL Base
https://<seu-projeto-no-render>.onrender.com

📂 Endpoints
📌 Contatos
➕ Criar contato

POST /contatos
Body (JSON):
{
  "nome": "João",
  "sobrenome": "Silva",
  "apelido": "Jão",
  "telefone": "11999999999",
  "email": "joao@email.com",
  "ddd": "11"
}

Resposta (201):
{"mensagem": "Contato criado com sucesso!"}

📋 Listar todos os contatos
GET /contatos
Resposta (200):
[
  {
    "id": 1,
    "nome": "João",
    "sobrenome": "Silva",
    "apelido": "Jão",
    "telefone": "11999999999",
    "email": "joao@email.com",
    "ddd": "11"
  }
]

🔍 Buscar contato por ID
GET /contatos/{id}
Exemplo:
GET /contatos/1
Resposta (200):
{
  "id": 1,
  "nome": "João",
  "sobrenome": "Silva",
  "apelido": "Jão",
  "telefone": "11999999999",
  "email": "joao@email.com",
  "ddd": "11"
}

✏️ Editar contato
PUT /contatos/{id}
Body (JSON):
{
  "telefone": "11988888888",
  "email": "novo@email.com"
}
Resposta (200):
{"mensagem": "Contato 1 atualizado com sucesso!"}

❌ Deletar contato
DELETE /contatos/{id}
Resposta (200):
{"mensagem": "Contato 1 apagado com sucesso!"}

📞 Ligações
➕ Registrar ligação
POST /ligacoes
Body (JSON):
{
  "contato_id": 1,
  "duracao_segundos": 300,
  "tipo": "saida"
}
Resposta (201):
{"mensagem": "Ligação registrada com sucesso!"}

📋 Listar todas as ligações
GET /ligacoes
Resposta (200):

[
  {
    "id": 1,
    "contato_id": 1,
    "data_hora": "2025-09-26 10:00:00",
    "duracao_segundos": 300,
    "tipo": "saida"
  }
]

🔍 Listar ligações de um contato
GET /ligacoes/{contato_id}
Exemplo:
GET /ligacoes/1
Resposta (200):
[
  {
    "id": 1,
    "contato_id": 1,
    "data_hora": "2025-09-26 10:00:00",
    "duracao_segundos": 300,
    "tipo": "saida"
  }
]

✏️ Editar ligação
PUT /ligacoes/{id}
Body (JSON):
{
  "duracao_segundos": 200,
  "tipo": "entrada"
}
Resposta (200):
{"mensagem": "Ligação 1 atualizada com sucesso!"}

❌ Deletar ligação
DELETE /ligacoes/{id}
Resposta (200):
{"mensagem": "Ligação 1 apagada com sucesso!"}
