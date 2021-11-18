
from sqlalchemy import create_engine

# Create a database connection
db_password = 'Kumara-42/600'  # Set to your own password
db_port = 6543
engine = create_engine('postgresql://postgres:{}@localhost:{}/Finance'.format(db_password, db_port))
