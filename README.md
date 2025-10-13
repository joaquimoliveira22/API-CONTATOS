#  API de Contatos e Ligações

Esta API gerencia **contatos telefônicos** e o **histórico de ligações** associados a cada contato.  
Foi desenvolvida com **Flask + SQLAlchemy** e está hospedada no **Render**.

---

##  URL Base

```
https://<seu-projeto-no-render>.onrender.com
```

---

##  Funcionalidades da API

###  Autenticação

A API utiliza autenticação via **Bearer Token**.

>  Para acessar qualquer rota protegida, inclua o seguinte header:
>
> ```
> Authorization: Bearer <token>
> ```

---

##  Endpoints

### Registro e Login

#### **POST /registro** → Criar um novo usuário

**Body (JSON):**
```json
{
  "nome": "Joaquim",
  "email": "joaquim@email.com"
}
```

**Resposta (201):**
```json
{"mensagem": "Usuário registrado com sucesso!"}
```

---

#### **POST /login** → Fazer login e receber token

**Body (JSON):**
```json
{
  "email": "joaquim@email.com"
}
```

**Resposta (200):**
```json
{"token": "<seu_token_aqui>"}
```

---

## 📇 Contatos

### **POST /contatos** → Criar um novo contato

**Body (JSON):**
```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "apelido": "Jão",
  "telefone": "11999999999",
  "email": "joao@email.com",
  "ddd": "11"
}
```

**Resposta (201):**
```json
{"mensagem": "Contato criado com sucesso!"}
```

---

### **GET /contatos** → Listar todos os contatos

**Resposta (200):**
```json
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
```

---

### **GET /contatos/{id}** → Obter dados de um contato específico

**Exemplo:**
```
GET /contatos/1
```

**Resposta (200):**
```json
{
  "id": 1,
  "nome": "João",
  "sobrenome": "Silva",
  "apelido": "Jão",
  "telefone": "11999999999",
  "email": "joao@email.com",
  "ddd": "11"
}
```

---

### **PUT /contatos/{id}** → Atualizar dados de um contato

**Body (JSON):**
```json
{
  "telefone": "11988888888",
  "email": "novo@email.com"
}
```

**Resposta (200):**
```json
{"mensagem": "Contato 1 atualizado com sucesso!"}
```

---

### **DELETE /contatos/{id}** → Deletar um contato

**Resposta (200):**
```json
{"mensagem": "Contato 1 apagado com sucesso!"}
```

>  Ao deletar um contato, **todas as ligações associadas** são removidas automaticamente.

---

##  Ligações

### **POST /ligacoes** → Registrar uma nova ligação

**Body (JSON):**
```json
{
  "contato_id": 1,
  "duracao_segundos": 300,
  "tipo": "saida"
}
```

**Resposta (201):**
```json
{"mensagem": "Ligação registrada com sucesso!"}
```

---

### **GET /ligacoes** → Listar todas as ligações

**Resposta (200):**
```json
[
  {
    "id": 1,
    "contato_id": 1,
    "data_hora": "2025-09-26 10:00:00",
    "duracao_segundos": 300,
    "tipo": "saida"
  }
]
```

---

### **GET /ligacoes/{contato_id}** → Listar ligações de um contato específico

**Exemplo:**
```
GET /ligacoes/1
```

**Resposta (200):**
```json
[
  {
    "id": 1,
    "contato_id": 1,
    "data_hora": "2025-09-26 10:00:00",
    "duracao_segundos": 300,
    "tipo": "saida"
  }
]
```

---

### **PUT /ligacoes/{id}** → Atualizar uma ligação

**Body (JSON):**
```json
{
  "duracao_segundos": 200,
  "tipo": "entrada"
}
```

**Resposta (200):**
```json
{"mensagem": "Ligação 1 atualizada com sucesso!"}
```

---

### **DELETE /ligacoes/{id}** → Deletar uma ligação

**Resposta (200):**
```json
{"mensagem": "Ligação 1 apagada com sucesso!"}
```

---

##  Como Executar o Projeto Localmente

### 1️ Clone o repositório
```bash
git clone https://github.com/joaquimoliveira22/API-CONTATOS.git
cd API-CONTATOS
```

### 2️ Instale as dependências
```bash
pip install -r requirements.txt
```

> Se o arquivo `requirements.txt` não existir, instale manualmente:
```bash
pip install flask flask_sqlalchemy
```

### 3️ Execute a aplicação
```bash
python api.py
```

A API estará disponível em:
```
http://localhost:5000https://api-contatos-1.onrender.com
```

---

##  Observações

- Os campos **telefone** e **email** são **únicos** por contato.  
- Ao **deletar um contato**, todas as **ligações relacionadas** são excluídas automaticamente.  
- A autenticação é **obrigatória** para acessar as rotas protegidas.

---

##  Tecnologias Utilizadas

- **Python 3**
- **Flask**
- **SQLAlchemy**
- **SQLite**
- **Render (Hospedagem)**

---

##  Autor
**Bianca Torrers**

**Carlos Henrique**

**Joaquim Oliveira**



