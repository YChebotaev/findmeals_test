from django.conf import settings
import sqlalchemy
import sqlalchemy.orm

engine = sqlalchemy.create_engine(settings.DATABASE_ENGINE)

Session = sqlalchemy.orm.sessionmaker(bind=engine)