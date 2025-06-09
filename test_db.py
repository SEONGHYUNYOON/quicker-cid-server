#!/usr/bin/env python3
import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app, db, Member
    
    with app.app_context():
        print("=== Database Connection Test ===")
        
        # 데이터베이스 연결 테스트
        try:
            members = Member.query.all()
            print(f"✓ Database connection OK")
            print(f"✓ Found {len(members)} existing members")
            
            # 기존 회원 정보 출력
            for member in members:
                print(f"  - {member.name} ({member.phone})")
            
            # 테스트 회원 추가 시도
            test_member = Member(
                name="테스트회원",
                phone="01000000000",
                registration_date=datetime.now(),
                expiry_date=datetime.now() + timedelta(days=365),
                deposit_amount=0
            )
            
            db.session.add(test_member)
            db.session.commit()
            print("✓ Test member added successfully")
            
            # 다시 조회
            members_after = Member.query.all()
            print(f"✓ Members after insert: {len(members_after)}")
            
            # 테스트 회원 삭제
            db.session.delete(test_member)
            db.session.commit()
            print("✓ Test member removed")
            print("✓ Database write/read operations working correctly")
            
        except Exception as e:
            print(f"✗ Database error: {e}")
            import traceback
            traceback.print_exc()
            
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ General error: {e}")
    import traceback
    traceback.print_exc() 