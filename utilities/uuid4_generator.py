from uuid import uuid4
from ports.id_generator import IdGenerator

class UUIDGenerator(IdGenerator):
    def generate():
        return str(uuid4())