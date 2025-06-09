#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

# 데이터베이스 파일 경로
db_path = 'quicker.db'

def update_database():
    """데이터베이스 스키마 업데이트"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # CID 테이블에 last_verified_at 컬럼이 있는지 확인
        cursor.execute("PRAGMA table_info(CID)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'last_verified_at' not in columns:
            print("Adding last_verified_at column to CID table...")
            cursor.execute("ALTER TABLE CID ADD COLUMN last_verified_at DATETIME")
            print("Successfully added last_verified_at column!")
        else:
            print("last_verified_at column already exists.")
            
        conn.commit()
        print("Database update completed!")
        
    except Exception as e:
        print(f"Error updating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_database() 