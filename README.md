# LeetCode 刷题日志 📝

> 课程作业：输入题号自动获取题目名称，记录刷题用时与笔记的轻量工具。

## ✨ 主要功能

- **自动获取题目**：输入题号自动拉取 LeetCode 题目名称
- **快速记录**：填写耗时 + 可选笔记，一键添加刷题记录
- **列表管理**：按时间倒序展示，支持删除单条记录
- **全栈实现**：HTML + JavaScript + Flask + PostgreSQL

## 🚀 快速开始

### 环境要求

| 组件 | 版本 |
|------|------|
| Python | 3.8+ |
| PostgreSQL | 12+ |

### 安装步骤

1. 克隆仓库
   ```bash
   git clone https://github.com/GreyFoox/LeetLog.git
   cd LeetLog
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 创建数据库
   ```bash
   psql -U postgres -c "CREATE DATABASE leetcode_log_db;"
   ```

4. 配置数据库连接  
   编辑 `app.py`，修改连接字符串中的密码：
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:你的密码@127.0.0.1:5432/leetcode_log_db'
   ```

5. 启动服务
   | 系统 | 命令 |
   |------|------|
   | Linux / Mac | `./start.sh`（自动打开浏览器） |
   | Windows | 分别运行 `python app.py` 和 `python -m http.server 8080` |

6. 访问 `http://127.0.0.1:8080` 🎉

## 📖 使用说明

1. 输入题号（如 `1`），失去焦点后自动显示题目名称
2. 填写耗时（分钟），可选填写笔记
3. 点击「添加记录」
4. 列表按时间倒序展示，支持删除单条

## 🔌 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/list` | 获取所有记录 |
| POST | `/add` | 添加记录 |
| DELETE | `/delete/<id>` | 删除记录 |
| GET | `/title/<pid>` | 根据题号获取题目名称 |

## 🛠️ 技术栈

- 前端：HTML + 原生 JavaScript
- 后端：Flask (Python)
- 数据库：PostgreSQL + SQLAlchemy
- 数据获取：LeetCode 公共接口（无鉴权）

## ❓ 常见问题

- **数据库连接失败**：检查 `app.py` 中的用户名/密码/端口
- **端口被占用**：修改 `app.py` 的 `port` 和前端 `API_BASE`
- **题目标题不显示**：确认后端服务已启动，网络可访问 LeetCode

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

> 💡 小提示：欢迎提交 Issue 或 Pull Request 一起改进这个项目～
