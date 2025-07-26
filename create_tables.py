from db.base import Base
from db.session import engine

def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created")

if __name__ == "__main__":
    create_all_tables()
