from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from models import db, Notification, NotificationSetting
from datetime import datetime

bp = Blueprint('notifications', __name__)

@bp.route('/notifications')
@login_required
def notifications_page():
    """알림 센터 페이지"""
    notifications = Notification.query.filter_by(admin_id=current_user.id)\
        .order_by(Notification.created_at.desc()).all()
    
    # 알림 설정 가져오기
    settings = {}
    notification_settings = NotificationSetting.query.filter_by(admin_id=current_user.id).all()
    for setting in notification_settings:
        settings[setting.type] = setting.to_dict()
    
    return render_template('notifications.html', 
                         notifications=notifications,
                         settings=settings)

@bp.route('/api/notifications/settings', methods=['POST'])
@login_required
def update_notification_settings():
    """알림 설정 업데이트"""
    settings = request.json
    
    for type_, config in settings.items():
        setting = NotificationSetting.query.filter_by(
            admin_id=current_user.id,
            type=type_
        ).first()
        
        if not setting:
            setting = NotificationSetting(
                admin_id=current_user.id,
                type=type_
            )
            db.session.add(setting)
        
        setting.email_enabled = config['email_enabled']
        setting.web_enabled = config['web_enabled']
        setting.priority = config['priority']
    
    db.session.commit()
    return jsonify({'status': 'success'})

@bp.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """알림 읽음 표시"""
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.admin_id != current_user.id:
        return jsonify({'error': '권한이 없습니다.'}), 403
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'status': 'success'})

@bp.route('/api/notifications/<int:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """알림 삭제"""
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.admin_id != current_user.id:
        return jsonify({'error': '권한이 없습니다.'}), 403
    
    db.session.delete(notification)
    db.session.commit()
    
    return jsonify({'status': 'success'})

@bp.route('/api/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """모든 알림 읽음 표시"""
    Notification.query.filter_by(admin_id=current_user.id)\
        .update({'is_read': True})
    db.session.commit()
    
    return jsonify({'status': 'success'})

@bp.route('/api/notifications/clear-all', methods=['DELETE'])
@login_required
def clear_all_notifications():
    """모든 알림 삭제"""
    Notification.query.filter_by(admin_id=current_user.id).delete()
    db.session.commit()
    
    return jsonify({'status': 'success'})

@bp.route('/api/notifications/unread-count')
@login_required
def get_unread_count():
    """읽지 않은 알림 개수"""
    count = Notification.query.filter_by(
        admin_id=current_user.id,
        is_read=False
    ).count()
    
    return jsonify({'count': count}) 