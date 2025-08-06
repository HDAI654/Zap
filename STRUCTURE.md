```
Zap/
├── api/                           # All API routes grouped by version
│   ├── v1/
│   │   ├── endpoints/             # Route handlers (login, query, etc)
│   │   │   ├── auth.py           # Login, logout, register
│   │   │   ├── user.py           # User profile, settings
│   │   │   ├── voice.py          # Upload & transcribe voice
│   │   │   └── tables.py         # List & manage user tables
│   │   └── __init__.py
│   └── __init__.py

├── auth/                          # Authentication logic
│   ├── session_manager.py        # Create, read, delete session cookies
│   ├── dependencies.py           # get_current_user() for route protection
│   └── security.py               # Password hashing & verification

├── core/                          # App-wide config and startup
│   ├── config.py                 # Environment vars (DB, secrets, session)
│   └── logger.py                 # Global logger

├── db/                            # DB connection, models, and CRUD
│   ├── session.py                # DB session management (SQLAlchemy)
│   ├── base.py                   # Declarative base model
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── user.py               # User table schema
│   │   ├── session.py            # Session storage model
│   │   └── table_data.py         # User financial tables
│   └── crud/                     # DB operations (Create/Read/Update/Delete)
│       ├── user.py
│       ├── session.py
│       └── table.py

├── services/                      # Core logic & LLM integrations
│   ├── voice_to_text.py          # Convert voice to text (API)
│   ├── rag_builder.py            # Build prompt with question + table (RAG)
│   ├── llm_client.py             # Send prompt to LLM and get response
│   ├── manage.py                 # manage all process after user question
│   └── response_parser.py        # Parse model output into final answer


├── middleware/                    # Custom FastAPI middlewares
│   └── cors.py                    # set cors for main app

├── tests/                         # Unit and integration tests

├── main.py                        # Entry point for FastAPI app
├── requirements.txt               # Project dependencies
├── LICENSE                        # Project license
├── simple_panel.html              # base and simple panel for using features
├── .env                           # enviroment variables
├── .env.example                   # example for enviroment variables
├── STRUCTURE.md                   # Project structure
└── README.md                      # Project documentation

```
