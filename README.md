# API Cifra Engineer

API desenvolvida em Python para manipulação de cifras musicais, com o objetivo de facilitar a transposição de acordes em cifras que já foram baixadas em seu dispositivo.

O projeto foi construído utilizando **Flask**, com organização modular e suporte a containerização com Docker.

---

## Funcionalidades

* Leitura de arquivos contendo cifras musicais (no momento apenas arquivos .txt e .pdf)
* Transposição de acordes (alterar o tom de uma música)
* Exposição de endpoints via API REST
* Organização modular para fácil manutenção e evolução

---

## Tecnologias Utilizadas

* Python
* Flask
* Docker
* Manipulação de arquivos

---

## Estrutura do Projeto

```
src/
├── app.py                 # Ponto de entrada da aplicação (API Flask)
├── ferramentas/
│   ├── musica.py          # Regras e lógica de manipulação musical
│   ├── file_reader.py     # Leitura e tratamento de arquivos
│   └── __init__.py
```

---

## Como Executar o Projeto

### Rodando localmente

1. Clone o repositório:

```
git clone https://github.com/Matheus-Soares2003/api-cifra-engineer.git
cd api-cifra-engineer
```

2. Crie um ambiente virtual:

```
python -m venv venv
```

3. Ative o ambiente:

**Windows:**

```
venv\Scripts\activate
```

**Linux/Mac:**

```
source venv/bin/activate
```

4. Instale as dependências:

```
pip install -r requirements.txt
```

5. Execute a aplicação:

```
python src/app.py
```

6. Acesse:

```
http://localhost:5000
```

---

### Rodando com Docker

```
docker build -t api-cifra-engineer .
docker run -p 5000:5000 api-cifra-engineer
```

---

## Endpoints

No momento, a API disponibiliza apenas um endpoint para fazer upload do arquivo contendo a cifra:

https://api-cifraengineer.onrender.com/upload

No corpo (enviar como form-data):

```
{
  "arquivo": arquivo.pdf (binário do arquivo com a cifra, podendo ser um .txt ou um .pdf) 
  "tom_original": string
  "tom_destino": string
}
```

---

## Possíveis Melhorias

* Criar testes automatizados
* Melhorar tratamento de erros
* Devolver a resposta em um arquivo JSON

---
## Autor

Matheus Soares Thomaz Cabral
https://www.linkedin.com/in/matheusstcabral
