from  app import db, create_app, WatchHistory

# 创建一个Flask应用实例
app = create_app()

# 激活上下文
with app.app_context():
    # 创建一个新的观看记录实例
    new_record = WatchHistory(user_id='3', video_class='tricep Pushdown')

    # 添加记录到会话并提交到数据库
    db.session.add(new_record)
    db.session.commit()