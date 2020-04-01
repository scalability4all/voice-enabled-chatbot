import config
import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect

engine = create_engine(config.DATABASE_URI)
Session = sessionmaker(bind=engine)


class crudOps:
    def createTable(self):
        models.Base.metadata.create_all(engine)

    def recreate_database(self):
        models.Base.metadata.drop_all(engine)
        models.Base.metadata.create_all(engine)

    def insertRow(self, row):
        s = Session()
        s.add(row)
        s.commit()
        s.close_all()

    def allRow(self):
        s = Session()
        data = s.query(models.Register).all()
        s.close_all()
        return data

    def primaryCol(self):
        s = Session()
        dataList = []
        data = s.query(models.Register.col1)
        for i in data:
            for j in i:
                dataList.append(j)
        s.close_all()
        return dataList


a = crudOps()

# Checking if register table present or not
inspector = inspect(engine)
table_present = False
for table_name in inspector.get_table_names():
    if table_name == config.table_name:
        table_present = True
if not table_present:
    a.createTable()
