from internal.db import Base, engine
from internal.models import User

Base.metadata.create_all(bind=engine)
