from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String
import config

Base = declarative_base()
formFields = config.form_fields


class Register(Base):
    __tablename__ = config.table_name
    col1 = Column(formFields[0]['fname'], formFields[0]['ftype'], primary_key=True)
    col2 = Column(formFields[1]['fname'], formFields[1]['ftype'], nullable=formFields[1]['null'])
    col3 = Column(formFields[2]['fname'], formFields[2]['ftype'], nullable=formFields[2]['null'])

    def __repr__(self):
        return "Register(name ={}, email = {}, number = {})"\
               .format(self.col1, self.col2, self.col3)
