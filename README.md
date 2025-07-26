# Zap

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)

Zap is an AI-powered online accounting platform that lets you manage your business using voice commands and natural language. Easily track finances, generate reports, and handle operations — all through an intuitive, conversational interface.

## Features

- 🎙️ Voice-controlled business management
- 🧠 AI-assisted accounting tools
- 📊 Automatic financial reports
- 💬 Natural language interface
- ☁️ Cloud-based and accessible anywhere

## How to use ?

1. clone repository

```
git clone https://github.com/HDAI654/Zap.git
```

2. install dependence

```
pip install -r requirements.txt
```

3. create tables

```
python create_tables.py
```

4. Run

```
uvicorn main:app --reload
```

---

#### for login and register use

[This file](login_register.html)

#### register

```
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register"   -H "Content-Type: application/json"   -d '{"email": "example@gmail.com", "password": "your_password", "username": "your_username"}'
```

#### login

```
curl -X POST http://127.0.0.1:8000/api/v1/auth/login   -H "Content-Type: application/json"   -d '{"email": "example@gmail.com", "password": "your_password"}'
```

## Project Structure

See full [project structure here](STRUCTURE.md)

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

We welcome contributions! Please open an issue or submit a pull request.
Or you can send me Email for collaboration.

My Email : hdai.code@gmail.com
