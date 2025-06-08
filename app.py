from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler
import os
from datetime import datetime, timedelta

# ... existing code ...

# 알림 블루프린트 등록
from routes.notifications import bp as notifications_bp
app.register_blueprint(notifications_bp)

# 알림 개수를 모든 템플릿에서 사용할 수 있도록 설정
@app.context_processor
def inject_unread_notifications():
    if current_user.is_authenticated:
        count = Notification.query.filter_by(
            admin_id=current_user.id,
            is_read=False
        ).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}

# ... existing code ... 