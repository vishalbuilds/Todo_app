#authentication process for a database
from sqlalchemy import URL
aurh_url = URL.create(
    drivername="postgresql+asyncpg",
    username="vishal",  
    password="vishal123",
    host="localhost",
    port=5432,  
    database="testdb"
)