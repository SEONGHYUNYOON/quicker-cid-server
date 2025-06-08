from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 서버 설정
    SERVER_NAME: str
    SERVER_HOST: str
    SERVER_PORT: int
    DEBUG_MODE: bool

    # 데이터베이스 설정
    DATABASE_URL: str

    # 보안 설정
    SECRET_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 관리자 설정
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    # CID 설정
    CID_PREFIX: str
    CID_LENGTH: int

    # 로깅 설정
    LOG_LEVEL: str
    LOG_FILE: str

    # 이메일 설정
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()