from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

def carregar(df, if_exists="append"):
    engine = create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    df.to_sql("divida_ativa", engine, if_exists="replace",index=False)