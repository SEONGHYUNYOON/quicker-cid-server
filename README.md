# Quicker CID 관리 서버

배달 기사 자동 주문 수락 앱 "Quicker(지지기)"의 CID 인증 및 회원 관리 시스템

## 🚀 주요 기능

- **회원 관리**: 300+ 회원 정보 및 CID 관리
- **CID 인증 API**: 모바일 앱 연동용 REST API
- **관리자 대시보드**: 웹 기반 관리 인터페이스
- **백업 시스템**: 자동/수동 백업 및 복원
- **통계 분석**: 실시간 사용량 및 회원 통계
- **알림 시스템**: 만료 예정 회원 알림

## 📱 시스템 구성

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: Bootstrap 5, Chart.js
- **API**: RESTful API with 인증
- **보안**: Flask-Login, Rate Limiting

## 🌐 AWS EC2 배포

### 1. EC2 인스턴스 생성
```bash
# 보안 그룹 설정
SSH (22): Your IP
HTTP (80): 0.0.0.0/0
Custom TCP (5000): 0.0.0.0/0
```

### 2. 서버 접속 및 배포
```bash
# SSH 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 배포 스크립트 실행
wget https://raw.githubusercontent.com/[YOUR_USERNAME]/quicker-cid-server/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### 3. 접속 확인
```
웹 관리자: http://your-ec2-ip
API 엔드포인트: http://your-ec2-ip/api/v1/verify
초기 비밀번호: 4568
```

## 📡 API 사용법

### CID 검증
```bash
curl -X POST http://your-server/api/v1/verify \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"cid": "device-unique-id"}'
```

### 응답 예시
```json
{
  "success": true,
  "member": {
    "name": "홍길동",
    "expiry_date": "2024-12-31",
    "status": "active"
  }
}
```

## 🔧 로컬 개발 환경

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 개발 서버 실행
python main.py
```

## 📊 관리자 기능

- **회원 관리**: CRUD 작업, 엑셀 내보내기
- **API 키 관리**: 키 생성/삭제, 사용량 모니터링
- **백업 관리**: 자동 백업 스케줄링
- **통계 분석**: Chart.js 기반 시각화
- **로그 분석**: API 호출 및 오류 로그

## 🔒 보안 기능

- 로그인 시도 제한 (5회)
- API Rate Limiting (10 req/min)
- 세션 기반 인증
- bcrypt 패스워드 해싱

## 💾 백업 시스템

- 일일/주간/월간 자동 백업
- 백업 파일 관리 및 정리
- 원클릭 복원 기능

## 📞 지원

문의사항이 있으시면 이슈를 등록해주세요. 