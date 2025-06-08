from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from datetime import datetime

metadata = MetaData()

# CID 관리 테이블
cid_management = Table(
    "cid_management",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cid", String(64), unique=True, nullable=False),
    Column("device_id", String(255)),
    Column("device_info", String),  # 디바이스 정보 저장
    Column("status", String(20)),   # PENDING, APPROVED, REJECTED
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("approved_at", DateTime, nullable=True),
    Column("notes", String, nullable=True)  # 추가 메모 사항
)

# CID 이력 테이블
cid_history = Table(
    "cid_history",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cid_id", Integer),
    Column("action", String(50)),  # CREATE, APPROVE, REJECT
    Column("action_date", DateTime, default=datetime.utcnow),
    Column("details", String)  # 변경 세부사항
)