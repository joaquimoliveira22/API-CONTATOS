import requests

BASE_URL = "http://127.0.0.1:5000"

novo_contato = {
    "nome": "joaquim",
    "sobrenome": "Oliveira",
    "apelido": "joacas",
    "telefone": "989089830",
    "email": "auramaisego@gmail.com",
    "ddd": "85"
}
res = requests.post(f"{BASE_URL}/contatos", json=novo_contato)
print(res.json())

# Listar contatos
res = requests.get(f"{BASE_URL}/contatos")
print(res.json())

# Registrar ligação
nova_ligacao = {
    "contato_id": 2,  # id do contato, importante pra usar na hora de listar a ligação
    "duracao_segundos": 240,
    "tipo": "entrada"
}
res = requests.post(f"{BASE_URL}/ligacoes", json=nova_ligacao)
print(res.json())

# Histórico de ligações de um contato
res = requests.get(f"{BASE_URL}/ligacoes/1")
print(res.json())
