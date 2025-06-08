from sqlalchemy import create_engine, MetaData
from databases import Database
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# SQLite 데이터베이스 사용
DATABASE_URL = "sqlite:///./quicker.db"
database = Database(DATABASE_URL)
metadata = MetaData()

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite를 위한 설정
)

# 데이터베이스 연결/종료 이벤트
async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()