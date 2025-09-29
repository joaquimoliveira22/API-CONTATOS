Documentação da API de Contatos e Ligações

Esta API gerencia contatos telefônicos e o histórico de ligações associado a cada contato.
Foi desenvolvida em Flask + SQLAlchemy e está hospedada no Render.

URL Base
https://<seu-projeto-no-render>.onrender.com


Funcionalidades da API:

CONTATOS

POST /contatos -> Criar um novo contato
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


GET /contatos -> Listar todos os contatos
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


GET /contatos/{id} -> Obter dados de um contato específico
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


PUT /contatos/{id} -> Atualizar dados de um contato
Body (JSON):
{
  "telefone": "11988888888",
  "email": "novo@email.com"
}
Resposta (200):
{"mensagem": "Contato 1 atualizado com sucesso!"}


DELETE /contatos/{id} -> Deletar um contato 
Resposta (200):
{"mensagem": "Contato 1 apagado com sucesso!"}


LIGAÇÕES 

POST /ligacoes -> Registrar uma nova ligação
Body (JSON):
{
  "contato_id": 1,
  "duracao_segundos": 300,
  "tipo": "saida"
}
Resposta (201):
{"mensagem": "Ligação registrada com sucesso!"}


GET /ligacoes -> Listar todas as ligações
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

 
GET /ligacoes/{contato_id} -> Listar ligações de um contato específico
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


PUT /ligacoes/{id} -> Atualizar uma ligação
Body (JSON):
{
  "duracao_segundos": 200,
  "tipo": "entrada"
}
Resposta (200):
{"mensagem": "Ligação 1 atualizada com sucesso!"}


DELETE /ligacoes/{id} -> Deletar uma ligação
Resposta (200):
{"mensagem": "Ligação 1 apagada com sucesso!"}

_______________________________________________________________________________

Como Executar o Projeto:

1. Clone o repositório
git clone https://github.com/joaquimoliveira22/API-CONTATOS.git
cd API-CONTATOS

2. Instale as dependências
pip install -r requirements.txt 

Se não tiver o arquivo requirements.txt, use:
pip install flask flask_sqlalchemy

3. Execute a aplicação
python api.py

A API estará disponível em:
http://localhost:5000

________________________________________________________________________________

Observações
- O campo telefone e email são únicos por contato.
- Ao deletar um contato, todas as ligações associadas também são deletadas automaticamente.