from sqlalchemy import BigInteger, String

# create a local postgresql database and server
# Scheme : "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = ''

table_name = 'register'

# First column has to be primary key
form_fields = [{'fname': 'name', 'ftype': String, },
               {'fname': 'email', 'ftype': String, 'null': False},
               {'fname': 'number', 'ftype': BigInteger, 'null': True}, ]
