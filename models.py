from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from sqlalchemy import func, and_
import json

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    last_login = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime)
    is_locked = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'is_locked': self.is_locked
        }

class LoginLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(32)
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_used_at': self.last_used_at.strftime('%Y-%m-%d %H:%M:%S') if self.last_used_at else None,
            'is_active': self.is_active
        }

class ApiLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key_id = db.Column(db.Integer, db.ForeignKey('api_key.id'))
    endpoint = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    request_data = db.Column(db.Text)
    response_data = db.Column(db.Text)
    status_code = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    api_key = db.relationship('ApiKey', backref=db.backref('logs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'api_key': self.api_key.name if self.api_key else None,
            'endpoint': self.endpoint,
            'method': self.method,
            'request_data': self.request_data,
            'response_data': self.response_data,
            'status_code': self.status_code,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    deposit_amount = db.Column(db.Integer, default=0)
    referrer = db.Column(db.String(100))
    cids = db.relationship('CID', backref='member', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'registration_date': self.registration_date.strftime('%Y-%m-%d'),
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d'),
            'deposit_amount': self.deposit_amount,
            'referrer': self.referrer,
            'cids': [cid.cid_value for cid in self.cids]
        }

class CID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cid_value = db.Column(db.String(100), nullable=False, unique=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    # last_verified_at = db.Column(db.DateTime)  # 임시로 비활성화
    
    def to_dict(self):
        return {
            'id': self.id,
            'cid_value': self.cid_value,
            'member_id': self.member_id,
            'is_active': self.is_active,
            # 'last_verified_at': self.last_verified_at.strftime('%Y-%m-%d %H:%M:%S') if self.last_verified_at else None
        }

class Backup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    size = db.Column(db.Integer)  # 파일 크기 (bytes)
    description = db.Column(db.String(500))
    is_auto = db.Column(db.Boolean, default=False)  # 자동 백업 여부
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'size': self.size,
            'description': self.description,
            'is_auto': self.is_auto
        }

class BackupSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(20), nullable=False)  # daily, weekly, monthly
    time = db.Column(db.Time, nullable=False)  # 백업 시간
    retention_days = db.Column(db.Integer, default=30)  # 보관 기간
    is_active = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'frequency': self.frequency,
            'time': self.time.strftime('%H:%M'),
            'retention_days': self.retention_days,
            'is_active': self.is_active,
            'last_run': self.last_run.strftime('%Y-%m-%d %H:%M:%S') if self.last_run else None
        }

class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_members = db.Column(db.Integer, default=0)
    active_members = db.Column(db.Integer, default=0)
    total_cids = db.Column(db.Integer, default=0)
    active_cids = db.Column(db.Integer, default=0)
    api_calls = db.Column(db.Integer, default=0)
    new_members = db.Column(db.Integer, default=0)
    expired_members = db.Column(db.Integer, default=0)
    total_deposit = db.Column(db.Integer, default=0)
    
    @classmethod
    def calculate_stats(cls, date):
        """일일 통계 계산"""
        stats = cls.query.filter_by(date=date).first() or cls(date=date)
        
        # 전체 회원 수 및 활성 회원 수
        stats.total_members = Member.query.count()
        stats.active_members = Member.query.filter(Member.expiry_date >= date).count()
        
        # 전체 CID 수 및 활성 CID 수
        stats.total_cids = CID.query.count()
        stats.active_cids = CID.query.filter_by(is_active=True).count()
        
        # API 호출 수
        stats.api_calls = ApiLog.query.filter(
            func.date(ApiLog.timestamp) == date
        ).count()
        
        # 신규 회원 수
        stats.new_members = Member.query.filter(
            func.date(Member.registration_date) == date
        ).count()
        
        # 만료된 회원 수
        stats.expired_members = Member.query.filter(
            func.date(Member.expiry_date) == date
        ).count()
        
        # 총 입금액
        stats.total_deposit = db.session.query(
            func.sum(Member.deposit_amount)
        ).scalar() or 0
        
        db.session.add(stats)
        db.session.commit()
        return stats
    
    def to_dict(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'total_members': self.total_members,
            'active_members': self.active_members,
            'total_cids': self.total_cids,
            'active_cids': self.active_cids,
            'api_calls': self.api_calls,
            'new_members': self.new_members,
            'expired_members': self.expired_members,
            'total_deposit': self.total_deposit
        }

class MemberActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # registration, renewal, deposit
    amount = db.Column(db.Integer)  # 입금액
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)
    
    member = db.relationship('Member', backref=db.backref('activities', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'member_name': self.member.name,
            'activity_type': self.activity_type,
            'amount': self.amount,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'details': self.details
        }

# Member 모델에 통계 메서드 추가
def get_member_stats(cls, days=30):
    """회원 통계 조회"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    return {
        'total': cls.query.count(),
        'active': cls.query.filter(cls.expiry_date >= datetime.now()).count(),
        'new': cls.query.filter(cls.registration_date >= start_date).count(),
        'expired': cls.query.filter(
            and_(
                cls.expiry_date >= start_date,
                cls.expiry_date < end_date
            )
        ).count(),
        'total_deposit': db.session.query(func.sum(cls.deposit_amount)).scalar() or 0,
        'avg_deposit': db.session.query(func.avg(cls.deposit_amount)).scalar() or 0
    }

Member.get_stats = classmethod(get_member_stats)

# CID 모델에 통계 메서드 추가
def get_cid_stats(cls):
    """CID 통계 조회"""
    return {
        'total': cls.query.count(),
        'active': cls.query.filter_by(is_active=True).count(),
        'per_member_avg': db.session.query(
            func.avg(
                db.session.query(func.count(cls.id))
                .filter(cls.member_id == Member.id)
                .group_by(cls.member_id)
                .scalar_subquery()
            )
        ).scalar() or 0
    }

CID.get_stats = classmethod(get_cid_stats)

# ApiLog 모델에 통계 메서드 추가
def get_api_stats(cls, days=30):
    """API 사용 통계 조회"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    return {
        'total_calls': cls.query.filter(cls.timestamp >= start_date).count(),
        'success_rate': db.session.query(
            func.avg(cls.status_code.between(200, 299))
        ).filter(cls.timestamp >= start_date).scalar() or 0,
        'calls_by_endpoint': db.session.query(
            cls.endpoint,
            func.count(cls.id)
        ).filter(cls.timestamp >= start_date).group_by(cls.endpoint).all(),
        'calls_by_date': db.session.query(
            func.date(cls.timestamp),
            func.count(cls.id)
        ).filter(cls.timestamp >= start_date).group_by(
            func.date(cls.timestamp)
        ).all()
    }

ApiLog.get_stats = classmethod(get_api_stats)

class NotificationSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # expiry, api_usage, error, backup, security
    email_enabled = db.Column(db.Boolean, default=True)
    web_enabled = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(20), default='normal')  # high, normal, low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    admin = db.relationship('Admin', backref=db.backref('notification_settings', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'email_enabled': self.email_enabled,
            'web_enabled': self.web_enabled,
            'priority': self.priority
        }

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')
    data = db.Column(db.Text)  # JSON 형식의 추가 데이터
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    admin = db.relationship('Admin', backref=db.backref('notifications', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'priority': self.priority,
            'data': json.loads(self.data) if self.data else None,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def create_notification(cls, admin_id, type, title, message, priority='normal', data=None):
    """알림 생성 및 설정에 따른 전송"""
    # 알림 설정 확인
    setting = NotificationSetting.query.filter_by(
        admin_id=admin_id,
        type=type
    ).first()
    
    if not setting:
        # 기본 설정으로 생성
        setting = NotificationSetting(
            admin_id=admin_id,
            type=type,
            priority=priority
        )
        db.session.add(setting)
    
    # 알림 생성
    notification = cls(
        admin_id=admin_id,
        type=type,
        title=title,
        message=message,
        priority=priority,
        data=json.dumps(data) if data else None
    )
    db.session.add(notification)
    db.session.commit()
    
    # 이메일 알림 전송 (설정된 경우)
    if setting.email_enabled:
        admin = Admin.query.get(admin_id)
        if admin and admin.email:
            send_email_notification(
                admin.email,
                notification.title,
                notification.message
            )
    
    return notification

Notification.create = classmethod(create_notification)

def send_email_notification(email, title, message):
    """이메일 알림 전송 (실제 구현 필요)"""
    # TODO: 이메일 전송 구현
    pass

# 알림 생성이 필요한 모델들에 이벤트 리스너 추가
from sqlalchemy import event

@event.listens_for(Member.expiry_date, 'set')
def check_member_expiry(target, value, oldvalue, initiator):
    """회원 만료일 변경 시 만료 예정 알림"""
    if value and isinstance(value, datetime):
        days_until_expiry = (value - datetime.now()).days
        if days_until_expiry <= 7:
            Notification.create(
                admin_id=1,  # TODO: 실제 관리자 ID 사용
                type='expiry',
                title='회원 만료 예정',
                message=f'회원 {target.name}의 이용 기간이 {days_until_expiry}일 후 만료됩니다.',
                priority='high' if days_until_expiry <= 3 else 'normal',
                data={'member_id': target.id}
            )

@event.listens_for(ApiLog, 'after_insert')
def check_api_usage(mapper, connection, target):
    """API 사용량 모니터링"""
    # 시간당 호출 수 체크
    hour_ago = datetime.utcnow() - timedelta(hours=1)
    calls_last_hour = ApiLog.query.filter(
        ApiLog.api_key_id == target.api_key_id,
        ApiLog.timestamp >= hour_ago
    ).count()
    
    if calls_last_hour > 1000:  # 임계값
        Notification.create(
            admin_id=1,  # TODO: 실제 관리자 ID 사용
            type='api_usage',
            title='API 사용량 경고',
            message=f'API 키의 시간당 사용량이 임계값을 초과했습니다. (최근 1시간: {calls_last_hour}회)',
            priority='high',
            data={'api_key_id': target.api_key_id}
        )
    
    # 오류 응답 모니터링
    if target.status_code >= 400:
        Notification.create(
            admin_id=1,  # TODO: 실제 관리자 ID 사용
            type='error',
            title='API 오류 발생',
            message=f'API 호출 중 오류가 발생했습니다. (상태 코드: {target.status_code})',
            priority='high' if target.status_code >= 500 else 'normal',
            data={
                'api_key_id': target.api_key_id,
                'endpoint': target.endpoint,
                'status_code': target.status_code
            }
        ) 