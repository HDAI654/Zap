```
Zap/
├── api/                           # All API routes grouped by version
│   ├── v1/
│   │   ├── endpoints/             # Route handlers (login, query, etc)
│   │   │   ├── auth.py           # Login, logout, register
│   │   │   ├── user.py           # User profile, settings
│   │   │   ├── voice.py          # Upload & transcribe voice
│   │   │   ├── query.py          # Handle user questions (natural lang)
│   │   │   └── tables.py         # List & manage user tables
│   │   └── __init__.py
│   └── __init__.py

├── auth/                          # Authentication logic
│   ├── session_manager.py        # Create, read, delete session cookies
│   ├── dependencies.py           # get_current_user() for route protection
│   └── security.py               # Password hashing & verification

├── core/                          # App-wide config and startup
│   ├── config.py                 # Environment vars (DB, secrets, session)
│   ├── constants.py              # Global constants
│   └── startup.py                # App init: DB, middleware, etc

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

├── models/                        # Pydantic models (request/response)
│   ├── user.py                   # Login, Register schemas
│   ├── auth.py                   # Session/cookie schema
│   ├── query.py                  # User query schema
│   ├── table.py                  # Table metadata schemas
│   └── voice.py                  # Audio upload schemas

├── services/                      # Core logic & LLM integrations
│   ├── voice_to_text.py          # Convert voice to text (Whisper/API)
│   ├── intent_analyzer.py        # Determine user intent/table from question
│   ├── table_loader.py           # Load relevant user table data
│   ├── rag_builder.py            # Build prompt with question + table (RAG)
│   ├── llm_client.py             # Send prompt to LLM and get response
│   └── response_parser.py        # Parse model output into final answer

├── utils/                         # Reusable utility functions
│   ├── audio_tools.py            # Audio conversion, validation, storage
│   ├── translator.py             # Translate input (e.g., Persian → English)
│   └── helpers.py                # Common helper functions (dates, etc)

├── middleware/                    # Custom FastAPI middlewares
│   └── session_cookie.py         # Read session cookie on every request

├── tests/                         # Unit and integration tests

├── main.py                        # Entry point for FastAPI app
├── requirements.txt               # Project dependencies
├── LICENSE                        # Project license
├── STRUCTURE.md                   # Project structure
└── README.md                      # Project documentation

```
