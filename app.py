import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量

app = Flask(__name__)
CORS(app)  # 允许所有域名跨域（开发阶段）

# ⚠️ 请替换以下数据库连接字符串
# 格式：postgresql://用户名:密码@localhost:5432/数据库名
# 示例：postgresql://postgres:123456@localhost:5432/leetcode_log_db
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@localhost:5432/leetcode_log_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------------- 数据模型 ----------------------
class LeetcodeLog(db.Model):
    __tablename__ = 'leetcode_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    problem_id = db.Column(db.Integer, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'time_spent': self.time_spent,
            'note': self.note,
            'created_at': self.created_at.isoformat()
        }

# ---------------------- API 路由 ----------------------
@app.route('/api/list', methods=['GET'])
def get_records():
    """获取所有记录，按创建时间倒序"""
    records = LeetcodeLog.query.order_by(LeetcodeLog.created_at.desc()).all()
    return jsonify([r.to_dict() for r in records])

@app.route('/api/add', methods=['POST'])
def add_record():
    """新增一条记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体不能为空'}), 400

    problem_id = data.get('problem_id')
    time_spent = data.get('time_spent')
    note = data.get('note', '')

    if problem_id is None or time_spent is None:
        return jsonify({'error': '题号和花费时间必须提供'}), 400
    try:
        problem_id = int(problem_id)
        time_spent = int(time_spent)
    except ValueError:
        return jsonify({'error': '题号和花费时间必须是数字'}), 400

    new_record = LeetcodeLog(
        problem_id=problem_id,
        time_spent=time_spent,
        note=note
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'status': 'ok'})

@app.route('/api/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    """删除指定 id 的记录"""
    record = LeetcodeLog.query.get(id)
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({'status': 'ok'})

# ---------------------- 创建表（首次运行自动创建）--------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # ⚠️ 本地调试：host='0.0.0.0' 让同一 WiFi 的设备可以访问，port=5000
    app.run(host='0.0.0.0', port=5000, debug=True)