import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:1234@127.0.0.1:5432/leetcode_log_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, nullable=False)
    problem_title = db.Column(db.String(200), nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.now)

@app.route('/list')
def list_logs():
    logs = Log.query.order_by(Log.created_at.desc()).all()
    return jsonify([{
        'id': l.id,
        'problem_id': l.problem_id,
        'problem_title': l.problem_title,
        'time_spent': l.time_spent,
        'note': l.note,
        'created_at': l.created_at.isoformat()
    } for l in logs])

@app.route('/add', methods=['POST'])
def add_log():
    data = request.json
    log = Log(
        problem_id=data['problem_id'],
        problem_title=data['problem_title'],
        time_spent=data['time_spent'],
        note=data.get('note', '')
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'ok': True})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_log(id):
    Log.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'ok': True})

# 题目标题缓存
problem_cache = {}
def get_title(pid):
    pid = str(pid)
    if pid in problem_cache:
        return problem_cache[pid]
    if not problem_cache:
        resp = requests.get('https://leetcode.com/api/problems/all/', timeout=5)
        for item in resp.json()['stat_status_pairs']:
            qid = str(item['stat']['frontend_question_id'])
            title = item['stat']['question__title']
            problem_cache[qid] = title
    return problem_cache.get(pid, '未知题目')

@app.route('/title/<int:pid>')
def get_title_api(pid):
    return jsonify({'title': get_title(pid)})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000)
