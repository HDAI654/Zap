from uuid import uuid4
from ports.id_generator import IdGenerator

class UUID4Generator(IdGenerator):
    def generate():
        return str(uuid4())